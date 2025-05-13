import GitHubIcon from '@mui/icons-material/GitHub';
import HelpAlert from './HelpAlert';
import { Button } from '@mui/material';
import '../Header.css'
import SignInSignOutButton from './SignInSignOutButton';

const Header = () => {
    return (
        <header>
            <span>Minecraft Playlist Builder</span>
            <span>
                <Button href='https://github.com/'>
                        <GitHubIcon/>
                </Button>
                <HelpAlert/>
                <SignInSignOutButton/>
            </span>
        </header>
    )
}

export default Header;