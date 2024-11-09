import { Box, Grid, Paper, Typography } from '@mui/material';
import { format } from 'date-fns';
import { Project, ProjectTranslation } from '../../types';

interface ProjectDetailsTabProps {
  project: Project;
  translation?: ProjectTranslation;
}

export const ProjectDetailsTab = ({ project, translation }: ProjectDetailsTabProps) => {
  const formatDate = (date: string | null) => {
    if (!date) return 'N/A';
    return format(new Date(date), 'MM/dd/yyyy');
  };

  return (
    <Box>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Project Information
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <Typography color="textSecondary">Project ID</Typography>
                <Typography variant="body1">{project.project_id}</Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography color="textSecondary">Region</Typography>
                <Typography variant="body1">{project.region}</Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography color="textSecondary">Created By</Typography>
                <Typography variant="body1">{project.created_by}</Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography color="textSecondary">Created At</Typography>
                <Typography variant="body1">
                  {formatDate(project.created_at)}
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Translation Details
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <Typography color="textSecondary">Benchmark File ID</Typography>
                <Typography variant="body1">
                  {translation?.BenchmarkFileID || 'N/A'}
                </Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography color="textSecondary">Project Type</Typography>
                <Typography variant="body1">
                  {translation?.ProjectType || 'N/A'}
                </Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography color="textSecondary">Analyst</Typography>
                <Typography variant="body1">
                  {translation?.Analyst || 'N/A'}
                </Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography color="textSecondary">Project Manager</Typography>
                <Typography variant="body1">
                  {translation?.PM || 'N/A'}
                </Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography color="textSecondary">Go Live Date</Typography>
                <Typography variant="body1">
                  {formatDate(translation?.GoLiveDate)}
                </Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography color="textSecondary">Max Mileage</Typography>
                <Typography variant="body1">
                  {translation?.MaxMileage || 'N/A'}
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}; 