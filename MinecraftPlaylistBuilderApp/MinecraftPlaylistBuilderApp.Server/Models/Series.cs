using System.ComponentModel.DataAnnotations;

namespace MinecraftPlaylistBuilderApp.Server.Models
{
    public class Series
    {
        [Key]
        public int SeriesId { get; set; }
        [Required]
        public string SeriesTitle { get; set; }
        public virtual ICollection<Season> Seasons { get; set; }
    }
}
