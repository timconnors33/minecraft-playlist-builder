import { Button, Card, CardContent, Link, Paper, Typography } from "@mui/material";
import { Playlist } from "../../types/api";
import DOMPurify from "dompurify";
import DeletePlaylistDialog from "./DeletePlaylistDialog";
import EditPlaylistDialog from "./EditPlaylistDialog";
import { NavLink } from "react-router";
// TODO: Make this generic so it uses the currently selected theme regardless of the actual underlying theme
import { darkTheme } from "../../Theme";

interface Props {
    playlist: Playlist;
}

function PlaylistCard({ playlist }: Props) {

    // TODO: Need to make card element flexbox?
    return (
    // TODO: Make generic card element for shared styles
        <Paper elevation={5} sx={{ width: '700px' }}>
            <CardContent style={{padding: '16px'}}>
                <div style={{ display: "flex", justifyContent: 'space-between' }}>
                    <div>
                        <NavLink to={`/playlists/${playlist.publicPlaylistId}`} style={{color: darkTheme.palette.primary.main, textAlign: 'start'}}>
                            <Typography gutterBottom variant="h6">
                                {DOMPurify.sanitize(playlist.playlistTitle)}
                            </Typography>
                        </NavLink>
                        <Typography variant="body2" sx={{ color: 'text.secondary', textAlign: 'start' }}>
                            {DOMPurify.sanitize(playlist.seriesTitle)}
                        </Typography>
                        <Typography variant="body2" sx={{ color: 'text.secondary', textAlign: 'start' }}>
                            {DOMPurify.sanitize(playlist.seasonTitle)}
                        </Typography>
                    </div>
                    <div style={{ display: "flex", flexDirection: 'column', justifyContent: 'space-between' }}>
                        <EditPlaylistDialog playlistId={playlist.publicPlaylistId} currentTitle={playlist.playlistTitle} />
                        <DeletePlaylistDialog playlistId={playlist.publicPlaylistId} />
                    </div>
                </div>
            </CardContent>
        </Paper>
    )
}

export default PlaylistCard;