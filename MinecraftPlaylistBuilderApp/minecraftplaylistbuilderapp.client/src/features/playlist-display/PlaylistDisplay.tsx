import { useLocation } from "react-router";
import { Video } from "../../types/api";
import VideoCard from "./VideoCard";
import { useState } from "react";
import { Pagination } from "@mui/material";

function PlaylistDisplay() {

    const pageItemCount = 10;

    const [page, setPage] = useState(0);

    const location = useLocation();
    const videos: Video[] = location.state?.videos;
    console.log(videos);
    const pageCount = Math.ceil(videos.length / pageItemCount);

    const [pageVideos, setPageVideos] = useState(videos.slice(0, pageItemCount));

    const handlePageChange = (event: React.ChangeEvent<unknown>, page : number) => {
        setPage(page);
        setPageVideos(videos.slice((page - 1) * pageItemCount, Math.min(page * pageItemCount + 1, videos.length + 1)));
    }

    return (
        <div>
            <h1>Playlist Videos</h1>
            <div style={{display: 'flex', flexDirection: 'column', gap: '5px'}}>
                {pageVideos.length > 0 ? (
                    pageVideos.map((video) => (
                        // TODO: Purify id? Check here and in VideoCard module
                        <VideoCard key={video.videoYouTubeId} video={video}/>
                    ))
                ) : (
                    <p>No videos found.</p>
                )}
            </div>
            {videos.length > pageItemCount && (
                <Pagination sx={{display: 'flex', justifyContent: 'center'}} count={pageCount} page={page} onChange={handlePageChange}/>
            )}
        </div>
    )
}

export default PlaylistDisplay;