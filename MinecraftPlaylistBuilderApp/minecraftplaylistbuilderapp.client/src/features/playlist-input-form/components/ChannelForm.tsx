import { FormControl, FormGroup, FormHelperText } from "@mui/material"
import ChannelCheckbox from "./ChannelCheckbox"
import { Channel } from "../../../types/api"
import { ChangeEvent, useEffect, useState } from "react";

interface Props {
    channels: Channel[];
    onChange: ChangeEvent<HTMLInputElement>;
    error: boolean;
}

export const ChannelForm = ({ channels, onChange, error }: Props) => {

    const [isError, setIsError] = useState<boolean>(error)

    useEffect(() => {
        setIsError(error);
    }, [error]);

    return (
        <div style={{ overflowX: 'hidden', overflowY: 'auto', maxHeight: '75vh' }}>
            <FormControl required error={isError}>
                <FormHelperText>Channels (Pick between 1 and 5)</FormHelperText>
                <FormGroup id='channel-checkboxes' >
                    {channels.map((channel) => (
                        <ChannelCheckbox
                            channel={channel}
                            onChange={onChange}
                            key={channel.channelName}
                        />
                    ))}
                </FormGroup>
            </FormControl>
        </div>
    );
}