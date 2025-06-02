import GitHubIcon from '@mui/icons-material/GitHub';
import HelpAlert from './HelpAlert';
import { Button } from '@mui/material';
import '../Header.css'
import SignInSignOutButton from './SignInSignOutButton';
import { AuthenticatedTemplate } from '@azure/msal-react';
import FeaturedPlayListIcon from '@mui/icons-material/FeaturedPlayList';
import { BASE_CLIENT_URL } from '../utils/config';

const Header = () => {
    return (
        <header>
            <span>Minecraft Playlist Builder</span>
            <span>
                <AuthenticatedTemplate>
                    <Button href={`${BASE_CLIENT_URL}/playlists`}>
                        Playlists
                    </Button>
                </AuthenticatedTemplate>
                <Button href='https://github.com/'>
                    <GitHubIcon />
                </Button>
                <HelpAlert />
                <SignInSignOutButton />

            </span>
        </header>
    )
}

export default Header;