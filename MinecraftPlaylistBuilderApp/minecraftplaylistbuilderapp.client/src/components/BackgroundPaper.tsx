import { Paper } from "@mui/material";

// https://stackoverflow.com/questions/55129942/typescript-styled-component-error-type-children-string-has-no-properti
export const BackgroundPaper: React.FC<React.PropsWithChildren> = ({children}) => {
    return (
        <Paper elevation={1} style={{flex: '1 1 auto', padding: '10px', marginBottom: '10px'}}>
            {children}
        </Paper>
    );
}