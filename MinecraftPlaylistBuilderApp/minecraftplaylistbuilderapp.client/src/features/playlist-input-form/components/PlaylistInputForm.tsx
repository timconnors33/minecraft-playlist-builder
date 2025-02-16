import { Checkbox, FormControlLabel, FormGroup, SelectChangeEvent } from "@mui/material";
import { useState, useEffect, SetStateAction } from "react";
import { Series, Season, Channel, SeasonAppearance } from "../../../interfaces/api-interfaces";
import SeasonSelect from "./SeasonSelect";
import SeriesSelect from "./SeriesSelect";

const BASE_URL = 'https://localhost:7258';

const fetchSeasonAppearance = async (): Promise<SeasonAppearance> => {
    const response = await fetch(`${BASE_URL}/api/seasonappearances`)
    if (!response.ok) {
        throw new Error('Failed to fetch season appearance data');
    }
    const seasonAppearanceData: SeasonAppearance = await response.json();
    console.log('Fetched season appearance data');
    return seasonAppearanceData;
}

const seasonAppearanceData: SeasonAppearance = await fetchSeasonAppearance();

const PlaylistInputForm = () => {
    const [seriesList, setSeriesList] = useState<Series[]>();
    // TODO: Check using undefined here
    const [selectedSeries, setSelectedSeries] = useState<string>();

    const [seasons, setSeasons] = useState<Season[]>();
    const [selectedSeason, setSelectedSeason] = useState<string>();

    const [channels, setChannels] = useState<Channel[]>();
    const [selectedChannels, setSelectedChannels] = useState<Channel[]>();

    const [seasonAppearance, setSeasonAppearance] = useState<SeasonAppearance>(seasonAppearanceData);

    const populateSeriesListData = () => {
        console.log(`Series: ${seasonAppearance.series}`);
        setSeriesList(seasonAppearance.series);
    }

    const fetchSeasons = async (seriesTitle: string) => {
        try {
            const seasonsData = seasonAppearance.series.find((s: Series) => s.seriesTitle == seriesTitle)?.seasons;
            seasonsData.sort((a: Season, b: Season) => a.seasonTitle.localeCompare(b.seasonTitle, undefined, { numeric: true, sensitivity: 'base' }))
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

    const fetchChannels = (seriesTitle: string, seasonTitle: string) => {
        try {
            const channelsData = seasonAppearance.series.find((series: Series) => series.seriesTitle == seriesTitle).seasons.find((season: Season) => season.seasonTitle == seasonTitle).channels;
            channelsData.sort((a: Channel, b: Channel) => a.channelName.localeCompare(b.channelName, undefined, { numeric: true, sensitivity: 'base' }));
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