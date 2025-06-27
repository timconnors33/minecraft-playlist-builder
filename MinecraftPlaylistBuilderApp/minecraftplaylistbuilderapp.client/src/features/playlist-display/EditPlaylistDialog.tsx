import { Button, Dialog, DialogActions, DialogTitle, TextField } from "@mui/material";
import EditIcon from '@mui/icons-material/Edit';
import { useState } from "react";
import useFetchWithMsal from "../../utils/useFetchWithMsal";
import { protectedResources } from "../../utils/authConfig";
import { useQueryClient, useMutation } from "@tanstack/react-query";
import { UUID } from "crypto";
import { useForm, SubmitHandler } from "react-hook-form";

interface Props {
    playlistId: UUID;
    currentTitle: string;
}

interface IFormInput {
    newTitle: string;
}

function EditPlaylistDialog({ playlistId, currentTitle }: Props) {
    const [openDialog, setOpenDialog] = useState<boolean>(false);
    const [playlistTitle, setPlaylistTitle] = useState<string>(currentTitle);

    const { error, execute } = useFetchWithMsal({ scopes: [protectedResources.playlistApi.scopes.write] });
    const queryClient = useQueryClient();

    const { register, handleSubmit } = useForm<IFormInput>();
    const onSubmit: SubmitHandler<IFormInput> = async (data) => { 
        console.log(data);
        await editPlaylistMn.mutateAsync(data.newTitle);
        setOpenDialog(false); 
    }

    const editPlaylistMn = useMutation({
        mutationKey: ['playlists', playlistId],
        mutationFn: async (playlistTitle: string) => {
            // TODO: Ok to build uri like this? 
            return await execute('PUT', `${protectedResources.playlistApi.endpoint}/${playlistId}`, {playlistTitle});
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['playlists'] });
        },
        onError: () => {
            console.log('Error editing playlist');
        }
    });

    const handleEditPlaylist = async () => {
        await editPlaylistMn.mutateAsync(playlistTitle);
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
                <EditIcon />
            </Button>
            <Dialog
                open={openDialog}
                onClose={handleCloseDialog}
            >
                <DialogTitle>
                    {'Edit Playlist'}
                </DialogTitle>
                <form onSubmit={handleSubmit(onSubmit)}>
                    <TextField
                        required
                        id='outline-required'
                        label='Playlist Title'
                        defaultValue={playlistTitle}
                        onChange={e => setPlaylistTitle(e.target.value)}
                        slotProps={{htmlInput:{minLength: 1, maxLength: 64}}}
                    />
                </form>
                <DialogActions>
                    <Button onClick={handleEditPlaylist}>Confirm</Button>
                    <Button onClick={handleCloseDialog}>Cancel</Button>
                </DialogActions>
            </Dialog>
        </>
    );
};

export default EditPlaylistDialog;