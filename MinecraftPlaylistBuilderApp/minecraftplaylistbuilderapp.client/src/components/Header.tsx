import GitHubIcon from '@mui/icons-material/GitHub';
import HelpAlert from './HelpAlert';
import { Button } from '@mui/material';
import '../Header.css'

const Header = () => {
    return (
        <header>
            <span>Minecraft Playlist Builder</span>
            <span>
                <Button href='https://github.com/'>
                        <GitHubIcon/>
                </Button>
                <HelpAlert/>
            </span>
        </header>
    )
}

export default Header;