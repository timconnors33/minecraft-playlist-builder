using System.ComponentModel.DataAnnotations;

namespace MinecraftPlaylistBuilderApp.Server.Models
{
    public class Playlist
    {
        [Key]
        public int PlaylistId { get; set; }
        [Required]
        public Guid PublicPlaylistId { get; set; }
        [Required]
        public Guid OwnerId { get; set; }
        [Required]
        public string PlaylistTitle { get; set; }
        [Required]
        public int SeasonId { get; set; }
    }
}
