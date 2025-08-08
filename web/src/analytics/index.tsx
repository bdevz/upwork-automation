import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
} from 'recharts';
import { Box, Grid, Paper, Typography } from '@mui/material';

const applicationsData = [
  { name: 'Jan', applications: 30 },
  { name: 'Feb', applications: 45 },
  { name: 'Mar', applications: 60 },
  { name: 'Apr', applications: 50 },
  { name: 'May', applications: 70 },
  { name: 'Jun', applications: 80 },
];

const jobsData = [
  { name: 'Frontend', count: 25 },
  { name: 'Backend', count: 40 },
  { name: 'Full Stack', count: 35 },
  { name: 'DevOps', count: 20 },
];

const AnalyticsPage: React.FC = () => {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" gutterBottom>
        Analytics
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 240 }}>
            <Typography variant="h6" gutterBottom>
              Applications Over Time
            </Typography>
            <ResponsiveContainer>
              <LineChart data={applicationsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="applications" stroke="#8884d8" activeDot={{ r: 8 }} />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 240 }}>
            <Typography variant="h6" gutterBottom>
              Jobs by Category
            </Typography>
            <ResponsiveContainer>
              <BarChart data={jobsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="count" fill="#82ca9d" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default AnalyticsPage;
