import { useLocation } from "react-router";
import { Video } from "../../types/api";
import VideoCard from "./VideoCard";
import { ReactNode } from "react";
import PaginatedList from "../../components/PaginatedList";

function PlaylistVideoDisplay() {

    const location = useLocation();
    const videos: Video[] = location.state?.videos;
    const videoCards: ReactNode[] = [];
    videos.map((video) => (
        // TODO: Purify id? Check here and in VideoCard module
        videoCards.push(<VideoCard key={video.videoYouTubeId} video={video}/>)
    ))
    console.log(videos);

    return (
        <div>
            <h1>Playlist Videos</h1>
            <PaginatedList children={videoCards}/>
        </div>
    )
}

export default PlaylistVideoDisplay;