import { FormControl, FormGroup, FormHelperText } from "@mui/material"
import ChannelCheckbox from "./ChannelCheckbox"
import { Channel, PlaylistFormInput } from "../../../types/api"
import { useEffect, useState } from "react";
import { Control, Controller } from "react-hook-form";

interface Props {
    channels: Channel[];
    error: boolean;
    control: Control<PlaylistFormInput>;
    name: string;
}

export const ChannelForm = ({ channels, error, control, name }: Props) => {

    const [isError, setIsError] = useState<boolean>(error);

    useEffect(() => {
        setIsError(error);
    }, [error]);

    return (
        <div style={{ overflowX: 'hidden', overflowY: 'auto', maxHeight: '75vh' }}>
            <FormControl required error={isError}>
                <FormHelperText>Channels (Pick between 1 and 5)</FormHelperText>
                <FormGroup id='channel-checkboxes' >
                    <Controller
                        name='channels'
                        control={control}
                        rules={{
                            // TODO: Change error message
                            //required: { value: true, message: "Channel is required" },
                            /* minLength: { value: 1, message: "Please select at least one channel" },
                            maxLength: { value: 5, message: "You may only select up to 5 channels" }, */
                            validate: value => {
                                return ((value.length > 1) ? 
                                (value.length <= 5 || 'You may only select up to 5 channels') :
                                'Please select at least 1 channel')
                            },
                        }}
                        render={({field}) =>
                            <>
                                {channels.map((channel) => (
                                    <ChannelCheckbox
                                        isChecked={field.value?.includes(channel.channelName)}
                                        channel={channel}
                                        key={channel.channelName}
                                        name={channel.channelName}
                                        onChange={(event) => {
                                            const isChecked: boolean = event.target.checked;
                                            const valueArray = field.value || [];
                                            if (isChecked) {
                                                field.onChange([...valueArray, channel.channelName]);
                                            } else {
                                                field.onChange(valueArray.filter((name: string) => name !== channel.channelName));
                                            }
                                        }}
                                    />
                                ))}
                            </>
                        }
                    />
                </FormGroup>
            </FormControl>
        </div>
    );
}