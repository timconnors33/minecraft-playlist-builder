import { Card, CardContent, FormControlLabel, FormGroup, Link, Typography } from "@mui/material";
import { PlaylistVideo } from "../../types/api";
import DOMPurify from "dompurify";
import Checkbox from '@mui/material/Checkbox';
import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import useFetchWithMsal from "../../utils/useFetchWithMsal";
import { protectedResources } from "../../utils/authConfig";
import { UUID } from "crypto";

interface Props {
    playlistId: UUID;
    playlistVideo: PlaylistVideo;
}

function PlaylistVideoCard({ playlistId, playlistVideo }: Props) {

    const { error, execute } = useFetchWithMsal({ scopes: [protectedResources.playlistApi.scopes.write] });
    const queryClient = useQueryClient();


    const [isWatched, setIsWatched] = useState<boolean>(playlistVideo.isWatched);

    const handleIsWatchedChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
        setIsWatched(event.target.checked);
        await editIsWatchedMn.mutateAsync(event.target.checked);
    }
    const editIsWatchedMn = useMutation({
            mutationKey: ['playlistVideos', playlistVideo.publicPlaylistVideoId],
            mutationFn: async (isWatchedVal: boolean) => {
                // TODO: Ok to build uri like this? 
                return await execute('PUT', `${protectedResources.playlistApi.endpoint}/${playlistId}/playlistVideos/${playlistVideo.publicPlaylistVideoId}`, {isWatched: isWatchedVal});
            },
            onSuccess: () => {
                // TODO: Use publicPlaylistVideoId in queryKey here too?
                queryClient.invalidateQueries({ queryKey: ['playlistVideos'] });
            },
            onError: () => {
                console.log('Error editing playlist video');
            }
        });

    return (
        <Card sx={{ width: '700px' }}>
            <CardContent>
                <div style={{ display: "flex", justifyContent: 'space-between' }}>
                    <div>
                        <Link gutterBottom variant="h6" href={`https://www.youtube.com/watch?v=${playlistVideo.videoYouTubeId}`} color="inherit" sx={{ display: 'flex', alignItems: 'start', textAlign: 'start' }}>
                            {DOMPurify.sanitize(playlistVideo.videoTitle)}
                        </Link>
                        <Typography variant="body2" sx={{ color: 'text.secondary', textAlign: 'start' }}>
                            <div>
                                {DOMPurify.sanitize(playlistVideo.channelName)}
                            </div>
                            <div>
                                {DOMPurify.sanitize(
                                    // TODO: toLocaleDateString or toDateString?
                                    new Date(playlistVideo.videoPublishedAt).toLocaleDateString())
                                }
                            </div>
                        </Typography>
                    </div>
                    <div style={{ display: "flex", flexDirection: 'column', justifyContent: 'center' }}>
                        <FormGroup>
                            <FormControlLabel control={<Checkbox checked={isWatched} onChange={handleIsWatchedChange}/>} label="Watched?" labelPlacement="top"/>
                        </FormGroup>
                    </div>
                </div>
            </CardContent>
        </Card>
    )
}

export default PlaylistVideoCard;