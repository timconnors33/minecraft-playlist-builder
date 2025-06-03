using FluentValidation;
using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Validators
{
    public class PlaylistValidator : AbstractValidator<Playlist>
    {
        public PlaylistValidator() 
        {
            RuleFor(playlist => playlist.PublicPlaylistId).NotNull();
            RuleFor(playlist => playlist.OwnerId).NotNull();
            RuleFor(playlist => playlist.PlaylistTitle).NotNull().Length(1, 64);
            RuleFor(playlist => playlist.Season).NotNull();
        }
    }
}
