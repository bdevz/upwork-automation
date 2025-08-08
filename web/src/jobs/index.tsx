import React from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Box, Typography } from '@mui/material';

const columns: GridColDef[] = [
  { field: 'id', headerName: 'ID', width: 90 },
  {
    field: 'title',
    headerName: 'Title',
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
    field: 'created_at',
    headerName: 'Created At',
    type: 'dateTime',
    width: 180,
    editable: false,
    valueGetter: (value) => value && new Date(value),
  },
];

const rows = [
  { id: 1, title: 'Senior Frontend Developer', status: 'Applied', created_at: new Date().toISOString() },
  { id: 2, title: 'Full Stack Engineer', status: 'Pending', created_at: new Date().toISOString() },
  { id: 3, title: 'Backend Developer', status: 'Applied', created_at: new Date().toISOString() },
  { id: 4, title: 'DevOps Engineer', status: 'Rejected', created_at: new Date().toISOString() },
  { id: 5, title: 'UI/UX Designer', status: 'Pending', created_at: new Date().toISOString() },
];

const JobsPage: React.FC = () => {
  return (
    <Box sx={{ height: 400, width: '100%' }}>
      <Typography variant="h4" gutterBottom>
        Jobs
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

export default JobsPage;
