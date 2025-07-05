import { Button, FormGroup, FormHelperText, SelectChangeEvent, TextField } from "@mui/material";
import { useState, useEffect, FormEvent, ChangeEvent } from "react";
import { Series, Season, Channel, SeasonAppearance, Video, GetVideosPayload, CreatePlaylistPayload, Playlist } from "../../../types/api";
import SeasonSelect from "./SeasonSelect";
import SeriesSelect from "./SeriesSelect";
import '../PlaylistInputForm.css'
import ChannelCheckbox from "./ChannelCheckbox";
import { useNavigate } from "react-router"
import { AuthenticatedTemplate } from "@azure/msal-react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import useFetchWithMsal from "../../../utils/useFetchWithMsal";
import { protectedResources } from "../../../utils/authConfig";
import { BASE_API_URL } from "../../../utils/config";
import { UUID } from "crypto";
import { BackgroundPaper } from "../../../components/BackgroundPaper";
import { ChannelForm } from "./ChannelForm";
//import { handleAuth } from "../../youtube-playlist-creation/GoogleApiHandler";

interface Props {
    seasonAppearance: SeasonAppearance;
}

const PlaylistInputForm = ({ seasonAppearance }: Props) => {
    const [playlistTitle, setPlaylistTitle] = useState<string>('Minecraft Playlist');

    const [seriesList, setSeriesList] = useState<Series[]>(seasonAppearance.series);
    // TODO: Check using undefined here
    const [selectedSeries, setSelectedSeries] = useState<Series>(seriesList[0]);

    const [seasons, setSeasons] = useState<Season[]>(selectedSeries.seasons);
    // TODO: Might want to order the seasons alphanumerically here as well, maybe also the series above
    const [selectedSeason, setSelectedSeason] = useState<Season>(seasons[0]);

    const [channels, setChannels] = useState<Channel[]>(selectedSeason.channels);
    const [selectedChannels, setSelectedChannels] = useState<Channel[]>([]);

    let navigate = useNavigate();

    const { error, execute } = useFetchWithMsal({ scopes: [protectedResources.playlistApi.scopes.write, protectedResources.playlistVideoApi.scopes.write] });
    const queryClient = useQueryClient();

    const [selectedChannelsError, setSelectedChannelsError] = useState<boolean>((selectedChannels.length < 1) || (selectedChannels.length > 5));

    // TODO: Add payload to mutation key?
    const createPlaylistMutation = useMutation({
        mutationKey: ['createPlaylists'],
        mutationFn: async (payload: CreatePlaylistPayload) => {
            return await execute('POST', protectedResources.playlistApi.endpoint, payload);
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['playlists'] });
        }
    });

    const createPlaylistVideosMutation = useMutation({
        mutationKey: ['createPlaylistVideos'],
        mutationFn: async (params: { playlistId: UUID, payload: string[] }) => {
            console.log(params.playlistId);
            console.log(params.payload);
            return await execute('POST', `${protectedResources.playlistApi.endpoint}/${params.playlistId}/playlistVideos`, { channelNames: params.payload })
        }
    })

    const fetchSeasons = async (seriesTitle: string) => {
        try {
            const seasonsData = seasonAppearance.series.find((s: Series) => s.seriesTitle == seriesTitle)?.seasons;
            if (seasonsData === undefined) {
                throw new Error('Could not find season data');
            }
            seasonsData.sort((a: Season, b: Season) => a.seasonTitle.localeCompare(b.seasonTitle, undefined, { numeric: true, sensitivity: 'base' }))
            setSeasons(seasonsData);
        } catch (err) {
            console.log(err);
        }
    };

    const handleSeriesChange = (event: SelectChangeEvent) => {
        const selectedTitle = event.target.value as string;
        const series = seasonAppearance.series.find((series: Series) => series.seriesTitle === selectedTitle)
        if (!series) {
            throw new Error('The selected series could not be found.');
        }
        setSelectedSeries(series);
        setSeasons([]);
        setChannels([]);
        fetchSeasons(selectedTitle)
    };

    const handleSeasonChange = (event: SelectChangeEvent) => {
        if (selectedSeries) {
            const selectedTitle = event.target.value as string;
            const season = selectedSeries.seasons.find((season: Season) => season.seasonTitle === selectedTitle)
            if (!season) {
                throw new Error('The selected season could not be found.');
            }
            setSelectedSeason(season);
            setChannels([]);
            setSelectedChannels([]);
        }
    };

    const handleSubmit = async (event: FormEvent) => {
        event.preventDefault();
        const playlistPayload: CreatePlaylistPayload = {
            playlistTitle: playlistTitle,
            seriesTitle: selectedSeries.seriesTitle,
            seasonTitle: selectedSeason.seasonTitle
        };

        await createPlaylist(playlistPayload);

        const videosPayload: GetVideosPayload = {
            seriesTitle: selectedSeries.seriesTitle,
            seasonTitle: selectedSeason.seasonTitle,
            channelNames: selectedChannels.map(channel => channel.channelName)
        }
        //const videos: Video[] = await fetchVideos(videosPayload);
        //await handleAuth(videos);
        navigate("/playlists");
    }

    /* const fetchVideos = async (payload: GetVideosPayload): Promise<Video[]> => {
        console.log(JSON.stringify(payload));
        const response = await fetch(`${BASE_API_URL}/api/videos`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });
        if (!response.ok) {
            throw new Error('Failed to fetch video data');
        }
        const videos: Video[] = await response.json();
        console.log('Fetched videos');
        return videos;
    } */

    const createPlaylist = async (payload: CreatePlaylistPayload) => {
        console.log(JSON.stringify(payload));

        try {
            const response = await createPlaylistMutation.mutateAsync(payload);
            console.log(response);
            const createdPlaylist: Playlist = response
            console.log(createdPlaylist)
            console.log('Created playlist');
            const playlistId: UUID = createdPlaylist.publicPlaylistId;

            const channelNames = selectedChannels.map(channel => channel.channelName)
            const createPlaylistVideosRes = await createPlaylistVideosMutation.mutateAsync({ playlistId: playlistId, payload: channelNames });
            console.log('Created playlist items');
            console.log(createPlaylistVideosRes);

        } catch (error) {
            console.log("Error creating playlist");
            console.log(error);
        }
    }

    const handleChannelCheckboxChange = (event: ChangeEvent<HTMLInputElement>) => {
        const channelName = event.target.name;
        let newSelectedChannels: Channel[] = selectedChannels;
        const channel = channels.find((selectedChannel: Channel) => selectedChannel.channelName === channelName)
        if (!channel) {
            throw new Error('The channel associated with the checkbox could not be found.')
        }
        if (selectedChannels.includes(channel)) {
            const channelIndex = selectedChannels.indexOf(channel)
            newSelectedChannels.splice(channelIndex, 1);
        } else {
            newSelectedChannels.push(channel)
        }
        setSelectedChannels(newSelectedChannels);
        setSelectedChannelsError((newSelectedChannels.length < 1) || (newSelectedChannels.length > 5));
    }

    useEffect(() => {
        const fetchChannels = () => {
            try {
                if (selectedSeason) {
                    console.log(selectedSeason)
                    const channelsData = selectedSeason?.channels;
                    if (!channelsData) {
                        throw new Error('Could not find channel data');
                    }
                    channelsData.sort((a: Channel, b: Channel) => a.channelName.localeCompare(b.channelName, undefined, { numeric: true, sensitivity: 'base' }));
                    setChannels(channelsData);
                }
            } catch (err) {
                console.log(err);
            }
        };
        fetchChannels();
    }, [selectedSeason])

    // TODO: Implement flow for unauthenticated users
    return (
        <AuthenticatedTemplate>
            <BackgroundPaper>
                <form style={{ width: '400px', padding: '20px' }}>
                    <TextField
                        required
                        id='outline-required'
                        label='Playlist Title'
                        defaultValue={playlistTitle}
                        onChange={e => setPlaylistTitle(e.target.value)}
                    />
                    <div id='select-container'>
                        <SeriesSelect
                            seriesList={seriesList}
                            selectedSeries={selectedSeries}
                            onSeriesChange={handleSeriesChange}
                        />
                        <SeasonSelect
                            seasons={seasons}
                            selectedSeason={selectedSeason}
                            onSeasonChange={handleSeasonChange}
                        />
                    </div>
                    {channels && (
                        <ChannelForm channels={channels} onChange={handleChannelCheckboxChange} error={selectedChannelsError}/>
                    )}
                    <Button  color='secondary' variant="contained" style={{ borderRadius: '8px' }} type="submit" onClick={handleSubmit}>
                        Submit
                    </Button>
                </form>
            </BackgroundPaper>
        </AuthenticatedTemplate>
    );
}

export default PlaylistInputForm;