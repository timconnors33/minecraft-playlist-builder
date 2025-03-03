import { useEffect, useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles'
import { CircularProgress, CssBaseline } from '@mui/material';
import './App.css';
import PlaylistInputForm from './features/playlist-input-form/components/PlaylistInputForm';
import Header from './components/Header';
import { SeasonAppearance } from './types/api';
import { Outlet, Route, Routes } from 'react-router';
import PlaylistDisplay from './features/playlist-display/PlaylistDisplay';

const darkTheme = createTheme({
    palette: {
        mode: 'dark'
    }
})

const BASE_URL = 'https://localhost:7258';

function Layout() {
    return (
        <>
            <Header />
            <div id='content'>
                <Outlet />
            </div>
        </>
    );
}

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
                <Routes>
                    <Route path="/" element={<Layout />}>
                        <Route index element={seasonAppearance ? <PlaylistInputForm seasonAppearance={seasonAppearance} /> : <CircularProgress />} />
                        <Route path="playlist" element={<PlaylistDisplay />} />
                    </Route>
                </Routes>
            </ThemeProvider>
        </>
    )
}

export default App;