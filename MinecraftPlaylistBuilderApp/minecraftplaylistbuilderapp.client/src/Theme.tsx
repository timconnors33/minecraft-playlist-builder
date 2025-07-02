import { createTheme, Theme } from '@mui/material/styles';

export const theme: Theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#43ecec',
    },
    secondary: {
      main: '#60d265',
    },
    text: {
      primary: 'rgba(255,255,255,0.87)',
    },
  },
});

export const darkTheme: Theme = createTheme({
    palette: {
        mode: 'dark'
    }
})