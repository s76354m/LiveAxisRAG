import { useState } from 'react';
import { 
  Box, TextField, FormControl, InputLabel, Select, MenuItem,
  Button, Grid, Paper, Typography 
} from '@mui/material';

interface ServiceArea {
  RecordID: number;
  ProjectID: string;
  Region: string;
  State: string;
  County: string;
  ReportInclude: string;
  MaxMileage: number;
  ProjectStatus: string;
}

interface ServiceAreaFormProps {
  projectId: string;
  serviceArea?: ServiceArea;
  onSubmit: (data: Partial<ServiceArea>) => Promise<void>;
}

export const ServiceAreaForm = ({ 
  projectId, 
  serviceArea, 
  onSubmit 
}: ServiceAreaFormProps) => {
  const [formData, setFormData] = useState<Partial<ServiceArea>>(
    serviceArea || {
      ProjectID: projectId,
      ReportInclude: 'Y',
      MaxMileage: 0
    }
  );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onSubmit(formData);
  };

  return (
    <Paper component="form" onSubmit={handleSubmit} sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Service Area Details
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="Region"
            value={formData.Region}
            onChange={(e) => setFormData({
              ...formData,
              Region: e.target.value
            })}
          />
        </Grid>
        
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="State"
            value={formData.State}
            onChange={(e) => setFormData({
              ...formData,
              State: e.target.value
            })}
            inputProps={{ maxLength: 2 }}
          />
        </Grid>
        
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="County"
            value={formData.County}
            onChange={(e) => setFormData({
              ...formData,
              County: e.target.value
            })}
          />
        </Grid>
        
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="Max Mileage"
            type="number"
            value={formData.MaxMileage}
            onChange={(e) => setFormData({
              ...formData,
              MaxMileage: parseInt(e.target.value, 10)
            })}
          />
        </Grid>
        
        <Grid item xs={12}>
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
            <Button type="submit" variant="contained" color="primary">
              Save Service Area
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Paper>
  );
}; 