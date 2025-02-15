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
        public async Task<ActionResult<List<SeasonAppearanceDto>>> GetAllSeasonAppearances()
        {
            try
            {
                var seasonAppearanceDtos = await _seasonAppearanceService.GetAllSeasonAppearancesAsync();
                if (seasonAppearanceDtos == null || !seasonAppearanceDtos.Any())
                {
                    return NotFound("No season appearances found.");
                }
                return Ok(seasonAppearanceDtos);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
                return Problem("An error occured while getting the season appearances.");
            }
        }
    }
}
