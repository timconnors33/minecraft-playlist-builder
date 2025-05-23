import { Button, Card, CardContent, Link, Typography } from "@mui/material";
import { Playlist } from "../../types/api";
import DOMPurify from "dompurify";
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import useFetchWithMsal from "../../utils/useFetchWithMsal";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { protectedResources } from "../../utils/authConfig";
import { UUID } from "crypto";

interface Props {
    playlist: Playlist;
}

function PlaylistCard({ playlist }: Props) {

    const { error, execute } = useFetchWithMsal({ scopes: protectedResources.playlistApi.scopes.write });
    const queryClient = useQueryClient();

    // TODO: Add payload to mutation key?
    const deletePlaylistMn = useMutation({
            mutationKey: ['createPlaylists'],
            mutationFn: async (playlistId: UUID) => {
                // TODO: Ok to build uri like this? 
                return await execute('DELETE', `${protectedResources.playlistApi.endpoint}/${playlistId}`, null);},
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['playlists']});
            },
            onError: () => {
                console.log('Error deleting playlist');
            }
        });

    const deletePlaylist = async () => {
        await deletePlaylistMn.mutateAsync(playlist.publicPlaylistId);
    }

    // TODO: Need to make card element flexbox?
    return (
        <Card sx={{ width: '700px' }}>
            <CardContent>
                <div style={{ display: "flex", justifyContent: 'space-between' }}>
                    <div>
                        <Link gutterBottom variant="h6" href={`https://youtu.be/B8-ZmuJixIg?si=iGwWVlt42EplNGgP`} color="inherit" sx={{ display: 'flex', alignItems: 'start', textAlign: 'start' }}>
                            {DOMPurify.sanitize(playlist.playlistTitle)}
                        </Link>
                        <Typography variant="body2" sx={{ color: 'text.secondary', textAlign: 'start' }}>
                            {DOMPurify.sanitize(playlist.seriesTitle)}
                        </Typography>
                        <Typography variant="body2" sx={{ color: 'text.secondary', textAlign: 'start' }}>
                            {DOMPurify.sanitize(playlist.seasonTitle)}
                        </Typography>
                    </div>
                    <div style={{ display: "flex", flexDirection: 'column', justifyContent: 'space-between'}}>
                        <Button>
                            <EditIcon/>
                        </Button>
                        <Button onClick={deletePlaylist}>
                            <DeleteIcon/>
                        </Button>
                    </div>
                </div>
            </CardContent>
        </Card>
    )
}

export default PlaylistCard;