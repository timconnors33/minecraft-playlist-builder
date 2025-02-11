using System.ComponentModel.DataAnnotations;

namespace MinecraftPlaylistBuilderApp.Server.Models
{
    public class Video
    {
        [Key]
        public int VideoId { get; set; }
        [Required]
        public string VideoYouTubeId { get; set; }
        [Required]
        public string VideoTitle { get; set; }
        [Required]
        public string VideoThumbnailUri { get; set; }
        [Required]
        public DateTime VideoPublishedAt { get; set; }
        [Required]
        public int SeasonAppearanceId { get; set; }

        public virtual SeasonAppearance SeasonAppearance { get; set; }
        
    }
}
