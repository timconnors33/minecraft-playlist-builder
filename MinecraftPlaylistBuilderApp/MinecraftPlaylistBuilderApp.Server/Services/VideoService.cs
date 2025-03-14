using MinecraftPlaylistBuilderApp.Server.Dtos;
using MinecraftPlaylistBuilderApp.Server.Interfaces;

namespace MinecraftPlaylistBuilderApp.Server.Services
{
    public class VideoService : IVideoService
    {
        private readonly IVideoRepository _videoRepository;

        public VideoService(IVideoRepository videoRepository)
        {
            _videoRepository = videoRepository;
        }
        public async Task<List<VideoDto>> GetVideosBySeriesSeasonChannelsAsync(string seriesTitle, string seasonTitle, string[] channelNames)
        {
            var videos = await _videoRepository.GetVideosBySeriesSeasonChannelsAsync(seriesTitle, seasonTitle, channelNames);
            if (videos == null)
            {
                return [];
            }

            var videosInTimeOrder = videos.OrderBy(video => video.VideoPublishedAt);

            List<VideoDto> videoDtos = new List<VideoDto>();
            foreach (var video in videosInTimeOrder)
            {
                videoDtos.Add(new VideoDto(video.VideoYouTubeId, video.VideoTitle, video.VideoThumbnailUri, video.SeasonAppearance.Channel.ChannelName));
            }

            return videoDtos;
        }
    }
}
