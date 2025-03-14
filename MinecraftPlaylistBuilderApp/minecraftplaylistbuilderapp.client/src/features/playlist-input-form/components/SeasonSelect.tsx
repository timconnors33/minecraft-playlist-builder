import { SelectChangeEvent, Select, MenuItem, FormHelperText } from "@mui/material";
import { Season } from "../../../types/api";
import '../PlaylistInputForm.css'
import DOMPurify from "dompurify";

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
                value={selectedSeason ? DOMPurify.sanitize(selectedSeason.seasonTitle) : undefined}
                label="Series"
                onChange={onSeasonChange}
            >
                {seasons?.map((season) => (
                    <MenuItem value={DOMPurify.sanitize(season.seasonTitle)} key={DOMPurify.sanitize(season.seasonTitle)}>{DOMPurify.sanitize(season.seasonTitle)}</MenuItem>
                ))}
            </Select>
        </div>
    )
}

export default SeasonSelect;