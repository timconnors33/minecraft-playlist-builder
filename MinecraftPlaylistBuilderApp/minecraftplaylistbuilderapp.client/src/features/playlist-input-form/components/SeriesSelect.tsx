import Select, { SelectChangeEvent } from '@mui/material/Select';
import { FormHelperText, MenuItem } from '@mui/material';
import { Series } from '../../../types/api';

interface Props {
    seriesList: Series[];
    selectedSeries: Series;
    onSeriesChange: (event: SelectChangeEvent) => void;
}

const SeriesSelect = ({ seriesList, selectedSeries, onSeriesChange }: Props) => {
    return (
        <div>
            <FormHelperText>Series</FormHelperText>
            <Select
                value={selectedSeries && selectedSeries.seriesTitle}
                label="Series"
                onChange={onSeriesChange}
                id='series-select'
            >
                {seriesList?.map((series) => (
                    <MenuItem value={series.seriesTitle} key={series.seriesTitle}>{series.seriesTitle}</MenuItem>
                ))}
            </Select>
        </div>
    )
}

export default SeriesSelect;