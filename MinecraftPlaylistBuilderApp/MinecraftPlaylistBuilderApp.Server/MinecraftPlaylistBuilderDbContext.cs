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

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseLazyLoadingProxies();
        }
        public DbSet<Series> Series { get; set; }
        public DbSet<Season> Seasons { get; set; }
        public DbSet<Channel> Channels { get; set; }
        public DbSet<SeasonAppearance> SeasonAppearances { get; set; }
        public DbSet<Video> Videos { get; set; }
        public DbSet<Playlist> Playlists { get; set; }
    }
}
