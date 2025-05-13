using Microsoft.EntityFrameworkCore;
using MinecraftPlaylistBuilderApp.Server.Interfaces;
using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Repositories
{
    public class PlaylistRepository : IPlaylistRepository
    {
        private readonly MinecraftPlaylistBuilderDbContext _context;

        public PlaylistRepository(MinecraftPlaylistBuilderDbContext context)
        {
            _context = context;
        }

        public async Task<Playlist> CreatePlaylistAsync(Playlist playlist)
        {
            _context.Playlists.Add(playlist);
            await _context.SaveChangesAsync();
            return playlist;
        }

        public async Task<bool> DeletePlaylistAsync(Guid playlistId)
        {
            var playlist = await _context.Playlists.FindAsync(playlistId);
            if (playlist == null)
            {
                return false;
            }
            var removedPlaylist = _context.Playlists.Remove(playlist);
            await _context.SaveChangesAsync();
            // TODO: Is this if statement necessary? If so, should it go before or after saving changes?
            if (removedPlaylist == null)
            {
                return false;
            }
            return true;
        }

        public async Task<List<Playlist>> GetAllByOwnerAsync(Guid ownerId)
        {
            var playlists = await _context.Playlists.Where(playlist => playlist.PublicPlaylistId == ownerId).ToListAsync();
            return playlists;
        }

        public async Task<Playlist> GetPlaylistAsync(Guid playlistId)
        {
            var playlist = await _context.Playlists.SingleOrDefaultAsync(playlist => playlist.PublicPlaylistId == playlistId);
            return playlist;
        }

        public async Task<Playlist> UpdatePlaylistAsync(Guid playlistId, Playlist newPlaylist)
        {
            var playlistToUpdate = await _context.Playlists.SingleOrDefaultAsync(playlist => playlist.PublicPlaylistId == playlistId);
            if (playlistToUpdate == null)
            {
                return null;
            }
            playlistToUpdate = newPlaylist;
            return playlistToUpdate;
        }
    }
}
