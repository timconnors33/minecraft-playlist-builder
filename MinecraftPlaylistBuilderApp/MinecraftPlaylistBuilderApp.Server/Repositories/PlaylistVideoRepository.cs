using Microsoft.EntityFrameworkCore;
using MinecraftPlaylistBuilderApp.Server.Interfaces;
using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Repositories
{
    public class PlaylistVideoRepository : IPlaylistVideoRepository
    {
        private readonly MinecraftPlaylistBuilderDbContext _context;

        public PlaylistVideoRepository(MinecraftPlaylistBuilderDbContext context)
        {
            _context = context;
        }

        public async Task<PlaylistVideo> CreatePlaylistVideoAsync(PlaylistVideo playlistVideo)
        {
            _context.PlaylistVideos.Add(playlistVideo);
            await _context.SaveChangesAsync();
            return playlistVideo;
        }

        public async Task<bool> DeletePlaylistVideoAsync(Guid playlistVideoId)
        {
            var playlistVideo = await GetPlaylistVideoByIdAsync(playlistVideoId);
            if (playlistVideo == null)
            {
                return false;
            }
            var removedPlaylistVideo = _context.PlaylistVideos.Remove(playlistVideo);
            await _context.SaveChangesAsync();
            // TODO: Is this if statement necessary? If so, should it go before or after saving changes?
            if (removedPlaylistVideo == null)
            {
                return false;
            }
            return true;
        }

        public async Task<PlaylistVideo> GetPlaylistVideoByIdAsync(Guid publicPlaylistVideoId)
        {
            var playlistVideo = await _context.PlaylistVideos.SingleOrDefaultAsync(playlistVideo => playlistVideo.PublicPlaylistVideoId == publicPlaylistVideoId);
            return playlistVideo;
        }

        public async Task<List<PlaylistVideo>> GetPlaylistVideosByPlaylistIdAsync(Guid publicPlaylistId)
        {
            var playlistVideos = await _context.PlaylistVideos.Where(playlistVideos => playlistVideos.Playlist.PublicPlaylistId == publicPlaylistId).ToListAsync();
            return playlistVideos;
        }

        public async Task<PlaylistVideo> UpdatePlaylistVideoAsync(Guid playlistVideoId, PlaylistVideo newPlaylistVideo)
        {
            var playlistVideoToUpdate = await _context.PlaylistVideos.SingleOrDefaultAsync(playlistVideo => playlistVideo.PublicPlaylistVideoId == playlistVideoId);
            if (playlistVideoToUpdate == null)
            {
                return null;
            }
            playlistVideoToUpdate = newPlaylistVideo;
            await _context.SaveChangesAsync();
            return playlistVideoToUpdate;
        }
    }
}
