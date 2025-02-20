using System.Text.Json;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using MinecraftPlaylistBuilderApp.Server.Dtos;
using MinecraftPlaylistBuilderApp.Server.Interfaces;
using MinecraftPlaylistBuilderApp.Server.Models;
using MinecraftPlaylistBuilderApp.Server.Services;

namespace MinecraftPlaylistBuilderApp.Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class VideosController(IVideoService videoService) : ControllerBase
    {
        private readonly IVideoService _videoService = videoService;

        [HttpPost]
        public async Task<ActionResult<List<VideoDto>>> GetVideoBySeriesSeasonChannel([FromBody] PostVideosDto postVideosDto)
        {
            try
            {
                Console.WriteLine(postVideosDto.ToString());
                var videos = await _videoService.GetVideosBySeriesSeasonChannelsAsync(postVideosDto.SeriesTitle, postVideosDto.SeasonTitle, postVideosDto.ChannelNames);
                if (videos == null || !videos.Any())
                {
                    return NotFound("No videos found matching the specified parameters.");
                }
                return Ok(videos);
            }
            catch (JsonException jsonEx)
            {
                Console.WriteLine(jsonEx.Message);
                return BadRequest("The request for videos is invalid.");
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
                return Problem("An error occured while getting the videos for the specified channel.");
            }
        }
    }
}
