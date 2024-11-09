import { useQuery, useMutation, useQueryClient } from 'react-query';
import { projectsApi } from '../api/projects';

export const useProject = (id: string) => {
  const queryClient = useQueryClient();

  const projectQuery = useQuery(['project', id], () => 
    projectsApi.getProject(id)
  );

  const translationQuery = useQuery(['projectTranslation', id], () =>
    projectsApi.getProjectTranslation(id)
  );

  const updateProjectMutation = useMutation(
    (data: Partial<Project>) => projectsApi.updateProject(id, data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['project', id]);
      },
    }
  );

  const updateTranslationMutation = useMutation(
    (data: Partial<ProjectTranslation>) => 
      projectsApi.updateProjectTranslation(id, data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['projectTranslation', id]);
      },
    }
  );

  return {
    project: projectQuery.data,
    translation: translationQuery.data,
    isLoading: projectQuery.isLoading || translationQuery.isLoading,
    updateProject: updateProjectMutation.mutate,
    updateTranslation: updateTranslationMutation.mutate,
  };
}; 