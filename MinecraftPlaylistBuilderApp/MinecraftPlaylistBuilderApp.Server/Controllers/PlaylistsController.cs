// Authentication code based on examples provided by https://github.com/Azure-Samples/ms-identity-ciam-javascript-tutorial.git

using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Identity.Web;
using Microsoft.Identity.Web.Resource;
using MinecraftPlaylistBuilderApp.Server.Dtos;
using MinecraftPlaylistBuilderApp.Server.Interfaces;

namespace MinecraftPlaylistBuilderApp.Server.Controllers
{
    [Authorize]
    [Route("api/[controller]")]
    [ApiController]
    public class PlaylistsController(IPlaylistService playlistService) : ControllerBase
    {
        private readonly IPlaylistService _playlistService = playlistService;
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
        public async Task<IActionResult> GetAllAsync()
        {
            var playlists = await _playlistService.GetAllAsync(GetUserId());
            return Ok(playlists);
        }

        [HttpGet("{playlistId}")]
        [RequiredScope(
            RequiredScopesConfigurationKey = "AzureAD:Scopes:Read"
        )]
        public async Task<IActionResult> GetAsync(Guid playlistId)
        {
            var playlist = await _playlistService.GetPlaylistAsync(playlistId, GetUserId());

            if (playlist == null)
            {
                return NotFound();
            }

            return Ok(playlist);
        }

        [HttpPost]
        [RequiredScope(
            RequiredScopesConfigurationKey = "AzureAD:Scopes:Write"
        )]
        public async Task<IActionResult> CreateAsync([FromBody] CreatePlaylistDto createPlaylistDto)
        {
            var playlist = await _playlistService.CreatePlaylistAsync(createPlaylistDto, GetUserId());

            // TODO: Add more extensive error handling here
            if (playlist == null)
            {
                return BadRequest();
            }

            return Ok(playlist);
        }

        [HttpPut("{playlistId}")]
        [RequiredScope(
            RequiredScopesConfigurationKey = "AzureAD:Scopes:Write"
        )]
        public async Task<IActionResult> UpdateAsync([FromBody] UpdatePlaylistDto updatePlaylistDto, Guid playlistId)
        {
            var updatedPlaylist = await _playlistService.UpdatePlaylistAsync(updatePlaylistDto, GetUserId(), playlistId);

            // TODO: Add more extensive error handling here
            if (updatedPlaylist == null)
            {
                return BadRequest();
            }

            return Ok(updatedPlaylist);
        }

        [HttpDelete("{playlistId}")]
        [RequiredScope(
            RequiredScopesConfigurationKey = "AzureAD:Scopes:Write"
        )]
        public async Task<IActionResult> DeleteAsync(Guid playlistId)
        {
            var isDeleted = await _playlistService.DeletePlaylistAsync(GetUserId(), playlistId);
            if (!isDeleted)
            {
                return NotFound();
            }

            return NoContent();
        }
    }
    
}
