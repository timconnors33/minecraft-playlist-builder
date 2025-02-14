import { SelectChangeEvent, Select, MenuItem } from "@mui/material";

interface Season {
    seasonTitle: string;
}

interface Props {
    seasons: Season[];
    selectedSeason: string;
    onSeasonChange: (event: SelectChangeEvent) => void;
}

const SeasonSelect = ({seasons, selectedSeason, onSeasonChange}: Props) => {
    return (
        <>
            <Select
                value={selectedSeason}
                label="Series"
                onChange={onSeasonChange}
            >
                {seasons?.map((season) => (
                    <MenuItem value={season.seasonTitle}>{season.seasonTitle}</MenuItem>
                ))}
            </Select>
        </>
    )
}

export default SeasonSelect;