import { ChangeEvent, useState } from "react";
import { Channel } from "../../../interfaces/api-interfaces";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";

interface Props {
    channel: Channel;
    onChange: (event: ChangeEvent<HTMLInputElement>) => void;
}

const ChannelCheckbox = ({ channel, onChange }: Props) => {
    // https://upmostly.com/tutorials/how-to-checkbox-onchange-react-js
    return (
        <FormControlLabel
            control={
                // TODO: Do I need key here?
                <Checkbox name={channel.channelName} onChange={onChange} key={channel.channelName}/>
            }
            label={channel.channelName}
        />
    )
}

export default ChannelCheckbox;