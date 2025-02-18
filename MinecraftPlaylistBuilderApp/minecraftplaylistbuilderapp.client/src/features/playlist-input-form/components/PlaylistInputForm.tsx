import { Checkbox, FormControlLabel, FormGroup, SelectChangeEvent } from "@mui/material";
import { useState, useEffect, SetStateAction } from "react";
import { Series, Season, Channel, SeasonAppearance } from "../../../interfaces/api-interfaces";
import SeasonSelect from "./SeasonSelect";
import SeriesSelect from "./SeriesSelect";
import '../PlaylistInputForm.css'

const BASE_URL = 'https://localhost:7258';

interface Props {
    seasonAppearance: SeasonAppearance;
}

interface SeasonAppearanceState {
    seriesList: Series[];
    selectedSeries: Series;
    seasons: Season[];
    selectedSeason: Season;
    channels: Channel[];
}

const PlaylistInputForm = ({seasonAppearance}: Props) => {
    const [seriesList, setSeriesList] = useState<Series[]>(seasonAppearance.series);
    // TODO: Check using undefined here
    const [selectedSeries, setSelectedSeries] = useState<Series>();

    const [seasons, setSeasons] = useState<Season[]>();
    const [selectedSeason, setSelectedSeason] = useState<Season>();

    const [channels, setChannels] = useState<Channel[]>();
    const [selectedChannels, setSelectedChannels] = useState<Channel[]>();

    const fetchSeasons = async (seriesTitle: string) => {
        try {
            const seasonsData = seasonAppearance.series.find((s: Series) => s.seriesTitle == seriesTitle)?.seasons;
            if (seasonsData === undefined) {
                throw new Error('Could not find season data');
            }
            seasonsData.sort((a: Season, b: Season) => a.seasonTitle.localeCompare(b.seasonTitle, undefined, { numeric: true, sensitivity: 'base' }))
            setSeasons(seasonsData);
        } catch (err) {
            console.log(err);
        }
    };

    const handleSeriesChange = (event: SelectChangeEvent) => {
        const selectedTitle = event.target.value as string;
        setSelectedSeries(seasonAppearance.series.find((series : Series) => series.seriesTitle === selectedTitle));
        setSeasons([]);
        setChannels([]);
        fetchSeasons(selectedTitle)
    };

    const handleSeasonChange = (event: SelectChangeEvent) => {
        if (selectedSeries) {
            const selectedTitle = event.target.value as string;
            setSelectedSeason(selectedSeries.seasons.find((season: Season) => season.seasonTitle === selectedTitle));
            setChannels([]);
        }
    };

    useEffect(() => {
        const fetchChannels = () => {
            try {
                if (selectedSeason) {
                    console.log(selectedSeason)
                    const channelsData = selectedSeason?.channels;
                    if (!channelsData) {
                        throw new Error('Could not find channel data');
                    }
                    channelsData.sort((a: Channel, b: Channel) => a.channelName.localeCompare(b.channelName, undefined, { numeric: true, sensitivity: 'base' }));
                    setChannels(channelsData);
                    console.log(channelsData)
                }
            } catch (err) {
                console.log(err);
            }
        };
        fetchChannels();
    }, [selectedSeason])

    return (
        <>
            <SeriesSelect
                seriesList={seriesList}
                selectedSeries={selectedSeries}
                onSeriesChange={handleSeriesChange}
            />
                <SeasonSelect
                    seasons={seasons}
                    selectedSeason={selectedSeason}
                    onSeasonChange={handleSeasonChange}
                />
            {channels && (
                <div>
                    <FormGroup id='channel-checkboxes' style={{overflowX: 'hidden', overflowY: 'auto'}}>
                        {channels.map((channel) => (
                            <FormControlLabel
                                control={
                                    <Checkbox name={channel.channelName} />
                                }
                                label={channel.channelName}
                            />
                        ))}
                    </FormGroup>
                </div>
            )}
        </>
    );
}

export default PlaylistInputForm;