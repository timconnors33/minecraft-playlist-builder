import { Button, Card, CardContent, Link, Typography } from "@mui/material";
import { Playlist } from "../../types/api";
import DOMPurify from "dompurify";
import DeletePlaylistDialog from "../playlist-video-display/DeletePlaylistDialog";
import EditPlaylistDialog from "../playlist-video-display/EditPlaylistDialog";

interface Props {
    playlist: Playlist;
}

function PlaylistCard({ playlist }: Props) {

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
                        <EditPlaylistDialog playlistId={playlist.publicPlaylistId} currentTitle={playlist.playlistTitle}/>
                        <DeletePlaylistDialog playlistId={playlist.publicPlaylistId}/>
                    </div>
                </div>
            </CardContent>
        </Card>
    )
}

export default PlaylistCard;