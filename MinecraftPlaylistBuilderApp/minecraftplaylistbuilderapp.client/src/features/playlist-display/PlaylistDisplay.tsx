import { Playlist } from "../../types/api";
import PlaylistCard from "./PlaylistCard";
import { useEffect, useState, useMemo} from "react";
import PaginatedList from "../../components/PaginatedList";
import useFetchWithMsal from "../../utils/useFetchWithMsal";
import { protectedResources } from "../../utils/authConfig";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { CircularProgress } from "@mui/material";

function PlaylistDisplay() {

    const { error, execute, result } = useFetchWithMsal({ scopes: [protectedResources.playlistApi.scopes.read] });

    const {
        data: playlists = [],
        isLoading,
        isError,
        error: queryError,
    } = useQuery({
        queryKey: ['playlists'],
        queryFn: async () => {
            return await execute('GET', protectedResources.playlistApi.endpoint, null);
        },
        enabled: !!result,
    });

    const playlistCards = useMemo(() => {
        console.log(playlists);
        return playlists.map((playlist) => (
            <PlaylistCard key={playlist.playlistId} playlist={playlist}/>
        ));
    }, [playlists]);

    if (isLoading) { return <CircularProgress />; }

    if (isError) {
        console.log(queryError);
        return <div>Error loading playlists.</div>;
    }

    return (
        <div>
            <h1>Playlists</h1>
            {playlistCards !== null && <PaginatedList children={playlistCards} />}
        </div>
    )
}

export default PlaylistDisplay;