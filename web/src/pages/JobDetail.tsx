import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Box,
  Button,
  Card,
  CardContent,
  Grid,
  TextField,
  Typography,
} from '@mui/material';

// Mock job data
const mockJobs = [
  { id: 1, title: 'Senior Frontend Developer', status: 'Applied', created_at: new Date().toISOString(), description: 'Looking for a skilled frontend developer to join our team.', proposal: 'I am a great fit for this role because...' },
  { id: 2, title: 'Full Stack Engineer', status: 'Pending', created_at: new Date().toISOString(), description: 'We need a full stack engineer with experience in React and Node.js.', proposal: '' },
  { id: 3, title: 'Backend Developer', status: 'Applied', created_at: new Date().toISOString(), description: 'Join our backend team and work with cutting-edge technologies.', proposal: 'My skills in backend development make me an ideal candidate.' },
];

const JobDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [job, setJob] = useState<any>(null);
  const [proposal, setProposal] = useState('');

  useEffect(() => {
    const jobId = parseInt(id || '', 10);
    const selectedJob = mockJobs.find((j) => j.id === jobId);
    if (selectedJob) {
      setJob(selectedJob);
      setProposal(selectedJob.proposal);
    }
  }, [id]);

  const handleProposalChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setProposal(event.target.value);
  };

  const handleSaveProposal = () => {
    console.log('Proposal saved:', proposal);
  };

  if (!job) {
    return <Typography>Job not found</Typography>;
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" gutterBottom>
        {job.title}
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6">Job Details</Typography>
              <Typography><strong>Status:</strong> {job.status}</Typography>
              <Typography><strong>Created At:</strong> {new Date(job.created_at).toLocaleString()}</Typography>
              <Typography sx={{ mt: 2 }}>{job.description}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6">Proposal</Typography>
              <TextField
                fullWidth
                multiline
                rows={8}
                value={proposal}
                onChange={handleProposalChange}
                margin="normal"
                variant="outlined"
              />
              <Button
                variant="contained"
                color="primary"
                onClick={handleSaveProposal}
                sx={{ mt: 2 }}
              >
                Save Proposal
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default JobDetailPage;
