import { Playlist } from "../../types/api";
import PlaylistCard from "./PlaylistCard";
import { useEffect, useState, useMemo} from "react";
import PaginatedList from "../../components/PaginatedList";
import useFetchWithMsal from "../../utils/useFetchWithMsal";
import { protectedResources } from "../../utils/authConfig";

function PlaylistDisplay() {

    const { error, execute, result } = useFetchWithMsal({ scopes: protectedResources.playlistApi.scopes.read });
    const [playlists, setPlaylists] = useState<Playlist[]>([]);

    useEffect(() => {
        if (!result) {
            return;
        }
        const fetchUserPlaylists = async () => {
            const response = await execute('GET', protectedResources.playlistApi.endpoint, null);
            console.log(response)
            if (response) {
                console.log('Fetched playlists');
                setPlaylists(response);
            } else {
                console.log("Error fetching playlists");
                console.log(error);
            }
        }

        fetchUserPlaylists();
    }, [result]);

    const playlistCards = useMemo(() => {
        console.log(playlists);
        return playlists.map((playlist) => (
            <PlaylistCard key={playlist.playlistId} playlist={playlist}/>
        ))
    }, [playlists])

    return (
        <div>
            <h1>Playlists</h1>
            {playlistCards !== null && <PaginatedList children={playlistCards} />}
        </div>
    )
}

export default PlaylistDisplay;