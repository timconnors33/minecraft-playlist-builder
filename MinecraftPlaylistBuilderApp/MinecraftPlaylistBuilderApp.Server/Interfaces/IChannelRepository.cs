using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Interfaces
{
    public interface IChannelRepository
    {
        Task<List<Channel>> GetChannelsBySeriesSeasonTitlesAsync(string seriesTitle, string seasonTitle);
    }
}
