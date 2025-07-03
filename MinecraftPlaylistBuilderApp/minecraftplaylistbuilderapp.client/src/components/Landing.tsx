import { Box, Button, Card, Typography } from "@mui/material"
import { darkTheme } from "../Theme"
import { BackgroundPaper } from "./BackgroundPaper"
import { AuthenticatedTemplate, UnauthenticatedTemplate } from "@azure/msal-react"
import { BASE_CLIENT_URL } from "../utils/config"

export const Landing = () => {
    return (
        <Box style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-evenly', flexGrow: 1, alignItems: 'center', maxWidth: '700px' }}>
            <Card sx={{ borderWidth: '1px', borderStyle: 'solid', borderColor: 'primary.main', padding: '10px', borderRadius: '10px' }}>
                <Typography textAlign='initial' variant="h1" sx={{ color: 'primary.main' }}>Welcome!</Typography>
                <Typography gutterBottom textAlign='initial' variant='h5' sx={{ color: 'primary.main' }}>Thank you for using Minecraft Playlist Builder!</Typography>
                <Typography textAlign='initial' variant='body1'>
                    This is a fan-made tool that helps you build customized playlists for various Minecraft multiplayer YouTube series.
                    It allows you to make playlists consisting of videos from different creators.
                    It sorts the videos by the time they were uploaded and allows you to check them off once you've watched them, so you'll be able to follow along with the fun easily!
                </Typography>
                <UnauthenticatedTemplate>
                    <Typography style={{ marginTop: '20px' }} textAlign='initial' variant='h5'>To start, click the button below to sign up or log in with your Google or Microsoft account.</Typography>
                </UnauthenticatedTemplate>
                <AuthenticatedTemplate>
                    <Typography style={{ marginTop: '20px' }} textAlign='initial' variant='h5'>It looks like you're signed in! Click the button below to view your playlists.</Typography>
                </AuthenticatedTemplate>
            </Card>
            <UnauthenticatedTemplate>
                <Button color='secondary' variant="contained" style={{ borderRadius: '8px' }}>
                    Sign Up or Log in
                </Button>
            </UnauthenticatedTemplate>
            <AuthenticatedTemplate>
                <Button color='secondary' variant="contained" style={{ borderRadius: '8px' }} href={`${BASE_CLIENT_URL}/playlists`}>
                    View Playlists
                </Button>
            </AuthenticatedTemplate>
        </Box>
    )
}