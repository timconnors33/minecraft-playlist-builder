import { CircularProgress, Box } from "@mui/material";

const LoadingOverlay = () => (
    <Box
        sx={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100vw",
            height: "100vh",
            bgcolor: "rgba(0,0,0,0.4)",
            zIndex: 2000,
            display: "flex",
            alignItems: "center",
            justifyContent: "center"
        }}
    >
        <CircularProgress size={'100px'} thickness={2}/>
    </Box>
);

export default LoadingOverlay;