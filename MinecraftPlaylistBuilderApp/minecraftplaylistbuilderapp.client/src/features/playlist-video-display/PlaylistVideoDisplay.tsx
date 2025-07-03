import { Playlist, PlaylistVideo, Video } from "../../types/api";
import PlaylistVideoCard from "./PlaylistVideoCard";
import { useEffect, useMemo, useState } from "react";
import PaginatedList from "../../components/PaginatedList";
import useFetchWithMsal from "../../utils/useFetchWithMsal";
import { protectedResources } from "../../utils/authConfig";
import { useQuery } from "@tanstack/react-query";
import { CircularProgress, Divider, FormControl, FormHelperText, MenuItem, Select, SelectChangeEvent } from "@mui/material";
import { UUID } from "crypto";
import { useParams } from "react-router";
import { BackgroundPaper } from "../../components/BackgroundPaper";
import LoadingOverlay from "../../components/LoadingOverlay";
import { useMsal } from "@azure/msal-react";

type Params = {
    playlistId: UUID
}

function PlaylistVideoDisplay() {

    const tokenRequest = {
        scopes: [protectedResources.playlistVideoApi.scopes.read,
        protectedResources.playlistVideoApi.scopes.write
        ]
    }

    const { instance } = useMsal();

    const { error, execute, result } = useFetchWithMsal({ scopes: [protectedResources.playlistVideoApi.scopes.read] });

    const { playlistId } = useParams<Params>()

    const [filterType, setFilterType] = useState<string>('all');
    const [filteredPlaylistVideos, setFilteredPlaylistVideos] = useState<PlaylistVideo[]>([]);

    // TODO: Optimistically update the playlist video counts when the watched value is edited.
    const {
        data: playlistVideos = [],
        isLoading,
        isError,
        error: queryError,
    } = useQuery({
        queryKey: ['playlistVideos'],
        queryFn: async () => {
            // TODO: I really don't like the string concatenation here
            return await execute('GET', `${protectedResources.playlistApi.endpoint}/${playlistId}/playlistVideos`, null);
        },
        enabled: !!result,
    });

    useEffect(() => {
        switch (filterType) {
            case 'watched':
                setFilteredPlaylistVideos(playlistVideos.filter((playlistVideo) => playlistVideo.isWatched));
                break;
            case 'unwatched':
                setFilteredPlaylistVideos(playlistVideos.filter((playlistVideo) => playlistVideo.isWatched == false));
                break;
            default:
                setFilteredPlaylistVideos(playlistVideos);
                break;
        }
    }, [filterType, playlistVideos])

    useEffect(() => {
        const getToken = async () => {
            const account = instance.getActiveAccount();
            if (account) {
                const tokenResponse = await instance.acquireTokenSilent({
                    ...tokenRequest,
                });
            }
        };
        getToken();
    }, [instance])

    const handleFilterChange = (event: SelectChangeEvent) => {
        setFilterType(event.target.value);
    }

    // TODO: Purify id? Check here and in VideoCard module
    const playlistVideoCards = useMemo(() => {
        console.log(playlistVideos);
        // TODO: Change so I only have to sort this once
        filteredPlaylistVideos.sort((a: PlaylistVideo, b: PlaylistVideo) => new Date(a.videoPublishedAt).getTime() - new Date(b.videoPublishedAt).getTime());
        return filteredPlaylistVideos.map((playlistVideo: PlaylistVideo) => (
            <PlaylistVideoCard key={playlistVideo.videoYouTubeId} playlistId={playlistId} playlistVideo={playlistVideo} />
        ))
    }, [filteredPlaylistVideos])

    if (isLoading) { return <LoadingOverlay />; }

    if (isError) {
        console.log(queryError);
        return <div>Error loading playlist videos.</div>;
    }

    return (
        <BackgroundPaper>
            <h1>Playlist Videos</h1>
            <Divider />
            {playlistVideoCards !== null &&
                <>
                    <FormControl>
                        <FormHelperText>Filter Videos</FormHelperText>
                        <Select
                            id='playlist-video-filter'
                            label='Filter Videos'
                            onChange={handleFilterChange}
                            defaultValue="all"
                            value={filterType}
                        >
                            <MenuItem value='all'>All ({playlistVideos.length})</MenuItem>
                            <MenuItem value='unwatched'>Unwatched ({(playlistVideos.filter((playlistVideo) => playlistVideo.isWatched == false)).length})</MenuItem>
                            <MenuItem value='watched'>Watched ({(playlistVideos.filter((playlistVideo) => playlistVideo.isWatched)).length})</MenuItem>

                        </Select>
                    </FormControl>
                    <PaginatedList children={playlistVideoCards} />
                </>}
        </BackgroundPaper>
    )
}

export default PlaylistVideoDisplay;