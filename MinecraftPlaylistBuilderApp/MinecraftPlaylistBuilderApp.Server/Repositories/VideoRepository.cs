using Microsoft.EntityFrameworkCore;
using MinecraftPlaylistBuilderApp.Server.Interfaces;
using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Repositories
{
    public class VideoRepository : IVideoRepository
    {
        private readonly MinecraftPlaylistBuilderDbContext _context;

        public VideoRepository(MinecraftPlaylistBuilderDbContext context)
        {
            _context = context;
        }
       
        public async Task<ICollection<Video>> GetVideosBySeriesSeasonChannelsAsync(string seriesTitle, string seasonTitle, string[] channelNames)
        {
            var matchingSeries = await _context.Series.SingleOrDefaultAsync(series => series.SeriesTitle == seriesTitle);
            if (matchingSeries == null)
            {
                return [];
            }
            var season = matchingSeries.Seasons.SingleOrDefault(s => s.SeasonTitle == seasonTitle);
            if (season == null)
            {
                return [];
            }
            var seasonAppearances = season.SeasonAppearances;
            if (seasonAppearances == null || !seasonAppearances.Any())
            {
                return [];
            }

            List<Video> videos = new List<Video>();
            foreach (var seasonAppearance in seasonAppearances)
            {
                if (channelNames.Contains(seasonAppearance.Channel.ChannelName))
                {
                    videos.AddRange(seasonAppearance.Videos);
                }
            }

            return videos;
        }
        
    }
}
