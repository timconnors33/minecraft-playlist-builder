using MinecraftPlaylistBuilderApp.Server.Dtos;
using MinecraftPlaylistBuilderApp.Server.Interfaces;

namespace MinecraftPlaylistBuilderApp.Server.Services
{
    public class ChannelService : IChannelService
    {
        private readonly IChannelRepository _channelRepository;

        public ChannelService(IChannelRepository channelRepository)
        {
            _channelRepository = channelRepository;
        }
        public async Task<List<ChannelDto>> GetChannelsBySeriesSeasonTitlesAsync(string seriesTitle, string seasonTitle)
        {
            var channels = await _channelRepository.GetChannelsBySeriesSeasonTitlesAsync(seriesTitle, seasonTitle);
            if (channels == null)
            {
                return [];
            }
            var channelDtos = new List<ChannelDto>();
            foreach (var channel in channels)
            {
                var channelDto = new ChannelDto(channel.ChannelName, channel.ChannelYouTubeId, channel.ChannelThumbnailUri);
                channelDtos.Add(channelDto);
            }
            return channelDtos;
        }
    }
}
