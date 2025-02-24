import { Button, Checkbox, FormControlLabel, FormGroup, FormHelperText, SelectChangeEvent } from "@mui/material";
import { useState, useEffect, SetStateAction, FormEvent, ChangeEvent } from "react";
import { Series, Season, Channel, SeasonAppearance, Video, GetVideosPayload } from "../../../types/api";
import SeasonSelect from "./SeasonSelect";
import SeriesSelect from "./SeriesSelect";
import '../PlaylistInputForm.css'
import ChannelCheckbox from "./ChannelCheckbox";

const BASE_URL = 'https://localhost:7258';
const DEV_OAUTH2_CLIENT_ID = import.meta.env.VITE_REACT_APP_DEV_OAUTH2_CLIENT_ID;

interface Props {
    seasonAppearance: SeasonAppearance;
}

const PlaylistInputForm = ({ seasonAppearance }: Props) => {
    const [seriesList, setSeriesList] = useState<Series[]>(seasonAppearance.series);
    // TODO: Check using undefined here
    const [selectedSeries, setSelectedSeries] = useState<Series>(seriesList[0]);

    const [seasons, setSeasons] = useState<Season[]>(selectedSeries.seasons);
    // TODO: Might want to order the seasons alphanumerically here as well, maybe also the series above
    const [selectedSeason, setSelectedSeason] = useState<Season>(seasons[0]);

    const [channels, setChannels] = useState<Channel[]>(selectedSeason.channels);
    const [selectedChannels, setSelectedChannels] = useState<Channel[]>([]);

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

    const youtubeAuthFlow = async (videos: Video[]) => {

        try {
            let tokenClient;
            let accessToken;
            const loadGapiClient = async () => {
                return new Promise((resolve, reject) => {
                    if (!window.gapi) {
                        reject(new Error("Google API not loaded"));
                        return;
                    }
                    window.gapi.load('client', { callback: resolve, onerror: reject });
                    console.log('Google API loaded');
                });
            };
            await loadGapiClient();
            await window.gapi.client.init({});
            await window.gapi.client.load('https://www.googleapis.com/discovery/v1/apis/youtube/v3/rest');

            tokenClient = window.google.accounts.oauth2.initTokenClient({
                client_id: DEV_OAUTH2_CLIENT_ID,
                scope: 'https://www.googleapis.com/auth/youtube',
                prompt: 'consent',
                callback: (tokenResponse) => {
                    if (tokenResponse && tokenResponse.access_token) {
                        createPlaylist();
                    } else {
                        console.log('Did not get access token');
                    }
                },
            });

            tokenClient.requestAccessToken();

        } catch (err) {
            console.log(err);
        }
    }

    const createPlaylist = async () => {

        const response = await window.gapi.client.youtube.playlists.insert({
            "part": [
                "snippet,contentDetails,status"
            ],
            "resource": {
                "snippet": {
                    "title": "Custom Minecraft Playlist"
                },
                "status": {
                    "privacyStatus": "private"
                }
            }
        });

        console.log(response);
    }

    const handleSubmit = async (event: FormEvent) => {
        event.preventDefault();
        const payload: GetVideosPayload = {
            seriesTitle: selectedSeries.seriesTitle,
            seasonTitle: selectedSeason.seasonTitle,
            channelNames: selectedChannels.map(channel => channel.channelName)
        }
        const videos: Video[] = await fetchVideos(payload);
        await youtubeAuthFlow(videos);
    }

    const fetchVideos = async (payload: GetVideosPayload): Promise<Video[]> => {
        console.log(JSON.stringify(payload));
        const response = await fetch(`${BASE_URL}/api/videos`, {
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

    return (
        <>
            <form>
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
                    <div>
                        <FormHelperText>Channels</FormHelperText>
                        <FormGroup id='channel-checkboxes' style={{ overflowX: 'hidden', overflowY: 'auto' }}>
                            {channels.map((channel) => (
                                <ChannelCheckbox
                                    channel={channel}
                                    onChange={handleChannelCheckboxChange}
                                    key={channel.channelName}
                                />
                            ))}
                        </FormGroup>
                    </div>
                )}
                <Button type="submit" onClick={handleSubmit}>
                    Submit
                </Button>
            </form>
        </>
    );
}

export default PlaylistInputForm;