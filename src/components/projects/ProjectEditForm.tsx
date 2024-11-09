import { useState } from 'react';
import { 
  Box, 
  TextField, 
  Select, 
  MenuItem, 
  FormControl,
  InputLabel,
  Button,
  Grid,
  Paper,
  FormHelperText
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { Project, ProjectTranslation } from '../../api/types';

interface ProjectEditFormProps {
  project: Project;
  translation?: ProjectTranslation;
  onSubmit: (projectData: Partial<Project>, translationData: Partial<ProjectTranslation>) => void;
  errors: {
    project: Record<string, string>;
    translation: Record<string, string>;
  };
}

export const ProjectEditForm = ({ project, translation, onSubmit, errors }: ProjectEditFormProps) => {
  const [projectData, setProjectData] = useState<Partial<Project>>(project);
  const [translationData, setTranslationData] = useState<Partial<ProjectTranslation>>(
    translation || {}
  );

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(projectData, translationData);
  };

  return (
    <Paper component="form" onSubmit={handleSubmit} sx={{ p: 3 }}>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="Project ID"
            value={projectData.project_id}
            disabled
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <FormControl fullWidth>
            <InputLabel>Status</InputLabel>
            <Select
              value={projectData.status}
              onChange={(e) => setProjectData({
                ...projectData,
                status: e.target.value as Project['status']
              })}
            >
              <MenuItem value="Active">Active</MenuItem>
              <MenuItem value="Pending">Pending</MenuItem>
              <MenuItem value="Completed">Completed</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} md={6}>
          <FormControl fullWidth error={!!errors.project.region}>
            <TextField
              label="Region"
              value={projectData.region}
              onChange={(e) => setProjectData({
                ...projectData,
                region: e.target.value
              })}
              error={!!errors.project.region}
              helperText={errors.project.region}
            />
          </FormControl>
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="Analyst"
            value={translationData.Analyst}
            onChange={(e) => setTranslationData({
              ...translationData,
              Analyst: e.target.value
            })}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="Project Manager"
            value={translationData.PM}
            onChange={(e) => setTranslationData({
              ...translationData,
              PM: e.target.value
            })}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <FormControl fullWidth error={!!errors.translation.MaxMileage}>
            <TextField
              label="Max Mileage"
              type="number"
              value={translationData.MaxMileage}
              onChange={(e) => setTranslationData({
                ...translationData,
                MaxMileage: parseInt(e.target.value, 10)
              })}
              error={!!errors.translation.MaxMileage}
              helperText={errors.translation.MaxMileage}
            />
          </FormControl>
        </Grid>
        <Grid item xs={12}>
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
            <Button type="submit" variant="contained" color="primary">
              Save Changes
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Paper>
  );
}; 