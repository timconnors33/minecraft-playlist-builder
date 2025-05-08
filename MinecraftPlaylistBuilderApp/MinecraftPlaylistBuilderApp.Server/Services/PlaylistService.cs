using MinecraftPlaylistBuilderApp.Server.Dtos;
using MinecraftPlaylistBuilderApp.Server.Interfaces;
using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Services
{
    public class PlaylistService : IPlaylistService
    {
        private readonly IPlaylistRepository _playlistRepository;
        private readonly ISeasonRepository _seasonRepository;

        public PlaylistService(IPlaylistRepository playlistRepository, ISeasonRepository seasonRepository)
        {
            _playlistRepository = playlistRepository;
            _seasonRepository = seasonRepository;
        }

        // These two methods are currently the same, but should there be the capability
        // to share playlists in the future, they might be different.
        private bool isAuthorizedToRead(Guid userId, Guid playlistId)
        {
            return (userId == playlistId);
        }

        private bool isAuthorizedToWrite(Guid userId, Guid playlistId)
        {
            return (userId == playlistId);
        }

        public async Task<PlaylistDto> CreatePlaylistAsync(CreatePlaylistDto CreatePlaylistDto, Guid userId)
        {
            var playlist = new Playlist();
            playlist.OwnerId = userId;
            playlist.PublicPlaylistId = Guid.NewGuid();
            playlist.PlaylistTitle = CreatePlaylistDto.PlaylistTitle;
            var playlistSeason = await _seasonRepository.GetSeasonBySeasonSeriesTitlesAsync(CreatePlaylistDto.SeriesTitle, CreatePlaylistDto.SeasonTitle);
            if (playlistSeason == null)
            {
                return null;
            }
            playlist.SeasonId = playlistSeason.SeasonId;

            var createdPlaylist = await _playlistRepository.CreatePlaylistAsync(playlist);
            if (createdPlaylist == null)
            {
                return null;
            }

            return new PlaylistDto(createdPlaylist.PublicPlaylistId, createdPlaylist.PlaylistTitle);
        }

        public async Task<bool> DeletePlaylistAsync(Guid userId, Guid playlistId)
        {
            // TODO: Differentiate between not having read privileges and playlist not existing (not found)
            // and having read privileges and no write privileges (forbidden)
            if (!isAuthorizedToRead(userId, playlistId) || !isAuthorizedToWrite(userId, playlistId))
            {
                return false;
            }

            return await _playlistRepository.DeletePlaylistAsync(playlistId);
        }

        public async Task<List<PlaylistDto>> GetAllAsync(Guid userId)
        {
            var playlistDtos = new List<PlaylistDto>();
            // TODO: Check for authorization here (and getting single playlist), or is it unnecessary?
            var playlists = await _playlistRepository.GetAllByOwnerAsync(userId);
            foreach (var playlist in playlists)
            {
                var playlistDto = new PlaylistDto(playlist.PublicPlaylistId, playlist.PlaylistTitle);
                playlistDtos.Add(playlistDto);
            }
            return playlistDtos;
        }

        public async Task<PlaylistDto> GetPlaylistAsync(Guid playlistId, Guid userId)
        {
            var playlist = await _playlistRepository.GetPlaylistAsync(playlistId);

            if (playlist == null || !isAuthorizedToRead(userId, playlistId) || !isAuthorizedToWrite(userId, playlistId))
            {
                return null;
            }

            var playlistDto = new PlaylistDto(playlist.PublicPlaylistId, playlist.PlaylistTitle);
            return playlistDto;
        }

        public async Task<PlaylistDto> UpdatePlaylistAsync(UpdatePlaylistDto updatePlaylistDto, Guid userId, Guid playlistId)
        {
            if (!isAuthorizedToRead(userId, playlistId) || !isAuthorizedToWrite(userId, playlistId))
            {
                return null;
            }
            var playlistToUpdate = await _playlistRepository.GetPlaylistAsync(playlistId);
            if (playlistToUpdate == null)
            {
                return null;
            }

            playlistToUpdate.PlaylistTitle = updatePlaylistDto.PlaylistTitle;

            // TODO: Safe to return direct data from database entity? Check for any potential vulnerabilities
            var updatedPlaylist = await _playlistRepository.UpdatePlaylistAsync(playlistId, playlistToUpdate);
            var updatedPlaylistDto = new PlaylistDto(updatedPlaylist.PublicPlaylistId, updatedPlaylist.PlaylistTitle);

            return updatedPlaylistDto;
        }
    }
}
