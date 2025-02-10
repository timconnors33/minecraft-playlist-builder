using System.ComponentModel.DataAnnotations;

namespace MinecraftPlaylistBuilderApp.Server.Models
{
    public class SeasonAppearance()
    {
        [Key]
        public int SeasonAppearanceId { get; set; }
        [Required]
        public int SeasonId { get; set; }
        [Required]
        public int ChannelId { get; set; }
        public virtual Season Season { get; set; }
        public virtual Channel Channel { get; set; }
        public virtual ICollection<Video> Videos { get; set; }
    }
}
