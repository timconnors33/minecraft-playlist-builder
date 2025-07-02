using MinecraftPlaylistBuilderApp.Server.Dtos;
using MinecraftPlaylistBuilderApp.Server.Interfaces;
using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Services
{
    public class PlaylistVideoService : IPlaylistVideoService
    {
        private readonly IPlaylistVideoRepository _playlistVideoRepository;
        private readonly IPlaylistRepository _playlistRepository;
        private readonly IVideoRepository _videoRepository;

        public PlaylistVideoService(IPlaylistVideoRepository playlistVideoRepository, IPlaylistRepository playlistRepository, IVideoRepository videoRepository)
        {
            _playlistVideoRepository = playlistVideoRepository;
            _playlistRepository = playlistRepository;
            _videoRepository = videoRepository;
        }

        // TODO: Abstract this to shared resource
        private async Task<bool> isAuthorizedToRead(Guid userId, Guid playlistId)
        {
            return (userId == await GetPlaylistOwnerAsync(playlistId));
        }

        private async Task<bool> isAuthorizedToWrite(Guid userId, Guid playlistId)
        {
            return (userId == await GetPlaylistOwnerAsync(playlistId));
        }

        private async Task<Guid> GetPlaylistOwnerAsync(Guid playlistId)
        {
            return await _playlistRepository.GetPlaylistOwnerAsync(playlistId);
        }

        public async Task<List<PlaylistVideoDto>> CreatePlaylistVideosAsync(Guid userId, Guid playlistId, CreatePlaylistVideoDto createPlaylistVideoDto)
        {
            if (!await isAuthorizedToRead(userId, playlistId) || !await isAuthorizedToWrite(userId, playlistId))
            {
                return null;
            }
            // TODO: Add validation
            var playlist = await _playlistRepository.GetPlaylistAsync(playlistId);
            // TODO: Should probably change this method to use the ChannelYouTubeIds insteaad of the ChannelTitles at some point
            var videos = await _videoRepository.GetVideosBySeriesSeasonChannelsAsync(playlist.Season.Series.SeriesTitle, playlist.Season.SeasonTitle, createPlaylistVideoDto.ChannelNames);
            List<PlaylistVideoDto> playlistVideoDtos = [];
            foreach (var video in videos)
            {
                var playlistVideo = new PlaylistVideo();
                playlistVideo.Playlist = playlist;
                playlistVideo.PlaylistId = playlist.PlaylistId;
                playlistVideo.Video = video;
                playlistVideo.VideoId = video.VideoId;
                playlistVideo.IsWatched = false;
                playlistVideo.PublicPlaylistVideoId = Guid.NewGuid();
                
                var createdPlaylistVideo = await _playlistVideoRepository.CreatePlaylistVideoAsync(playlistVideo);
                if (createdPlaylistVideo != null)
                {
                    playlistVideoDtos.Add(new PlaylistVideoDto
                        (
                            createdPlaylistVideo.PublicPlaylistVideoId, 
                            createdPlaylistVideo.Video.VideoTitle, 
                            createdPlaylistVideo.Video.VideoYouTubeId, 
                            playlistVideo.IsWatched,
                            playlistVideo.Video.SeasonAppearance.Channel.ChannelName,
                            playlistVideo.Video.VideoPublishedAt
                        )
                    );
                }    
            }
            return playlistVideoDtos;
        }

        public async Task<bool> DeletePlaylistVideoAsync(Guid userId, Guid playlistId, Guid playlistVideoId)
        {
            // TODO: Differentiate between not having read privileges and playlist not existing (not found)
            // and having read privileges and no write privileges (forbidden)
            if (!await isAuthorizedToRead(userId, playlistId) || !await isAuthorizedToWrite(userId, playlistId))
            {
                return false;
            }

            await _playlistVideoRepository.DeletePlaylistVideoAsync(playlistVideoId);
            return true;
        }

        public async Task<PlaylistVideoDto> GetPlaylistVideoByIdAsync(Guid userId, Guid playlistId, Guid playlistVideoId)
        {
            if (!await isAuthorizedToRead(userId, playlistId))
            {
                return null;
            }
            var playlistVideo = await _playlistVideoRepository.GetPlaylistVideoByIdAsync(playlistVideoId);
            if (playlistVideo == null)
            {
                return null;
            }
            return new PlaylistVideoDto
                        (
                            playlistVideo.PublicPlaylistVideoId,
                            playlistVideo.Video.VideoTitle,
                            playlistVideo.Video.VideoYouTubeId,
                            playlistVideo.IsWatched,
                            playlistVideo.Video.SeasonAppearance.Channel.ChannelName,
                            playlistVideo.Video.VideoPublishedAt
                        );
        }

        public async Task<List<PlaylistVideoDto>> GetPlaylistVideosByPlaylistIdAsync(Guid userId, Guid playlistId)
        {
            if (!await isAuthorizedToRead(userId, playlistId))
            {
                return null;
            }
            var playlistVideos = await _playlistVideoRepository.GetPlaylistVideosByPlaylistIdAsync(playlistId);
            List<PlaylistVideoDto> playlistVideoDtos = [];
            foreach (var playlistVideo in playlistVideos)
            {
                playlistVideoDtos.Add(new PlaylistVideoDto
                        (
                            playlistVideo.PublicPlaylistVideoId,
                            playlistVideo.Video.VideoTitle,
                            playlistVideo.Video.VideoYouTubeId,
                            playlistVideo.IsWatched,
                            playlistVideo.Video.SeasonAppearance.Channel.ChannelName,
                            playlistVideo.Video.VideoPublishedAt
                        )
                );
            }

            return playlistVideoDtos;
        }

        public async Task<PlaylistVideoDto> UpdatePlaylistVideoAsync(Guid userId, Guid playlistId, Guid playlistVideoId, UpdatePlaylistVideoDto updatePlaylistVideoDto)
        {
            if (!await isAuthorizedToRead(userId, playlistId) || !await isAuthorizedToWrite(userId, playlistId))
            {
                return null;
            }

            var playlistVideoToUpdate = await _playlistVideoRepository.GetPlaylistVideoByIdAsync(playlistVideoId);
            if (playlistVideoToUpdate == null)
            {
                return null;
            }

            playlistVideoToUpdate.IsWatched = updatePlaylistVideoDto.IsWatched;
            var updatedPlaylistVideo = await _playlistVideoRepository.UpdatePlaylistVideoAsync(playlistVideoId, playlistVideoToUpdate);
            return new PlaylistVideoDto
                (
                updatedPlaylistVideo.PublicPlaylistVideoId, 
                updatedPlaylistVideo.Video.VideoTitle, 
                updatedPlaylistVideo.Video.VideoYouTubeId, 
                updatedPlaylistVideo.IsWatched, 
                updatedPlaylistVideo.Video.SeasonAppearance.Channel.ChannelName,
                updatedPlaylistVideo.Video.VideoPublishedAt
                );
        }
    }
}
