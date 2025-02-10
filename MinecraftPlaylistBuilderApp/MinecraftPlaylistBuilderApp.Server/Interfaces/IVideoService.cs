using MinecraftPlaylistBuilderApp.Server.Dtos;
using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Interfaces
{
    public interface IVideoService
    {
        public Task<List<VideoDto>> GetVideosBySeriesSeasonChannelAsync(string seriesTitle, string seasonTitle, string channelName);
    }
}
