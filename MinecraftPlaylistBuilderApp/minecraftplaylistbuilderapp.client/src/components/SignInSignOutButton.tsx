// CODE SOURCED FROM https://github.com/Azure-Samples/ms-identity-ciam-javascript-tutorial.git WITH MODIFICATION FOR USE IN THIS PROJECT

import { AuthenticatedTemplate, UnauthenticatedTemplate, useMsal } from '@azure/msal-react';
import { loginRequest, protectedResources } from '../utils/authConfig';
import { Button } from '@mui/material';
import LoginIcon from '@mui/icons-material/Login';
import LogoutIcon from '@mui/icons-material/Logout';
import { BASE_CLIENT_URL } from '../utils/config';

const SignInSignOutButton = () => {

    const { instance } = useMsal();

    let activeAccount;

    if (instance) {
        activeAccount = instance.getActiveAccount();
    };

    const handleLoginRedirect = () => {
        try {
            instance.loginRedirect(loginRequest)
        } catch (err) {
            console.log(err);
        }
    };

    const handleLoginPopUp = () => {
        instance.loginPopup({
            ...loginRequest,
            redirectUri: `${BASE_CLIENT_URL}/auth-response`
        })
    };

    const handleLogoutRedirect = () => {
        instance.logoutRedirect({
            account: instance.getActiveAccount(),
        });
    };

    const handleLogoutPopup = () => {
        instance.logoutPopup({
            mainWindowRedirectUri: `${BASE_CLIENT_URL}/`,
            account: instance.getActiveAccount(),
        })
    };

    return (
        <>
            <UnauthenticatedTemplate>
                <Button onClick={handleLoginRedirect}>
                    <LoginIcon />
                </Button>
            </UnauthenticatedTemplate>
            <AuthenticatedTemplate>
                <Button onClick={handleLogoutRedirect}>
                    <LogoutIcon />
                </Button>
            </AuthenticatedTemplate>
        </>
    )

}

export default SignInSignOutButton;