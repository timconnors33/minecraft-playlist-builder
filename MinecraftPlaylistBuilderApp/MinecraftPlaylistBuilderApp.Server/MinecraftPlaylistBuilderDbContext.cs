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
        public DbSet<Channel> Channels { get; set; }
        public DbSet<SeasonAppearance> SeasonAppearances { get; set; }
    }
}
