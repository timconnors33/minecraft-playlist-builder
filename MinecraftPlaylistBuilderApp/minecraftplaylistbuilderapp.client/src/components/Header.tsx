import GitHubIcon from '@mui/icons-material/GitHub';
import HelpAlert from './HelpAlert';
import { Button, Paper } from '@mui/material';
import '../Header.css'
import SignInSignOutButton from './SignInSignOutButton';
import { AuthenticatedTemplate } from '@azure/msal-react';
import { BASE_CLIENT_URL } from '../utils/config';
import { darkTheme } from '../Theme';

const Header = () => {
    return (
        <header>
            <Paper elevation={20} square style={{ color: darkTheme.palette.primary.main, padding: '10px', display: 'flex', alignSelf: 'stretch', justifyContent: 'space-between', alignItems: 'center', flexGrow: '1' }}>
                <Button href={BASE_CLIENT_URL}>Minecraft Playlist Builder</Button>
                <span>
                    <AuthenticatedTemplate>
                        <Button href={`${BASE_CLIENT_URL}/playlists`}>
                            View Playlists
                        </Button>
                    </AuthenticatedTemplate>
                    <Button href={`${BASE_CLIENT_URL}/create-playlist`}>
                        Create Playlist
                    </Button>
                    <Button href='https://github.com/'>
                        <GitHubIcon />
                    </Button>
                    <HelpAlert />
                    <SignInSignOutButton />

                </span>
            </Paper>
        </header>
    )
}

export default Header;