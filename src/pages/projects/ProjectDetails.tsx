import { useState } from 'react';
import { useQuery } from 'react-query';
import { useParams } from 'react-router-dom';
import { 
  Box, 
  Tabs, 
  Tab, 
  Paper, 
  Typography,
  Grid,
  Chip
} from '@mui/material';
import { ProjectNotes } from './ProjectNotes';
import { CompetitorList } from '../competitors/CompetitorList';
import { ServiceAreas } from './ServiceAreas';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

const TabPanel = (props: TabPanelProps) => {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
};

export const ProjectDetails = () => {
  const { id } = useParams();
  const [tabValue, setTabValue] = useState(0);
  
  const { data: project, isLoading } = useQuery(['project', id], 
    () => fetchProjectDetails(id)
  );
  
  const { data: translation } = useQuery(['projectTranslation', id],
    () => fetchProjectTranslation(id)
  );

  if (isLoading) return <div>Loading...</div>;
  if (!project) return <div>Project not found</div>;

  return (
    <Box sx={{ width: '100%' }}>
      <Paper sx={{ p: 2, mb: 2 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Typography variant="h6">
              Project {project.project_id}
            </Typography>
            <Typography color="textSecondary">
              {translation?.ProjectDesc}
            </Typography>
          </Grid>
          <Grid item xs={12} md={6} sx={{ textAlign: 'right' }}>
            <Chip 
              label={project.status}
              color={project.status === 'Active' ? 'success' : 
                     project.status === 'Pending' ? 'warning' : 'default'}
            />
          </Grid>
        </Grid>
      </Paper>

      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)}>
          <Tab label="Details" />
          <Tab label="Competitors" />
          <Tab label="Notes" />
          <Tab label="Service Areas" />
        </Tabs>
      </Box>

      <TabPanel value={tabValue} index={0}>
        <ProjectDetailsTab project={project} translation={translation} />
      </TabPanel>
      <TabPanel value={tabValue} index={1}>
        <CompetitorList projectId={id} />
      </TabPanel>
      <TabPanel value={tabValue} index={2}>
        <ProjectNotes projectId={id} />
      </TabPanel>
      <TabPanel value={tabValue} index={3}>
        <ServiceAreas projectId={id} />
      </TabPanel>
    </Box>
  );
}; 