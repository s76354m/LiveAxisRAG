import axios from 'axios';
import { ProjectNote } from './types';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

export const projectNotesApi = {
  async getProjectNotes(projectId: string): Promise<ProjectNote[]> {
    const response = await axios.get(
      `${API_BASE_URL}/projects/${projectId}/notes`
    );
    return response.data;
  },

  async createProjectNote(
    projectId: string, 
    data: Partial<ProjectNote>
  ): Promise<ProjectNote> {
    const response = await axios.post(
      `${API_BASE_URL}/projects/${projectId}/notes`,
      data
    );
    return response.data;
  },

  async updateProjectNote(
    projectId: string,
    noteId: number,
    data: Partial<ProjectNote>
  ): Promise<ProjectNote> {
    const response = await axios.patch(
      `${API_BASE_URL}/projects/${projectId}/notes/${noteId}`,
      data
    );
    return response.data;
  },

  async deleteProjectNote(
    projectId: string,
    noteId: number
  ): Promise<void> {
    await axios.delete(
      `${API_BASE_URL}/projects/${projectId}/notes/${noteId}`
    );
  }
}; 