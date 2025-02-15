using System.ComponentModel.DataAnnotations;

namespace MinecraftPlaylistBuilderApp.Server.Models
{
    public class Season
    {
        [Key]
        public int SeasonId { get; set; }
        [Required]
        public int SeriesId { get; set; }
        [Required]
        public string SeasonTitle { get; set; }
        [Required]
        public bool IsCurrentSeason { get; set; }
        public virtual Series Series { get; set; }
        public virtual ICollection<SeasonAppearance> SeasonAppearances { get; set; }
    }
}
