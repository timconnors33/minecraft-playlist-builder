import { Card, CardContent, Link, Typography } from "@mui/material";
import { Video } from "../../types/api";

interface Props {
    video: Video;
}

function VideoCard({video} : Props) {
    return (
        <Card sx={{display: 'flex'}}>
            <CardContent>
                <Link gutterBottom variant="h5" href={`https://www.youtube.com/watch?v=${video.videoYouTubeId}`} color="inherit">
                    {video.videoTitle}
                </Link>
                <Typography variant="body2" sx={{color: 'text.secondary', textAlign: 'start'}}>
                    {video.channelName}
                </Typography>
            </CardContent>
        </Card>
    )
}

export default VideoCard;