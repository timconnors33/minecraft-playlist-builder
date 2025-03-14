import Select, { SelectChangeEvent } from '@mui/material/Select';
import { FormHelperText, MenuItem } from '@mui/material';
import { Series } from '../../../types/api';
import DOMPurify from "dompurify";

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
                value={selectedSeries && DOMPurify.sanitize(selectedSeries.seriesTitle)}
                label="Series"
                onChange={onSeriesChange}
                id='series-select'
            >
                {seriesList?.map((series) => (
                    <MenuItem value={DOMPurify.sanitize(series.seriesTitle)} key={DOMPurify.sanitize(series.seriesTitle)}>{DOMPurify.sanitize(series.seriesTitle)}</MenuItem>
                ))}
            </Select>
        </div>
    )
}

export default SeriesSelect;