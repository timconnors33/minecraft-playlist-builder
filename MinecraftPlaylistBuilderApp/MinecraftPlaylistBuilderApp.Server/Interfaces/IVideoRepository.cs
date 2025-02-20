using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Interfaces
{
    public interface IVideoRepository
    {
       Task<ICollection<Video>> GetVideosBySeriesSeasonChannelsAsync(string seriesTitle, string seasonTitle, string[] channelNames);
    }
}
