import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from "@mui/material";
import HelpIcon from '@mui/icons-material/Help';
import { useState } from "react"

const HelpAlert = () => {
    // https://mui.com/material-ui/react-dialog/
    const [isOpen, setIsOpen] = useState(false);
    
    const handleClickIcon = () => {
        setIsOpen(true);
    };

    const handleCloseDialog = () => {
        setIsOpen(false);
    };

    return (
        <>
            <Button onClick={handleClickIcon}>
                <HelpIcon/>
            </Button>
            <Dialog
                open={isOpen}
                onClose={handleCloseDialog}
                aria-labelledby="help-alert-dialog-title"
                aria-describedby="help-alert-dialog-description"
            >
                <DialogTitle id="help-alert-dialog-title">
                    How to build your playlist
                </DialogTitle>
                <DialogContent>
                    <DialogContentText id="help-alert-dialog-description">
                        Here's how to use make and use your playlist:
                        <ol>
                            <li>
                                Use the drop-down menus to select the series and season of your choice.
                            </li>
                            <li>
                                Choose all the channels you'd like to include in the playlist.
                            </li>
                            <li>
                                Hit the submit button. Your playlist will now be available. You can navigate to your playlists at any time using the "View Playlists" button.
                            </li>
                            <li>
                                Click on your playlist title to see all its videos. You can click the video title to be taken to its YouTube page. After your done watching, just mark the video as watched!
                            </li>
                        </ol>
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseDialog}>Close</Button>
                </DialogActions>
            </Dialog>
        </>
    )
}

export default HelpAlert;