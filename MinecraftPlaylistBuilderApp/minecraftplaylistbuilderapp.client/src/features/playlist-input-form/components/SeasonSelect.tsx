import { SelectChangeEvent, Select, MenuItem } from "@mui/material";
import { Season } from "../../../interfaces/api-interfaces";
import '../PlaylistInputForm.css'

interface Props {
    seasons: Season[];
    selectedSeason: Season | undefined;
    onSeasonChange: (event: SelectChangeEvent) => void;
}

const SeasonSelect = ({seasons, selectedSeason, onSeasonChange}: Props) => {
    return (
        <>
            <Select
                value={selectedSeason ? selectedSeason.seasonTitle : undefined}
                label="Series"
                onChange={onSeasonChange}
            >
                {seasons?.map((season) => (
                    <MenuItem value={season.seasonTitle} key={season.seasonTitle}>{season.seasonTitle}</MenuItem>
                ))}
            </Select>
        </>
    )
}

export default SeasonSelect;