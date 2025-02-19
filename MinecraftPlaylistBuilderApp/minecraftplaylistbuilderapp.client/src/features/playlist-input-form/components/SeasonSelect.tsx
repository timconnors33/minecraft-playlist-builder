import { SelectChangeEvent, Select, MenuItem, FormHelperText } from "@mui/material";
import { Season } from "../../../interfaces/api-interfaces";
import '../PlaylistInputForm.css'

interface Props {
    seasons: Season[];
    selectedSeason: Season;
    onSeasonChange: (event: SelectChangeEvent) => void;
}

const SeasonSelect = ({seasons, selectedSeason, onSeasonChange}: Props) => {
    return (
        <div>
            <FormHelperText>Season</FormHelperText>
            <Select
                value={selectedSeason ? selectedSeason.seasonTitle : undefined}
                label="Series"
                onChange={onSeasonChange}
            >
                {seasons?.map((season) => (
                    <MenuItem value={season.seasonTitle} key={season.seasonTitle}>{season.seasonTitle}</MenuItem>
                ))}
            </Select>
        </div>
    )
}

export default SeasonSelect;