import { useState } from 'react';
import { useQuery } from 'react-query';
import { 
  DataGrid, 
  GridColDef,
  GridFilterModel,
  GridSortModel 
} from '@mui/x-data-grid';
import { Box, Button, Chip } from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { ProjectStatus } from '../../types';

const columns: GridColDef[] = [
  { 
    field: 'project_id', 
    headerName: 'Project ID', 
    width: 130,
    filterable: true 
  },
  { 
    field: 'region', 
    headerName: 'Region', 
    width: 150,
    filterable: true
  },
  {
    field: 'status',
    headerName: 'Status',
    width: 130,
    renderCell: (params) => (
      <Chip 
        label={params.value}
        color={params.value === 'Active' ? 'success' : 
              params.value === 'Pending' ? 'warning' : 'default'}
      />
    ),
    filterable: true
  },
  {
    field: 'created_at',
    headerName: 'Created',
    width: 180,
    valueFormatter: (params) => new Date(params.value).toLocaleString()
  },
  {
    field: 'created_by',
    headerName: 'Created By',
    width: 150
  }
];

export const ProjectList = () => {
  const [filterModel, setFilterModel] = useState<GridFilterModel>({
    items: []
  });
  const [sortModel, setSortModel] = useState<GridSortModel>([]);

  const { data, isLoading } = useQuery(['projects', filterModel, sortModel], 
    () => fetchProjects(filterModel, sortModel)
  );

  return (
    <Box sx={{ height: 600, width: '100%' }}>
      <Box sx={{ mb: 2, display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {/* TODO: Implement new project */}}
        >
          New Project
        </Button>
      </Box>
      <DataGrid
        rows={data || []}
        columns={columns}
        loading={isLoading}
        filterModel={filterModel}
        onFilterModelChange={setFilterModel}
        sortModel={sortModel}
        onSortModelChange={setSortModel}
        disableSelectionOnClick
      />
    </Box>
  );
}; 