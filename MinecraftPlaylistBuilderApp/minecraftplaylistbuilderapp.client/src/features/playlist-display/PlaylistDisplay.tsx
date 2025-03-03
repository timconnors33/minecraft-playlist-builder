import { useLocation } from "react-router";
import { Video } from "../../types/api";

function PlaylistDisplay() {

    const location = useLocation();
    const videos: Video[] = location.state?.videos;

    console.log(videos);

    return (
        <div>
            <h1>Playlist Videos</h1>
            {videos.length > 0 ? (
                videos.map((video) => <p key={video.videoYouTubeId}>{video.videoTitle}</p>)
            ) : (
                <p>No videos found.</p>
            )}
        </div>
    )
}

export default PlaylistDisplay;