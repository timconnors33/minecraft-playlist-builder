import { Card, CardContent, Link, Typography } from "@mui/material";
import { Video } from "../../types/api";
import DOMPurify from "dompurify";

interface Props {
    video: Video;
}

function VideoCard({video} : Props) {
    return (
        <Card sx={{display: 'flex', width: '700px'}}>
            <CardContent>
                <Link gutterBottom variant="h6" href={`https://www.youtube.com/watch?v=${video.videoYouTubeId}`} color="inherit" sx={{display:'flex', alignItems: 'start', textAlign: 'start'}}>
                    {DOMPurify.sanitize(video.videoTitle)}
                </Link>
                <Typography variant="body2" sx={{color: 'text.secondary', textAlign: 'start'}}>
                    {DOMPurify.sanitize(video.channelName)}
                </Typography>
            </CardContent>
        </Card>
    )
}

export default VideoCard;