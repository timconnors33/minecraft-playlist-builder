import { useLocation } from "react-router";
import { Video } from "../../types/api";
import VideoCard from "./VideoCard";

function PlaylistDisplay() {

    const location = useLocation();
    const videos: Video[] = location.state?.videos;

    console.log(videos);

    return (
        <div>
            <h1>Playlist Videos</h1>
            <div style={{display: 'flex', flexDirection: 'column', gap: '5px'}}>
                {videos.length > 0 ? (
                    videos.map((video) => (
                        <VideoCard key={video.videoYouTubeId} video={video}/>
                    ))
                ) : (
                    <p>No videos found.</p>
                )}
            </div>
        </div>
    )
}

export default PlaylistDisplay;