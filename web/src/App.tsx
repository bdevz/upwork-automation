import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { QueryClient, QueryClientProvider } from 'react-query';

import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Jobs from './pages/Jobs';
import Applications from './pages/Applications';
import Settings from './pages/Settings';
import Analytics from './pages/Analytics';
import Controls from './pages/Controls';
import JobDetailPage from './pages/JobDetail';

// Create theme
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

// Create query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

const initialJobs = [
  { id: 1, title: 'Senior Frontend Developer', status: 'Applied', created_at: new Date().toISOString() },
  { id: 2, title: 'Full Stack Engineer', status: 'Pending', created_at: new Date().toISOString() },
  { id: 3, title: 'Backend Developer', status: 'Applied', created_at: new Date().toISOString() },
  { id: 4, title: 'DevOps Engineer', status: 'Rejected', created_at: new Date().toISOString() },
  { id: 5, title: 'UI/UX Designer', status: 'Pending', created_at: new Date().toISOString() },
];

function App() {
  const [jobs, setJobs] = useState(initialJobs);

  useEffect(() => {
    const interval = setInterval(() => {
      setJobs((prevJobs) => [
        ...prevJobs,
        {
          id: prevJobs.length + 1,
          title: `New Job ${prevJobs.length + 1}`,
          status: 'Pending',
          created_at: new Date().toISOString(),
        },
      ]);
    }, 5000); // Add a new job every 5 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/jobs" element={<Jobs jobs={jobs} />} />
              <Route path="/jobs/:id" element={<JobDetailPage />} />
              <Route path="/applications" element={<Applications />} />
              <Route path="/settings" element={<Settings />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/controls" element={<Controls />} />
            </Routes>
          </Layout>
        </Router>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
