using MinecraftPlaylistBuilderApp.Server.Dtos;
using MinecraftPlaylistBuilderApp.Server.Interfaces;
using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Services
{
    public class VideoService : IVideoService
    {
        private readonly IVideoRepository _videoRepository;

        public VideoService(IVideoRepository videoRepository)
        {
            _videoRepository = videoRepository;
        }
        public async Task<List<VideoDto>> GetVideosBySeriesSeasonChannelAsync(string seriesTitle, string seasonTitle, string channelName)
        {
            var videos = await _videoRepository.GetVideosBySeriesSeasonChannelAsync(seriesTitle, seasonTitle, channelName);
            if (videos == null)
            {
                return [];
            }

            var videosInTimeOrder = videos.OrderBy(video => video.VideoPublishedAt);

            List<VideoDto> videoDtos = new List<VideoDto>();
            foreach (var video in videosInTimeOrder)
            {
                videoDtos.Add(new VideoDto(video.VideoTitle, video.VideoYouTubeId, video.VideoThumbnailUri));
            }

            return videoDtos;
        }
    }
}
