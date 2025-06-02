import { useEffect, useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles'
import { CircularProgress, CssBaseline } from '@mui/material';
import './App.css';
import PlaylistInputForm from './features/playlist-input-form/components/PlaylistInputForm';
import Header from './components/Header';
import { SeasonAppearance } from './types/api';
import { Outlet, Route, Routes } from 'react-router';
import PlaylistVideoDisplay from './features/playlist-video-display/PlaylistVideoDisplay';
import { MsalProvider } from '@azure/msal-react';
import PlaylistDisplay from './features/playlist-display/PlaylistDisplay';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BASE_API_URL } from './utils/config';

const darkTheme = createTheme({
    palette: {
        mode: 'dark'
    }
})

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

const queryClient = new QueryClient();

const App = ({ instance }) => {

    const [seasonAppearance, setSeasonAppearance] = useState<SeasonAppearance>();

    useEffect(() => {
        const fetchSeasonAppearance = async () => {
            const response = await fetch(`${BASE_API_URL}/api/seasonappearances`)
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
        <MsalProvider instance={instance}>
            <QueryClientProvider client={queryClient}>
                <ThemeProvider theme={darkTheme}>
                    <CssBaseline />
                    <Routes>
                        <Route path="/" element={<Layout />}>
                            <Route index element={seasonAppearance ? <PlaylistInputForm seasonAppearance={seasonAppearance} /> : <CircularProgress />} />
                            <Route path="playlist" element={<PlaylistVideoDisplay />} />
                            <Route path="auth-response" element={<div>Authenticated!</div>} />
                            <Route path="playlists" element={<PlaylistDisplay />} />
                        </Route>
                    </Routes>
                </ThemeProvider>
            </QueryClientProvider>
        </MsalProvider>
    )
}

export default App;