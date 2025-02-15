using Microsoft.EntityFrameworkCore;
using MinecraftPlaylistBuilderApp.Server.Interfaces;
using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Repositories
{
    public class SeasonAppearanceRepository : ISeasonAppearanceRepository
    {
        private readonly MinecraftPlaylistBuilderDbContext _context;

        public SeasonAppearanceRepository(MinecraftPlaylistBuilderDbContext context)
        {
            _context = context;
        }
        public async Task<List<SeasonAppearance>> GetAllSeasonAppearancesAsync()
        {
            return (await _context.SeasonAppearances.ToListAsync());
        }
    }
}
