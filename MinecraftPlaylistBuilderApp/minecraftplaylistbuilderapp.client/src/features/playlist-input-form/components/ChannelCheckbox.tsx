import { ChangeEvent, useState } from "react";
import { Channel } from "../../../types/api";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import DOMPurify from "dompurify";

interface Props {
    channel: Channel;
    isChecked: boolean;
    onChange: (event: ChangeEvent<HTMLInputElement>) => void;
}

const ChannelCheckbox = ({ channel, isChecked, onChange }: Props) => {
    const pureChannelName = DOMPurify.sanitize(channel.channelName);
    // https://upmostly.com/tutorials/how-to-checkbox-onchange-react-js
    return (
        <FormControlLabel
            control={
                // TODO: Do I need key here?
                <Checkbox name={pureChannelName} checked={isChecked} onChange={onChange}/>
            }
            label={pureChannelName}
        />
    )
}

export default ChannelCheckbox;