using System.ComponentModel.DataAnnotations;

namespace MinecraftPlaylistBuilderApp.Server.Models
{
    public class Channel
    {
        [Key]
        public int ChannelId { get; set; }
        [Required]
        public string ChannelYouTubeId { get; set; }
        [Required]
        public string ChannelName { get; set; }
        [Required]
        public string ChannelThumbnailUri { get; set; }
    }
}
