import { Card, CardContent, Link, Typography } from "@mui/material";
import { PlaylistVideo } from "../../types/api";
import DOMPurify from "dompurify";

interface Props {
    playlistVideo: PlaylistVideo;
}

function PlaylistVideoCard({playlistVideo} : Props) {

    return (
        <Card sx={{display: 'flex', width: '700px'}}>
            <CardContent>
                <Link gutterBottom variant="h6" href={`https://www.youtube.com/watch?v=${playlistVideo.videoYouTubeId}`} color="inherit" sx={{display:'flex', alignItems: 'start', textAlign: 'start'}}>
                    {DOMPurify.sanitize(playlistVideo.videoTitle)}
                </Link>
                <Typography variant="body2" sx={{color: 'text.secondary', textAlign: 'start'}}>
                    {DOMPurify.sanitize(playlistVideo.channelName)}
                </Typography>
            </CardContent>
        </Card>
    )
}

export default PlaylistVideoCard;