using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using MinecraftPlaylistBuilderApp.Server.Dtos;
using MinecraftPlaylistBuilderApp.Server.Interfaces;

namespace MinecraftPlaylistBuilderApp.Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class SeasonAppearancesController(ISeasonAppearanceService seasonAppearanceService) : ControllerBase
    {
        private readonly ISeasonAppearanceService _seasonAppearanceService = seasonAppearanceService;

        [HttpGet]
        public async Task<ActionResult<SeasonAppearanceDto>> GetAllSeasonAppearances()
        {
            try
            {
                var seasonAppearanceDto = await _seasonAppearanceService.GetSeasonAppearanceDataAsync();
                if (seasonAppearanceDto == null)
                {
                    return NotFound("No season appearance data found.");
                }
                return Ok(seasonAppearanceDto);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
                return Problem("An error occured while getting the season appearance data.");
            }
        }
    }
}
