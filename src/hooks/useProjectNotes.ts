import { useQuery, useMutation, useQueryClient } from 'react-query';
import { projectNotesApi } from '../api/projectNotes';
import { ProjectNote } from '../api/types';

export const useProjectNotes = (projectId: string) => {
  const queryClient = useQueryClient();
  const queryKey = ['projectNotes', projectId];

  const notesQuery = useQuery(queryKey, () => 
    projectNotesApi.getProjectNotes(projectId)
  );

  const createNoteMutation = useMutation(
    (data: Partial<ProjectNote>) => 
      projectNotesApi.createProjectNote(projectId, data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(queryKey);
      },
    }
  );

  const updateNoteMutation = useMutation(
    ({ id, data }: { id: number; data: Partial<ProjectNote> }) =>
      projectNotesApi.updateProjectNote(projectId, id, data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(queryKey);
      },
    }
  );

  const deleteNoteMutation = useMutation(
    (noteId: number) => projectNotesApi.deleteProjectNote(projectId, noteId),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(queryKey);
      },
    }
  );

  return {
    notes: notesQuery.data,
    isLoading: notesQuery.isLoading,
    createNote: createNoteMutation.mutate,
    updateNote: updateNoteMutation.mutate,
    deleteNote: deleteNoteMutation.mutate,
  };
}; 