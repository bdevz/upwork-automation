import React from 'react';
import {
  Box,
  Button,
  Checkbox,
  FormControlLabel,
  FormGroup,
  Grid,
  TextField,
  Typography,
} from '@mui/material';

const SettingsPage: React.FC = () => {
  const [state, setState] = React.useState({
    enableAutomation: true,
    minRate: '50',
    jobTitleFilter: 'frontend, full stack, react',
  });

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setState({
      ...state,
      [event.target.name]: event.target.checked,
    });
  };

  const handleTextChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setState({
      ...state,
      [event.target.name]: event.target.value,
    });
  };

  const handleSave = () => {
    // In a real application, you would save the settings to a backend.
    console.log('Settings saved:', state);
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Typography variant="h6">Automation</Typography>
          <FormGroup>
            <FormControlLabel
              control={
                <Checkbox
                  checked={state.enableAutomation}
                  onChange={handleChange}
                  name="enableAutomation"
                />
              }
              label="Enable Automation"
            />
          </FormGroup>
        </Grid>
        <Grid item xs={12} md={6}>
          <Typography variant="h6">Job Filters</Typography>
          <TextField
            fullWidth
            label="Minimum Rate ($/hr)"
            name="minRate"
            value={state.minRate}
            onChange={handleTextChange}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Job Title Keywords (comma-separated)"
            name="jobTitleFilter"
            value={state.jobTitleFilter}
            onChange={handleTextChange}
            margin="normal"
          />
        </Grid>
        <Grid item xs={12}>
          <Button variant="contained" color="primary" onClick={handleSave}>
            Save Settings
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
};

export default SettingsPage;
