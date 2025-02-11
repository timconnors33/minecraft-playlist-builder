using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Interfaces
{
    public interface IVideoRepository
    {
       Task<ICollection<Video>> GetVideosBySeriesSeasonChannelAsync(string seriesTitle, string seasonTitle, string channelTitle);
    }
}
