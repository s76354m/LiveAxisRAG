import axios from 'axios';
import { Competitor, CompetitorTranslation } from './types';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

export const competitorsApi = {
  async getProjectCompetitors(projectId: string): Promise<Competitor[]> {
    const response = await axios.get(`${API_BASE_URL}/projects/${projectId}/competitors`);
    return response.data;
  },

  async getCompetitorTranslations(projectId: string): Promise<CompetitorTranslation[]> {
    const response = await axios.get(
      `${API_BASE_URL}/projects/${projectId}/competitor-translations`
    );
    return response.data;
  },

  async createCompetitor(projectId: string, data: Partial<Competitor>): Promise<Competitor> {
    const response = await axios.post(
      `${API_BASE_URL}/projects/${projectId}/competitors`, 
      data
    );
    return response.data;
  },

  async updateCompetitor(
    projectId: string, 
    competitorId: number, 
    data: Partial<Competitor>
  ): Promise<Competitor> {
    const response = await axios.patch(
      `${API_BASE_URL}/projects/${projectId}/competitors/${competitorId}`, 
      data
    );
    return response.data;
  }
}; 