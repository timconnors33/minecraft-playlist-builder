import { Checkbox, FormControlLabel, FormGroup, SelectChangeEvent } from "@mui/material";
import { useState, useEffect } from "react";
import { Series, Season, Channel } from "../../../interfaces/api-interfaces";
import SeasonSelect from "./SeasonSelect";
import SeriesSelect from "./SeriesSelect";


const PlaylistInputForm = () => {
    const[seriesList, setSeriesList] = useState<Series[]>([]);
    // TODO: Check using undefined here
    const[selectedSeries, setSelectedSeries] = useState<string>();
    
    const[seasons, setSeasons] = useState<Season[]>();
    const [selectedSeason, setSelectedSeason] = useState<string>();

    const [channels, setChannels] = useState<Channel[]>();
    const [selectedChannels, setSelectedChannels] = useState<Channel[]>();
    

    const populateSeriesListData = async () => {
        const response = await fetch('https://localhost:7258/api/series');
        if (response.ok) {
            const seriesListData = await response.json();
            setSeriesList(seriesListData);
        }
    }

    const fetchSeasons = async (seriesTitle: string) => {
        try {
            const response = await fetch(`https://localhost:7258/api/series/${seriesTitle}/seasons`);
            if (!response.ok) {
                throw new Error('Failed to fetch seasons');
            }
            const seasonsData = await response.json();
            seasonsData.sort((a: Season, b: Season) => a.seasonTitle.localeCompare(b.seasonTitle, undefined, { numeric : true, sensitivity: 'base'}))
            setSeasons(seasonsData);
        } catch (err) {
            console.log(err);
        }
    }

    const handleSeriesChange = (event: SelectChangeEvent) => {
        const selectedTitle = event.target.value as string;
        setSelectedSeries(selectedTitle);
        setSeasons([]);
        setChannels([]);
        fetchSeasons(selectedTitle)
    }

    const handleSeasonChange = (event: SelectChangeEvent) => {
        const selectedTitle = event.target.value as string;
        setSelectedSeason(selectedTitle);
        setChannels([]);
        fetchChannels(selectedSeries, selectedSeason);
    }

    const fetchChannels = async (seriesTitle: string, seasonTitle: string) => {
        try {
            const response = await fetch(`https://localhost:7258/api/series/${seriesTitle}/seasons/${seasonTitle}/channels`)
            const channelsData = await response.json();
            channelsData.sort((a: Channel, b: Channel) => a.channelName.localeCompare(b.channelName, undefined, {numeric: true, sensitivity: 'base'}))
            setChannels(channelsData);
        } catch (err) {
            console.log(err);
        }
    }

    useEffect(() => {
        populateSeriesListData();
    }, []);
    
    return (
        <>
            <SeriesSelect 
                seriesList={seriesList}
                selectedSeries={selectedSeries}
                onSeriesChange={handleSeriesChange}
            />
            {selectedSeries && (
                <SeasonSelect
                    seasons={seasons}
                    selectedSeason={selectedSeason}
                    onSeasonChange={handleSeasonChange}
                />
            )}
            {selectedSeason && (
                <div>
                    <FormGroup>
                        {channels?.map((channel) => (
                            <FormControlLabel
                                control = {
                                    <Checkbox name={channel.channelName}/>
                                }
                                label = {channel.channelName}
                            />
                        ))}
                    </FormGroup>
                </div>
            )}
        </>
    );
}

export default PlaylistInputForm;