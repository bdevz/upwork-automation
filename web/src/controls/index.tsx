import React, { useState } from 'react';
import {
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Grid,
  Typography,
} from '@mui/material';

const ControlsPage: React.FC = () => {
  const [open, setOpen] = useState(false);

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleEmergencyStop = () => {
    // In a real application, you would send a request to the backend to stop the system.
    console.log('Emergency stop initiated!');
    handleClose();
  };

  const handlePause = () => {
    console.log('System paused');
  };

  const handleResume = () => {
    console.log('System resumed');
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" gutterBottom>
        Manual Controls
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Typography variant="h6">System Control</Typography>
          <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
            <Button variant="contained" color="primary" onClick={handlePause}>
              Pause Automation
            </Button>
            <Button variant="contained" color="secondary" onClick={handleResume}>
              Resume Automation
            </Button>
          </Box>
        </Grid>
        <Grid item xs={12}>
          <Typography variant="h6">Emergency</Typography>
          <Button variant="contained" color="error" onClick={handleOpen}>
            Emergency Stop
          </Button>
          <Dialog open={open} onClose={handleClose}>
            <DialogTitle>{'Confirm Emergency Stop'}</DialogTitle>
            <DialogContent>
              <DialogContentText>
                Are you sure you want to perform an emergency stop? This action is irreversible and will halt all system operations immediately.
              </DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button onClick={handleClose}>Cancel</Button>
              <Button onClick={handleEmergencyStop} color="error" autoFocus>
                Confirm
              </Button>
            </DialogActions>
          </Dialog>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ControlsPage;
