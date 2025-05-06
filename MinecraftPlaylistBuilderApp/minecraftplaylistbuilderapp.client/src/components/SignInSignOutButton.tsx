// CODE SOURCED FROM https://github.com/Azure-Samples/ms-identity-ciam-javascript-tutorial.git WITH MODIFICATION FOR USE IN THIS PROJECT

import { AuthenticatedTemplate, UnauthenticatedTemplate, useMsal } from '@azure/msal-react';
import { loginRequest } from '../utils/authConfig';
import { Button } from '@mui/material';

const SignInSignOutButton = () => {
    const { instance } = useMsal();

    let activeAccount;

    if (instance) {
        activeAccount = instance.getActiveAccount();
    };

    const handleLoginRedirect = () => {
        instance.loginRedirect(loginRequest)
            .catch((err) => console.log(err));
    };

    const handleLoginPopUp = () => {
        instance.loginPopup({
            ...loginRequest,
            redirectUri: 'auth-response'
        })
    };

    const handleLogoutRedirect = () => {
        instance.loginRedirect({
            account: instance.getActiveAccount(),
        });
    }

    const handleLogoutPopup = () => {
        instance.logoutPopup({
            mainWindowRedirectUri: '/',
            account: instance.getActiveAccount(),
        })
    };

    return (
        <>
            <UnauthenticatedTemplate>
                <Button onClick={handleLoginPopUp}>
                    Sign in using Popup
                </Button>
                <Button onClick={handleLoginRedirect}>
                    Sign in using Redirect
                </Button>
            </UnauthenticatedTemplate>
            <AuthenticatedTemplate>
                <Button onClick={handleLogoutPopup}>
                    Sign out using Popup
                </Button>
                <Button onClick={handleLogoutRedirect}>
                    Sign out using Redirect
                </Button>
            </AuthenticatedTemplate>
        </>
    )

}

export default SignInSignOutButton;