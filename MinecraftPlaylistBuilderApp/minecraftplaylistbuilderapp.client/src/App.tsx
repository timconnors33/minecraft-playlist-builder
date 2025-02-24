import { useEffect, useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles'
import { Button, CircularProgress, CssBaseline } from '@mui/material';
import './App.css';
import PlaylistInputForm from './features/playlist-input-form/components/PlaylistInputForm';
import Header from './components/Header';
import { SeasonAppearance } from './types/api';

const darkTheme = createTheme({
    palette: {
        mode: 'dark'
    }
})

const BASE_URL = 'https://localhost:7258';

function App() {

    const [seasonAppearance, setSeasonAppearance] = useState<SeasonAppearance>();

    useEffect(() => {
        const fetchSeasonAppearance = async () => {
            const response = await fetch(`${BASE_URL}/api/seasonappearances`)
            if (!response.ok) {
                throw new Error('Failed to fetch season appearance data');
            }
            const seasonAppearanceData: SeasonAppearance = await response.json();
            if (seasonAppearanceData === undefined) {
                throw new Error('Could not read season appearance data');
            }
            console.log('Fetched season appearance data');
            setSeasonAppearance(seasonAppearanceData);
        }
        fetchSeasonAppearance();
    }, []);

    return (
        <>
            <ThemeProvider theme={darkTheme}>
                <CssBaseline />
                <Header />
                <div id='content'>
                    {(seasonAppearance ? <PlaylistInputForm seasonAppearance={seasonAppearance} /> : <CircularProgress />)}
                </div>
            </ThemeProvider>
        </>
    )
}

export default App;