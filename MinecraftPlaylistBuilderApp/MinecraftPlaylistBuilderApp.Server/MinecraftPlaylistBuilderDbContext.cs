using Microsoft.EntityFrameworkCore;
using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server
{
    public class MinecraftPlaylistBuilderDbContext : DbContext
    {
        public MinecraftPlaylistBuilderDbContext(DbContextOptions<MinecraftPlaylistBuilderDbContext> options)
            : base(options)
        {
        }
        public DbSet<Series> Series { get; set; }
        public DbSet<Season> Seasons { get; set; }
    }
}
