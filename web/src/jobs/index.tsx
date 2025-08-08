import React from 'react';
import { DataGrid, GridColDef, GridRenderCellParams } from '@mui/x-data-grid';
import { Box, Typography } from '@mui/material';
import { Link } from 'react-router-dom';

const columns: GridColDef[] = [
  { field: 'id', headerName: 'ID', width: 90 },
  {
    field: 'title',
    headerName: 'Title',
    width: 300,
    renderCell: (params: GridRenderCellParams) => (
      <Link to={`/jobs/${params.id}`}>{params.value}</Link>
    ),
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

interface Job {
  id: number;
  title: string;
  status: string;
  created_at: string;
}

interface JobsPageProps {
  jobs: Job[];
}

const JobsPage: React.FC<JobsPageProps> = ({ jobs }) => {
  return (
    <Box sx={{ height: 400, width: '100%' }}>
      <Typography variant="h4" gutterBottom>
        Jobs
      </Typography>
      <DataGrid
        rows={jobs}
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
