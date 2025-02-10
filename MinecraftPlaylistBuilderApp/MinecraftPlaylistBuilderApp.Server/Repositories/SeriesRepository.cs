using Microsoft.EntityFrameworkCore;
using MinecraftPlaylistBuilderApp.Server.Interfaces;
using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Repositories
{
    public class SeriesRepository : ISeriesRepository
    {
        private readonly MinecraftPlaylistBuilderDbContext _context;

        public SeriesRepository(MinecraftPlaylistBuilderDbContext context)
        {
            _context = context;
        }

        public async Task<ICollection<Series>> GetAllSeriesAsync()
        {
            return (await _context.Series.ToListAsync());
        }
    }
}
