import { Video } from "../../types/api";

const DEV_OAUTH2_CLIENT_ID = import.meta.env.VITE_REACT_APP_DEV_OAUTH2_CLIENT_ID;

const handleAuth = async (videos: Video[]) => {
    try {
        let tokenClient;
        const loadGapiClient = async () => {
            return new Promise((resolve, reject) => {
                if (!window.gapi) {
                    reject(new Error("Google API not loaded"));
                    return;
                }
                window.gapi.load('client', { callback: resolve, onerror: reject });
                console.log('Google API loaded');
            });
        };
        await loadGapiClient();
        await window.gapi.client.init({});
        await window.gapi.client.load('https://www.googleapis.com/discovery/v1/apis/youtube/v3/rest');

        tokenClient = window.google.accounts.oauth2.initTokenClient({
            client_id: DEV_OAUTH2_CLIENT_ID,
            scope: 'https://www.googleapis.com/auth/youtube',
            prompt: 'consent',
            callback: (tokenResponse) => {
                if (tokenResponse && tokenResponse.access_token) {
                    createPlaylist(videos);
                } else {
                    throw new Error('Did not get access token');
                }
            },
        });

        tokenClient.requestAccessToken();

    } catch (err) {
        console.log(err);
    }
}

const createPlaylist = async (videos: Video[]) => {

    const response = await window.gapi.client.youtube.playlists.insert({
        "part": [
            "snippet,status"
        ],
        "resource": {
            "snippet": {
                "title": "Custom Minecraft Playlist"
            },
            "status": {
                "privacyStatus": "private"
            }
        }
    });

    console.log(response);

    if (response.status !== 200) {
        throw new Error('Could not create YouTube playlist');
    }

    const playlistId = response.result.id;

    addVideosToPlaylist(videos, playlistId);
}

const addVideosToPlaylist = async (videos: Video[], playlistId: string) => {
    for (const video of videos) {
        const response = await window.gapi.client.youtube.playlistItems.insert({
            "part": [
                "snippet"
            ],
            "resource": {
                "snippet": {
                    "playlistId": playlistId,
                    "resourceId": {
                        "videoId": video.videoYouTubeId,
                        "kind": "youtube#video"
                    }
                }
            }
        });

        if (response.status !== 200) {
            throw new Error(`Could not insert video with ID of ${video.videoYouTubeId} into playlist`);
        }

        console.log(`Inserted video with ID of ${video.videoYouTubeId} into playlist`);
    }
}

export {handleAuth};