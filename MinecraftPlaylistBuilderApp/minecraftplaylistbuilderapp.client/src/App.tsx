import { useEffect, useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles'
import { CssBaseline } from '@mui/material';
import './App.css';
import PlaylistInputForm from './components/PlaylistInputForm';
import Header from './components/Header';

const darkTheme = createTheme({
    palette: {
        mode: 'dark'
    }
})

function App() {
    return (
        <>
            <ThemeProvider theme={darkTheme}>
            <CssBaseline/>
            <Header/>
            <div id='content'>
                <PlaylistInputForm/>
            </div>
            </ThemeProvider>
        </>
    )
}

export default App;