using System.Reflection;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using MinecraftPlaylistBuilderApp.Server.Dtos;
using MinecraftPlaylistBuilderApp.Server.Interfaces;

namespace MinecraftPlaylistBuilderApp.Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class SeriesController(ISeriesService seriesService) : ControllerBase
    {
        private readonly ISeriesService _seriesService = seriesService;

        [HttpGet]
        public async Task<ActionResult<IEnumerable<SeriesDto>>> GetAllSeries()
        {
            try
            {
                List<SeriesDto> allSeriesTitles = await _seriesService.GetAllSeriesAsync();
                return Ok(allSeriesTitles);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
                return Problem("An error occured while getting the series");
            }
        }
    }
}
