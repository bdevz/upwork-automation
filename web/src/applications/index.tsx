import React from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Box, Typography } from '@mui/material';

const columns: GridColDef[] = [
  { field: 'id', headerName: 'ID', width: 90 },
  {
    field: 'job_title',
    headerName: 'Job Title',
    width: 300,
    editable: false,
  },
  {
    field: 'status',
    headerName: 'Status',
    width: 150,
    editable: false,
  },
  {
    field: 'applied_at',
    headerName: 'Applied At',
    type: 'dateTime',
    width: 180,
    editable: false,
    valueGetter: (value) => value && new Date(value),
  },
];

const rows = [
  { id: 1, job_title: 'Senior Frontend Developer', status: 'Submitted', applied_at: new Date().toISOString() },
  { id: 2, job_title: 'Full Stack Engineer', status: 'Viewed', applied_at: new Date().toISOString() },
  { id: 3, job_title: 'Backend Developer', status: 'Rejected', applied_at: new Date().toISOString() },
  { id: 4, job_title: 'DevOps Engineer', status: 'Submitted', applied_at: new Date().toISOString() },
  { id: 5, job_title: 'UI/UX Designer', status: 'Viewed', applied_at: new Date().toISOString() },
];

const ApplicationsPage: React.FC = () => {
  return (
    <Box sx={{ height: 400, width: '100%' }}>
      <Typography variant="h4" gutterBottom>
        Applications
      </Typography>
      <DataGrid
        rows={rows}
        columns={columns}
        initialState={{
          pagination: {
            paginationModel: {
              pageSize: 5,
            },
          },
        }}
        pageSizeOptions={[5]}
        checkboxSelection
        disableRowSelectionOnClick
      />
    </Box>
  );
};

export default ApplicationsPage;
