import React from 'react';
import { Tabs, Tab, Box } from '@mui/material';
import { ProjectHeader } from './ProjectHeader';
import { CompetitorList } from '../competitors/CompetitorList';
import { ProjectNotes } from './ProjectNotes';

export const ProjectDetails = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [project, setProject] = useState(null);

  return (
    <Box>
      <ProjectHeader project={project} />
      <Tabs value={activeTab} onChange={(e, v) => setActiveTab(v)}>
        <Tab label="Details" />
        <Tab label="Competitors" />
        <Tab label="Notes" />
        <Tab label="Service Areas" />
      </Tabs>
      {/* Tab panels can be added incrementally as backend support is completed */}
    </Box>
  );
}; 