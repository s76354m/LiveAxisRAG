import axios from 'axios';
import { ServiceArea } from './types';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

export const serviceAreaApi = {
  async getServiceAreas(projectId: string): Promise<ServiceArea[]> {
    const response = await axios.get(
      `${API_BASE_URL}/projects/${projectId}/service-areas`
    );
    return response.data;
  },

  async updateServiceArea(
    projectId: string,
    serviceAreaId: number,
    data: Partial<ServiceArea>
  ): Promise<ServiceArea> {
    const response = await axios.patch(
      `${API_BASE_URL}/projects/${projectId}/service-areas/${serviceAreaId}`,
      data
    );
    return response.data;
  },

  async createServiceArea(
    projectId: string,
    data: Partial<ServiceArea>
  ): Promise<ServiceArea> {
    const response = await axios.post(
      `${API_BASE_URL}/projects/${projectId}/service-areas`,
      data
    );
    return response.data;
  },

  async deleteServiceArea(
    projectId: string,
    serviceAreaId: number
  ): Promise<void> {
    await axios.delete(
      `${API_BASE_URL}/projects/${projectId}/service-areas/${serviceAreaId}`
    );
  }
}; 