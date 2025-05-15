import { Card, CardContent, Link, Typography } from "@mui/material";
import { Playlist } from "../../types/api";
import DOMPurify from "dompurify";

interface Props {
    playlist: Playlist;
}

function PlaylistCard({playlist} : Props) {
    return (
        <Card sx={{display: 'flex', width: '700px'}}>
            <CardContent>
                <Link gutterBottom variant="h6" href={`https://youtu.be/B8-ZmuJixIg?si=iGwWVlt42EplNGgP`} color="inherit" sx={{display:'flex', alignItems: 'start', textAlign: 'start'}}>
                    {DOMPurify.sanitize(playlist.playlistTitle)}
                </Link>
                <Typography variant="body2" sx={{color: 'text.secondary', textAlign: 'start'}}>
                    {DOMPurify.sanitize(playlist.seriesTitle)}
                </Typography>
                <Typography variant="body2" sx={{color: 'text.secondary', textAlign: 'start'}}>
                    {DOMPurify.sanitize(playlist.seasonTitle)}
                </Typography>
            </CardContent>
        </Card>
    )
}

export default PlaylistCard;