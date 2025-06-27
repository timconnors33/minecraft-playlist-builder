import { Playlist, PlaylistVideo, Video } from "../../types/api";
import PlaylistVideoCard from "./PlaylistVideoCard";
import { useMemo } from "react";
import PaginatedList from "../../components/PaginatedList";
import useFetchWithMsal from "../../utils/useFetchWithMsal";
import { protectedResources } from "../../utils/authConfig";
import { useQuery } from "@tanstack/react-query";
import { CircularProgress } from "@mui/material";
import { UUID } from "crypto";
import { useParams } from "react-router";

type Params = {
    playlistId: UUID
}

function PlaylistVideoDisplay() {
    const { error, execute, result } = useFetchWithMsal({ scopes: [protectedResources.playlistVideoApi.scopes.read] });

    const {playlistId} = useParams<Params>()

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

    // TODO: Purify id? Check here and in VideoCard module
    const playlistVideoCards = useMemo(() => {
        console.log(playlistVideos);
        playlistVideos.sort((a: PlaylistVideo, b: PlaylistVideo) => new Date(a.videoPublishedAt).getTime() - new Date(b.videoPublishedAt).getTime());
        return playlistVideos.map((playlistVideo: PlaylistVideo) => (
            <PlaylistVideoCard key={playlistVideo.videoYouTubeId} playlistId={playlistId} playlistVideo={playlistVideo}/>
        ))
    })

    if (isLoading) { return <CircularProgress />; }

    if (isError) {
        console.log(queryError);
        return <div>Error loading playlist videos.</div>;
    }

    return (
        <div>
            <h1>Playlist Videos</h1>
            {playlistVideoCards !== null && <PaginatedList children={playlistVideoCards} />}
        </div>
    )
}

export default PlaylistVideoDisplay;