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
                        This tool helps you build a customized playlist for various Minecraft multiplayer YouTube series. 
                        It sorts the videos by the time they were uploaded. Here's how to use it:
                        <ol>
                            <li>
                                Use the drop-down menus to select the series and season of your choice.
                            </li>
                            <li>
                                Choose all the channels you'd like to include in the playlist.
                            </li>
                            <li>
                                Hit the submit button and follow the instructions to log in to your YouTube account.
                            </li>
                        </ol>
                        When your done, your playlist should be created on your YouTube account!
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