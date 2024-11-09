import { Dialog, DialogTitle, DialogContent, DialogActions, Button } from '@mui/material';
import { ProjectEditForm } from './ProjectEditForm';
import { Project, ProjectTranslation } from '../../api/types';
import { useProjectValidation } from '../../hooks/useProjectValidation';

interface ProjectEditDialogProps {
  open: boolean;
  onClose: () => void;
  project: Project;
  translation?: ProjectTranslation;
  onSubmit: (projectData: Partial<Project>, translationData: Partial<ProjectTranslation>) => void;
}

export const ProjectEditDialog = ({
  open,
  onClose,
  project,
  translation,
  onSubmit
}: ProjectEditDialogProps) => {
  const { validateProject, validateTranslation, errors } = useProjectValidation();

  const handleSubmit = (
    projectData: Partial<Project>, 
    translationData: Partial<ProjectTranslation>
  ) => {
    const projectErrors = validateProject(projectData);
    const translationErrors = validateTranslation(translationData);

    if (Object.keys(projectErrors).length === 0 && 
        Object.keys(translationErrors).length === 0) {
      onSubmit(projectData, translationData);
      onClose();
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>Edit Project Details</DialogTitle>
      <DialogContent>
        <ProjectEditForm
          project={project}
          translation={translation}
          onSubmit={handleSubmit}
          errors={errors}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
      </DialogActions>
    </Dialog>
  );
}; 