import GitHubIcon from '@mui/icons-material/GitHub';
import HelpAlert from './HelpAlert';
import { Button } from '@mui/material';

const Header = () => {
    return (
        <header>
            <span>Minecraft Playlist Builder</span>
            <span>
                <Button>
                    <a href='https://github.com/'>
                        <GitHubIcon/>
                    </a>
                </Button>
                <HelpAlert/>
            </span>
        </header>
    )
}

export default Header;