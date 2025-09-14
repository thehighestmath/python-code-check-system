import api from './api.ts';

export interface Solution {
  id: number;
  student_id: number;
  task_id: number;
  source_code: string;
  is_accepted: boolean;
  error_message?: string;
  created_at: string;
  updated_at?: string;
  task?: {
    id: number;
    name: string;
    complexity: string;
  };
}

export interface SolutionCreate {
  source_code: string;
  task_id: number;
}

export const solutionService = {
  async getSolutions(): Promise<Solution[]> {
    const response = await api.get('/solutions');
    return response.data;
  },

  async getSolution(id: number): Promise<Solution> {
    const response = await api.get(`/solutions/${id}`);
    return response.data;
  },

  async createSolution(solution: SolutionCreate): Promise<Solution> {
    const response = await api.post('/solutions', solution);
    return response.data;
  },

  async updateSolution(id: number, solution: Partial<SolutionCreate>): Promise<Solution> {
    const response = await api.put(`/solutions/${id}`, solution);
    return response.data;
  },

  async deleteSolution(id: number): Promise<void> {
    await api.delete(`/solutions/${id}`);
  },
};
