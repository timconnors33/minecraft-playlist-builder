using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using MinecraftPlaylistBuilderApp.Server.Dtos;
using MinecraftPlaylistBuilderApp.Server.Interfaces;
using MinecraftPlaylistBuilderApp.Server.Models;
using MinecraftPlaylistBuilderApp.Server.Services;

namespace MinecraftPlaylistBuilderApp.Server.Controllers
{
    [Route("api/series/{seriesTitle}/seasons/{seasonTitle}/channels/{channelTitle}/[controller]")]
    [ApiController]
    public class VideosController(IVideoService videoService) : ControllerBase
    {
        private readonly IVideoService _videoService = videoService;

        [HttpGet]
        public async Task<ActionResult<List<VideoDto>>> GetVideoBySeriesSeasonChannel(string seriesTitle, string seasonTitle, string channelTitle)
        {
            try
            {
                var videos = await _videoService.GetVideosBySeriesSeasonChannelAsync(seriesTitle, seasonTitle, channelTitle);
                if (videos == null || !videos.Any())
                {
                    return NotFound("No videos found for the specified channel.");
                }
                return Ok(videos);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
                return Problem("An error occured while getting the videos for the specified channel.");
            }
        }
    }
}
