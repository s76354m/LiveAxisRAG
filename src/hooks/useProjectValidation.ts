import { Project, ProjectTranslation } from '../api/types';

interface ValidationErrors {
  project: Record<string, string>;
  translation: Record<string, string>;
}

export const useProjectValidation = () => {
  const validateProject = (data: Partial<Project>) => {
    const errors: Record<string, string> = {};

    if (!data.region?.trim()) {
      errors.region = 'Region is required';
    }

    if (!data.status) {
      errors.status = 'Status is required';
    }

    return errors;
  };

  const validateTranslation = (data: Partial<ProjectTranslation>) => {
    const errors: Record<string, string> = {};

    if (data.MaxMileage && (data.MaxMileage < 0 || data.MaxMileage > 100)) {
      errors.MaxMileage = 'Mileage must be between 0 and 100';
    }

    if (data.Analyst && data.Analyst.length > 30) {
      errors.Analyst = 'Analyst name must be 30 characters or less';
    }

    if (data.PM && data.PM.length > 30) {
      errors.PM = 'Project Manager name must be 30 characters or less';
    }

    return errors;
  };

  return {
    validateProject,
    validateTranslation,
    errors: { project: {}, translation: {} } as ValidationErrors
  };
}; 