using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using MinecraftPlaylistBuilderApp.Server.Dtos;
using MinecraftPlaylistBuilderApp.Server.Interfaces;

namespace MinecraftPlaylistBuilderApp.Server.Controllers
{
    [Route("api/series/{seriesTitle}/[controller]")]
    [ApiController]
    public class SeasonsController(ISeasonService seasonService) : ControllerBase
    {
        private readonly ISeasonService _seasonService = seasonService;

        [HttpGet]
        public async Task<ActionResult<IEnumerable<SeasonDto>>> GetSeasonsBySeriesTitle(string seriesTitle)
        {
            try
            {
                List<SeasonDto> seasonsBySeriesTitle = await _seasonService.GetSeasonsBySeriesTitleAsync(seriesTitle);
                if (seasonsBySeriesTitle == null || !seasonsBySeriesTitle.Any())
                {
                    return NotFound("No seasons found for the specified series.");
                }
                return Ok(seasonsBySeriesTitle);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex);
                return Problem("An error occured while getting the seasons.");
            }
        }
    }
}
