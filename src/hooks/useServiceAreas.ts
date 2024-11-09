import { useQuery, useMutation, useQueryClient } from 'react-query';
import { serviceAreaApi } from '../api/serviceAreas';
import { ServiceArea } from '../api/types';

export const useServiceAreas = (projectId: string) => {
  const queryClient = useQueryClient();
  const queryKey = ['serviceAreas', projectId];

  const { data: serviceAreas, isLoading, error } = useQuery(
    queryKey,
    () => serviceAreaApi.getServiceAreas(projectId)
  );

  const createMutation = useMutation(
    (data: Partial<ServiceArea>) => 
      serviceAreaApi.createServiceArea(projectId, data),
    {
      onMutate: async (newServiceArea) => {
        await queryClient.cancelQueries(queryKey);
        const previousServiceAreas = queryClient.getQueryData(queryKey);
        
        queryClient.setQueryData(queryKey, (old: ServiceArea[] = []) => [
          ...old,
          { ...newServiceArea, RecordID: Date.now() }
        ]);

        return { previousServiceAreas };
      },
      onError: (err, variables, context) => {
        queryClient.setQueryData(queryKey, context?.previousServiceAreas);
      },
      onSettled: () => {
        queryClient.invalidateQueries(queryKey);
      }
    }
  );

  const updateMutation = useMutation(
    ({ id, data }: { id: number; data: Partial<ServiceArea> }) =>
      serviceAreaApi.updateServiceArea(projectId, id, data),
    {
      onMutate: async ({ id, data }) => {
        await queryClient.cancelQueries(queryKey);
        const previousServiceAreas = queryClient.getQueryData(queryKey);

        queryClient.setQueryData(queryKey, (old: ServiceArea[] = []) =>
          old.map((item) =>
            item.RecordID === id ? { ...item, ...data } : item
          )
        );

        return { previousServiceAreas };
      },
      onError: (err, variables, context) => {
        queryClient.setQueryData(queryKey, context?.previousServiceAreas);
      },
      onSettled: () => {
        queryClient.invalidateQueries(queryKey);
      }
    }
  );

  return {
    serviceAreas,
    isLoading,
    error,
    createServiceArea: createMutation.mutate,
    updateServiceArea: updateMutation.mutate,
    isUpdating: createMutation.isLoading || updateMutation.isLoading
  };
}; 