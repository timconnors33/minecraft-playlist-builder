import { FormControl, FormGroup, FormHelperText } from "@mui/material"
import ChannelCheckbox from "./ChannelCheckbox"
import { Channel, PlaylistFormInput } from "../../../types/api"
import { useEffect, useState } from "react";
import { Control, Controller } from "react-hook-form";

interface Props {
    channels: Channel[];
    control: Control<PlaylistFormInput>;
}

export const ChannelForm = ({ channels, control }: Props) => {
    return (
        <div style={{ overflowX: 'hidden', overflowY: 'auto', maxHeight: '75vh' }}>
            <FormControl required>
                <FormHelperText>Channels (Pick between 1 and 5)</FormHelperText>
                <FormGroup id='channel-checkboxes' >
                    <Controller
                        name='channels'
                        control={control}
                        rules={{
                            validate: value => {
                                return ((value.length >= 1) ? 
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