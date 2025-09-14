import api from './api.ts';

export interface Test {
  id: number;
  task_id: number;
  input_data: string;
  output_data: string;
  created_at: string;
}

export interface Task {
  id: number;
  name: string;
  description: string;
  complexity: 'easy' | 'medium' | 'hard';
  is_active: boolean;
  created_at: string;
  updated_at?: string;
  tests: Test[];
}

export interface TaskCreate {
  name: string;
  description: string;
  complexity: 'easy' | 'medium' | 'hard';
  is_active: boolean;
  tests: {
    input_data: string;
    output_data: string;
  }[];
}

export const taskService = {
  async getTasks(isActive: boolean = true): Promise<Task[]> {
    const response = await api.get(`/tasks?is_active=${isActive}`);
    return response.data;
  },

  async getTask(id: number): Promise<Task> {
    const response = await api.get(`/tasks/${id}`);
    return response.data;
  },

  async createTask(task: TaskCreate): Promise<Task> {
    const response = await api.post('/tasks', task);
    return response.data;
  },

  async updateTask(id: number, task: Partial<TaskCreate>): Promise<Task> {
    const response = await api.put(`/tasks/${id}`, task);
    return response.data;
  },

  async deleteTask(id: number): Promise<void> {
    await api.delete(`/tasks/${id}`);
  },
};
