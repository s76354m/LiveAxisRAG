import axios from 'axios';
import { Project, ProjectTranslation } from './types';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

export const projectsApi = {
  async getProject(id: string): Promise<Project> {
    const response = await axios.get(`${API_BASE_URL}/projects/${id}`);
    return response.data;
  },

  async getProjectTranslation(id: string): Promise<ProjectTranslation> {
    const response = await axios.get(`${API_BASE_URL}/projects/${id}/translation`);
    return response.data;
  },

  async updateProject(id: string, data: Partial<Project>): Promise<Project> {
    const response = await axios.patch(`${API_BASE_URL}/projects/${id}`, data);
    return response.data;
  },

  async updateProjectTranslation(
    id: string, 
    data: Partial<ProjectTranslation>
  ): Promise<ProjectTranslation> {
    const response = await axios.patch(
      `${API_BASE_URL}/projects/${id}/translation`, 
      data
    );
    return response.data;
  }
}; 