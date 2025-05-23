// CODE SOURCED FROM https://github.com/Azure-Samples/ms-identity-ciam-javascript-tutorial.git WITH MODIFICATION FOR USE IN THIS PROJECT

import {
    useState,
    useCallback,
} from 'react';

import { InteractionType } from '@azure/msal-browser';
import { useMsal, useMsalAuthentication } from "@azure/msal-react";

const BASE_API_URL: string = 'https://localhost:7258';
const BASE_CLIENT_URL: string = 'https://localhost:51252';

/**
 * Custom hook to call a web API using bearer token obtained from MSAL
 * @param {PopupRequest} msalRequest 
 * @returns 
 */
const useFetchWithMsal = (msalRequest) => {
    const { instance } = useMsal();
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [data, setData] = useState(null);

    const { result, error: msalError } = useMsalAuthentication(InteractionType.Popup, {
        ...msalRequest,
        account: instance.getActiveAccount(),
        redirectUri: `${BASE_CLIENT_URL}/auth-response`
    });

    /**
     * Execute a fetch request with the given options
     * @param {string} method: GET, POST, PUT, DELETE
     * @param {String} endpoint: The endpoint to call
     * @param {Object} data: The data to send to the endpoint, if any 
     * @returns JSON response
     */
    const execute = async (method: string, endpoint: string, data: object | null = null) => {
        if (msalError) {
            setError(msalError);
            return;
        }

        if (result) {
            try {
                let response = null;

                const headers = new Headers();
                const bearer = `Bearer ${result.accessToken}`;
                headers.append("Authorization", bearer);

                if (data) headers.append('Content-Type', 'application/json');

                let options = {
                    method: method,
                    headers: headers,
                    body: data ? JSON.stringify(data) : null,
                };

                setIsLoading(true);
                response = (await fetch(`${BASE_API_URL}${endpoint}`, options));

                if ((response.status === 200 || response.status === 201)) {
                    let responseData = response;

                    try {
                        responseData = await response.json();
                    } catch (error) {
                        console.log(error);
                    } finally {
                        setData(responseData);
                        setIsLoading(false);
                        return responseData;
                    }
                }

                setIsLoading(false);
                return response;
            } catch (e) {
                setError(e);
                setIsLoading(false);
                throw e;
            }
        }
    };

    return {
        isLoading,
        error,
        data,
        execute: useCallback(execute, [result, msalError]), // to avoid infinite calls when inside a `useEffect`
        result,
    };
};

export default useFetchWithMsal;