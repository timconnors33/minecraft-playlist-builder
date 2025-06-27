import { Button, Dialog, DialogActions, DialogTitle } from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';
import { useState } from "react";
import useFetchWithMsal from "../../utils/useFetchWithMsal";
import { protectedResources } from "../../utils/authConfig";
import { useQueryClient, useMutation } from "@tanstack/react-query";
import { UUID } from "crypto";

interface Props {
    playlistId: UUID;
}

function DeletePlaylistDialog({ playlistId }: Props) {
    const [openDialog, setOpenDialog] = useState<boolean>(false);

    const { error, execute } = useFetchWithMsal({ scopes: [protectedResources.playlistApi.scopes.write] });
    const queryClient = useQueryClient();

    const deletePlaylistMn = useMutation({
        mutationKey: ['playlists', playlistId],
        mutationFn: async (playlistId: UUID) => {
            // TODO: Ok to build uri like this? 
            return await execute('DELETE', `${protectedResources.playlistApi.endpoint}/${playlistId}`, null);
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['playlists'] });
        },
        onError: () => {
            console.log('Error deleting playlist');
        }
    });

    const handleDeletePlaylist = async () => {
        await deletePlaylistMn.mutateAsync(playlistId);
        setOpenDialog(false);
    }

    const handleClickIcon = () => {
        setOpenDialog(true);
    };

    const handleCloseDialog = () => {
        setOpenDialog(false);
    };

    return (
        <>
            <Button onClick={handleClickIcon}>
                <DeleteIcon />
            </Button>
            <Dialog
                open={openDialog}
                onClose={handleCloseDialog}
                aria-labelledby="delete-playlist-dialog-title"
                aria-describedby="delete-playlist-dialog-description"
            >
                <DialogTitle id="delete-playlist-dialog-title">
                    {'Are you sure you want to delete this playlist?'}
                </DialogTitle>
                <DialogActions>
                    <Button onClick={handleDeletePlaylist}>Delete</Button>
                    <Button onClick={handleCloseDialog}>Cancel</Button>
                </DialogActions>
            </Dialog>
        </>
    );
};

export default DeletePlaylistDialog;
