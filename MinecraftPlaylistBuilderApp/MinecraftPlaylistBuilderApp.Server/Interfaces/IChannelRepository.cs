using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Interfaces
{
    public interface IChannelRepository
    {
        Task<ICollection<Channel>> GetChannelsBySeriesSeasonTitlesAsync(string seriesTitle, string seasonTitle);
    }
}
