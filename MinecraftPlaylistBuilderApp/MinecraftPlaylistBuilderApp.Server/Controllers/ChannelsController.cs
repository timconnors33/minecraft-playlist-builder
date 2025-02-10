using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using MinecraftPlaylistBuilderApp.Server.Dtos;
using MinecraftPlaylistBuilderApp.Server.Interfaces;

namespace MinecraftPlaylistBuilderApp.Server.Controllers
{
    [Route("api/series/{seriesTitle}/seasons/{seasonTitle}/[controller]")]
    [ApiController]
    public class ChannelsController(IChannelService channelService) : ControllerBase
    {
        private readonly IChannelService _channelService = channelService;

        [HttpGet]
        public async Task<ActionResult<List<ChannelDto>>> GetChannelsForSeason(string seriesTitle, string seasonTitle)
        {
            try
            {
                var channels = await _channelService.GetChannelsBySeriesSeasonTitlesAsync(seriesTitle, seasonTitle);
                if (channels == null || !channels.Any())
                {
                    return NotFound("No channels found for the specified season.");
                }
                return Ok(channels);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
                return Problem("An error occured while getting the channels for the specified season.");
            }
        }
    }
}
