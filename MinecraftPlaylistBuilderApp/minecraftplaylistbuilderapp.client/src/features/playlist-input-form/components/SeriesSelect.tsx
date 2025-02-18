import Select, { SelectChangeEvent } from '@mui/material/Select';
import { MenuItem } from '@mui/material';
import { Series } from '../../../interfaces/api-interfaces';

interface Props {
    seriesList: Series[];
    selectedSeries: Series | undefined;
    onSeriesChange: (event: SelectChangeEvent) => void;
}

const SeriesSelect = ({seriesList, selectedSeries, onSeriesChange} : Props) => {
    return (
        <>
            <Select
                value={selectedSeries && selectedSeries.seriesTitle}
                label="Series"
                onChange={onSeriesChange}
                className='series-select'
            >
                {seriesList?.map((series) => (
                    <MenuItem value={series.seriesTitle} key={series.seriesTitle}>{series.seriesTitle}</MenuItem>
                ))}
            </Select>
        </>
    )
}

export default SeriesSelect;