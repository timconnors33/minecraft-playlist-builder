import { useEffect, useState } from 'react';
import './App.css';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { MenuItem } from '@mui/material';
import SeriesSelect from './components/SeriesSelect';
import SeasonSelect from './components/SeasonSelect';

interface Series {
    seriesTitle: string;
}

interface Season {
    seasonTitle: string;
}

interface Channel {
    channelName: string;
    channelYouTubeId: string;
    channelThumbnailUri: string;
}

function App() {
    const[seriesList, setSeriesList] = useState<Series[]>();
    // TODO: Check using undefined here
    const[selectedSeries, setSelectedSeries] = useState<string | undefined>(undefined);
    
    const[seasons, setSeasons] = useState<Season[]>();
    const [selectedSeason, setSelectedSeason] = useState<string | undefined>(undefined);

    const [channels, setChannels] = useState<Channel[]>();
    const [selectedChannels, setSelectedChannels] = useState<Channel[] | undefined>(undefined);
    

    const populateSeriesListData = async () => {
        const response = await fetch('https://localhost:7258/api/series');
        if (response.ok) {
            const seriesListData = await response.json();
            setSeriesList(seriesListData);
        }
    }

    const fetchSeasons = async (seriesTitle: string) => {
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
        setChannels([]);
        fetchSeasons(selectedTitle)
    }

    const handleSeasonChange = (event: SelectChangeEvent) => {
        const selectedTitle = event.target.value as string;
        setSelectedSeason(selectedTitle);
        setChannels([]);
        fetchChannels(selectedSeries, selectedSeason);
    }

    const fetchChannels = async (seriesTitle: string | undefined, seasonTitle: string | undefined) => {
        try {
            const response = await fetch(`https://localhost:7258/api/series/${seriesTitle}/seasons/${seasonTitle}/channels`)
            const channelsData = await response.json();
            setChannels(channelsData);
        } catch (err) {
            console.log(err);
        }
    }

    useEffect(() => {
        populateSeriesListData();
    }, []);
    
    return (
        <div>
            <h1 id="seriesListLabel">Series</h1>
            <SeriesSelect 
                seriesList={seriesList}
                selectedSeries={selectedSeries}
                onSeriesChange={handleSeriesChange}
            />
            {selectedSeries && (
                <SeasonSelect
                    seasons={seasons}
                    selectedSeason={selectedSeason}
                    onSeasonChange={handleSeasonChange}
                />
            )}
        </div>
    );
}

export default App;