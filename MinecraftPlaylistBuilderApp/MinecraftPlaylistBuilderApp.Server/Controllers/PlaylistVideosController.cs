using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Identity.Web;
using Microsoft.Identity.Web.Resource;
using MinecraftPlaylistBuilderApp.Server.Dtos;
using MinecraftPlaylistBuilderApp.Server.Interfaces;
using MinecraftPlaylistBuilderApp.Server.Services;

namespace MinecraftPlaylistBuilderApp.Server.Controllers
{
    [Authorize]
    [Route("api/playlists/{playlistId}/[controller]")]
    [ApiController]
    public class PlaylistVideosController(IPlaylistVideoService playlistVideoService) : ControllerBase
    {
        private readonly IPlaylistVideoService _playlistVideoService = playlistVideoService;
        private readonly Guid playlistId;
        // TODO: Implement this method in a resource shared by all authorized-protected routes?
        private Guid GetUserId()
        {
            Guid userId;

            if (!Guid.TryParse(HttpContext.User.GetObjectId(), out userId))
            {
                throw new Exception("User ID is not valid.");
            }

            return userId;
        }

        [HttpGet]
        [RequiredScope(
            RequiredScopesConfigurationKey = "AzureAD:Scopes:Read"
        )]
        public async Task<IActionResult> GetAllAsync(Guid playlistId)
        {
            var playlistVideos = await _playlistVideoService.GetPlaylistVideosByPlaylistIdAsync(GetUserId(), playlistId);
            return Ok(playlistVideos);
        }

        [HttpGet("{playlistVideoId}")]
        [RequiredScope(
            RequiredScopesConfigurationKey = "AzureAD:Scopes:Read"
        )]
        public async Task<IActionResult> GetAsync(Guid playlistId, Guid playlistVideoId)
        {
            var playlistVideo = await _playlistVideoService.GetPlaylistVideoByIdAsync(GetUserId(), playlistId, playlistVideoId);

            if (playlistVideo == null)
            {
                return NotFound();
            }

            return Ok(playlistVideo);
        }

        [HttpPost]
        [RequiredScope(
            RequiredScopesConfigurationKey = "AzureAD:Scopes:Write"
        )]
        public async Task<IActionResult> CreateAsync(Guid playlistId, [FromBody] CreatePlaylistVideoDto createPlaylistVideoDto)
        {
            var playlistVideos = await _playlistVideoService.CreatePlaylistVideosAsync(GetUserId(), playlistId, createPlaylistVideoDto);

            // TODO: Add more extensive error handling here
            if (playlistVideos == null)
            {
                return BadRequest();
            }

            return Ok(playlistVideos);
        }

        [HttpPut("{playlistVideoId}")]
        [RequiredScope(
            RequiredScopesConfigurationKey = "AzureAD:Scopes:Write"
        )]
        public async Task<IActionResult> UpdateAsync(Guid playlistId, [FromBody] UpdatePlaylistVideoDto updatePlaylistVideoDto, Guid playlistVideoId)
        {
            var updatedPlaylistVideo = await _playlistVideoService.UpdatePlaylistVideoAsync(GetUserId(), playlistId, playlistVideoId, updatePlaylistVideoDto);

            // TODO: Add more extensive error handling here
            if (updatedPlaylistVideo == null)
            {
                return BadRequest();
            }

            return Ok(updatedPlaylistVideo);
        }

        [HttpDelete("{playlistVideoId}")]
        [RequiredScope(
            RequiredScopesConfigurationKey = "AzureAD:Scopes:Write"
        )]
        public async Task<IActionResult> DeleteAsync(Guid playlistId, Guid playlistVideoId)
        {
            var isDeleted = await _playlistVideoService.DeletePlaylistVideoAsync(GetUserId(), playlistId, playlistVideoId);
            if (!isDeleted)
            {
                return NotFound();
            }

            return NoContent();
        }
    }
}
