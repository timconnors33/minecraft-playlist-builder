// CODE SOURCED FROM https://github.com/Azure-Samples/ms-identity-ciam-javascript-tutorial.git WITH MODIFICATION FOR USE IN THIS PROJECT

/*
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Licensed under the MIT License.
 */

import { LogLevel } from "@azure/msal-browser";

/**
 * Configuration object to be passed to MSAL instance on creation.
 * For a full list of MSAL.js configuration parameters, visit:
 * https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/configuration.md
 */
export const msalConfig = {
    auth: {
        clientId: '5449bd54-0d95-4bde-a7dc-051ce631d03b', // This is the ONLY mandatory field that you need to supply.
        authority: 'https://MinecraftPlaylistBuilder.ciamlogin.com/', // Replace the placeholder with your tenant subdomain
        redirectUri: 'https://localhost:51252/auth-response', // You must register this URI on Microsoft Entra admin center/App Registration. Defaults to window.location.origin
        postLogoutRedirectUri: 'https://localhost:51252', // Indicates the page to navigate after logout.
    },
    cache: {
        cacheLocation: 'localStorage', // Configures cache location. "sessionStorage" is more secure, but "localStorage" gives you SSO between tabs.
        storeAuthStateInCookie: false, // Set this to "true" if you are having issues on IE11 or Edge
    },
    system: {
        loggerOptions: {
            /**
             * Below you can configure MSAL.js logs. For more information, visit:
             * https://docs.microsoft.com/azure/active-directory/develop/msal-logging-js
             */
            loggerCallback: (level: LogLevel, message: string, containsPii: boolean) => {
                if (containsPii) {
                    return;
                }
                switch (level) {
                    case LogLevel.Error:
                        console.error(message);
                        return;
                    case LogLevel.Info:
                        console.info(message);
                        return;
                    case LogLevel.Verbose:
                        console.debug(message);
                        return;
                    case LogLevel.Warning:
                        console.warn(message);
                        return;
                    default:
                        return;
                }
            },
        },
    },
};

/**
 * Add here the endpoints and scopes when obtaining an access token for protected web APIs. For more information, see:
 * https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/resources-and-scopes.md
 */
export const protectedResources = {
    playlistApi: {
        endpoint: '/api/playlists',
        scopes: {
            read: 'api://922e867f-85d5-4f76-b6fd-eb78206a06f3/Playlists.Read',
            write: 'api://922e867f-85d5-4f76-b6fd-eb78206a06f3/Playlists.ReadWrite',
        },
    },
    playlistVideoApi: {
        scopes: {
            read: 'api://922e867f-85d5-4f76-b6fd-eb78206a06f3/PlaylistVideos.Read',
            write: 'api://922e867f-85d5-4f76-b6fd-eb78206a06f3/PlaylistVideos.ReadWrite',
        },
    },
};

/**
 * Scopes you add here will be prompted for user consent during sign-in.
 * By default, MSAL.js will add OIDC scopes (openid, profile, email) to any login request.
 * For more information about OIDC scopes, visit:
 * https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-permissions-and-consent#openid-connect-scopes
 */
export const loginRequest = {
    scopes: [protectedResources.playlistApi.scopes.read, protectedResources.playlistApi.scopes.write],
};
