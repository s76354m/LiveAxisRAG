import React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { ProjectStatus } from '../../types';

const columns = [
  { field: 'project_id', headerName: 'Project ID', width: 130 },
  { field: 'region', headerName: 'Region', width: 130 },
  { field: 'status', headerName: 'Status', width: 130,
    renderCell: (params) => (
      <StatusChip status={params.value as ProjectStatus} />
    )
  },
  { field: 'created_at', headerName: 'Created', width: 130,
    valueFormatter: (params) => new Date(params.value).toLocaleDateString()
  },
  { field: 'created_by', headerName: 'Created By', width: 130 }
];

export const ProjectList = () => {
  const [projects, setProjects] = useState([]);
  
  useEffect(() => {
    // Fetch projects from API
    // This can be implemented incrementally as backend endpoints are completed
  }, []);

  return (
    <DataGrid
      rows={projects}
      columns={columns}
      pageSize={10}
      checkboxSelection
      disableSelectionOnClick
    />
  );
}; 