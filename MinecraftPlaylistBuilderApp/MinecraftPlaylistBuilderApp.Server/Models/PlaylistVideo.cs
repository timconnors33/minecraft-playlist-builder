using System.ComponentModel.DataAnnotations;

namespace MinecraftPlaylistBuilderApp.Server.Models
{
    public class PlaylistVideo
    {
        [Key]
        public int PlaylistVideoId { get; set; }
        [Required]
        public Guid PublicPlaylistVideoId { get; set; }
        [Required]
        public int PlaylistId { get; set; }
        [Required]
        public int VideoId { get; set; }
        [Required]
        public bool IsWatched { get; set; }
        public virtual Playlist Playlist { get; set; }
        public virtual Video Video { get; set; }

    }
}
