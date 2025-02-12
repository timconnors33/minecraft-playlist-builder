import { useEffect, useState } from 'react';
import './App.css';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { MenuItem } from '@mui/material';

interface Series {
    seriesTitle: string;
}

interface Season {
    seasonTitle: string;
}

function App() {
    const[seriesList, setSeriesList] = useState<Series[]>();
    // TODO: Check using undefined here
    const[selectedSeries, setSelectedSeries] = useState<string | undefined>(undefined);
    const[seasons, setSeasons] = useState<Season[]>();

    const populateSeriesListData = async () => {
        const response = await fetch('https://localhost:7258/api/series');
        if (response.ok) {
            const seriesListData = await response.json();
            setSeriesList(seriesListData);
        }
    }

    const fetchSeasons = async(seriesTitle: string) => {
        try {
            const response = await fetch(`https://localhost:7258/api/series/${seriesTitle}/seasons`);
            if (!response.ok) {
                throw new Error('Failed to fetch seasons');
            }
            const seasonsData = await response.json();
            setSeasons(seasonsData);
        } catch (err) {
            console.log(err);
        }
    }

    const handleSeriesChange = (event: SelectChangeEvent) => {
        const selectedTitle = event.target.value as string;
        setSelectedSeries(selectedTitle);
        setSeasons([]);
        fetchSeasons(selectedTitle)
    }

    useEffect(() => {
        populateSeriesListData();
    }, []);
    
    return (
        <div>
            <h1 id="seriesListLabel">Series</h1>
            <Select
                value={selectedSeries}
                label="Series"
                onChange={handleSeriesChange}
            >
                {seriesList?.map((series) => (
                    <MenuItem value={series.seriesTitle}>{series.seriesTitle}</MenuItem>
                ))}
            </Select>
            {selectedSeries && (
                <>
                    <Select
                        label="Season"
                    >
                        {seasons?.map((season) => (
                            <MenuItem value={season.seasonTitle}>{season.seasonTitle}</MenuItem>
                        ))}
                    </Select>
                </>
            )}
        </div>
    );
}

/* interface Forecast {
    date: string;
    temperatureC: number;
    temperatureF: number;
    summary: string;
}

function App() {
    const [forecasts, setForecasts] = useState<Forecast[]>();

    useEffect(() => {
        populateWeatherData();
    }, []);

    const contents = forecasts === undefined
        ? <p><em>Loading... Please refresh once the ASP.NET backend has started. See <a href="https://aka.ms/jspsintegrationreact">https://aka.ms/jspsintegrationreact</a> for more details.</em></p>
        : <table className="table table-striped" aria-labelledby="tableLabel">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Temp. (C)</th>
                    <th>Temp. (F)</th>
                    <th>Summary</th>
                </tr>
            </thead>
            <tbody>
                {forecasts.map(forecast =>
                    <tr key={forecast.date}>
                        <td>{forecast.date}</td>
                        <td>{forecast.temperatureC}</td>
                        <td>{forecast.temperatureF}</td>
                        <td>{forecast.summary}</td>
                    </tr>
                )}
            </tbody>
        </table>;

    return (
        <div>
            <h1 id="tableLabel">Weather forecast</h1>
            <p>This component demonstrates fetching data from the server.</p>
            {contents}
        </div>
    );

    async function populateWeatherData() {
        const response = await fetch('weatherforecast');
        if (response.ok) {
            const data = await response.json();
            setForecasts(data);
        }
    }
} */

export default App;