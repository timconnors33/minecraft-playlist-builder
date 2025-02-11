using MinecraftPlaylistBuilderApp.Server.Dtos;

namespace MinecraftPlaylistBuilderApp.Server.Interfaces
{
    public interface IChannelService
    {
        Task<List<ChannelDto>> GetChannelsBySeriesSeasonTitlesAsync(string seriesTitle, string seasonTitle);
    }
}
