namespace MinecraftPlaylistBuilderApp.Server.Dtos
{
    public record SeasonAppearanceDto(IEnumerable<SeasonAppearanceSeriesDto> Series) { }
    public record SeasonAppearanceSeriesDto(string SeriesTitle, IEnumerable<SeasonAppearanceSeasonDto> Seasons) { }
    public record SeasonAppearanceSeasonDto(string SeasonTitle, IEnumerable<SeasonAppearanceChannelDto> Channels) { }
    public record SeasonAppearanceChannelDto(string ChannelName, string ChannelYouTubeId, string ChannelThumbnailUri) { }
}
