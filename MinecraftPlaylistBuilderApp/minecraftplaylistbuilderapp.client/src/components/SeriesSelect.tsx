import Select, { SelectChangeEvent } from '@mui/material/Select';
import { MenuItem } from '@mui/material';

interface Series {
    seriesTitle: string;
}

interface Props {
    seriesList: Series[];
    selectedSeries: string;
    onSeriesChange: (event: SelectChangeEvent) => void;
}

const SeriesSelect = ({seriesList, selectedSeries, onSeriesChange} : Props) => {
    return (
        <>
            <Select
                value={selectedSeries}
                label="Series"
                onChange={onSeriesChange}
            >
                {seriesList?.map((series) => (
                    <MenuItem value={series.seriesTitle}>{series.seriesTitle}</MenuItem>
                ))}
            </Select>
        </>
    )
}

export default SeriesSelect;