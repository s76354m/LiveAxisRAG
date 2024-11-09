import { useQuery, useMutation, useQueryClient } from 'react-query';
import { competitorsApi } from '../api/competitors';
import { Competitor } from '../api/types';

export const useCompetitors = (projectId: string) => {
  const queryClient = useQueryClient();

  const competitorsQuery = useQuery(
    ['competitors', projectId], 
    () => competitorsApi.getProjectCompetitors(projectId)
  );

  const translationsQuery = useQuery(
    ['competitorTranslations', projectId],
    () => competitorsApi.getCompetitorTranslations(projectId)
  );

  const createCompetitorMutation = useMutation(
    (data: Partial<Competitor>) => competitorsApi.createCompetitor(projectId, data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['competitors', projectId]);
      },
    }
  );

  const updateCompetitorMutation = useMutation(
    ({ id, data }: { id: number; data: Partial<Competitor> }) =>
      competitorsApi.updateCompetitor(projectId, id, data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['competitors', projectId]);
      },
    }
  );

  return {
    competitors: competitorsQuery.data,
    translations: translationsQuery.data,
    isLoading: competitorsQuery.isLoading || translationsQuery.isLoading,
    createCompetitor: createCompetitorMutation.mutate,
    updateCompetitor: updateCompetitorMutation.mutate,
  };
}; 