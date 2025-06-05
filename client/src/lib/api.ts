
const API_BASE_URL = 'http://localhost:8000/api';

interface ApiResponse<T> {
  data: T;
  status: number;
}

class ApiClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const token = localStorage.getItem('access_token');
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
      ...options,
    };

    const response = await fetch(`${this.baseURL}${endpoint}`, config);
    
    if (response.status === 401) {
      // Token expired, try to refresh
      await this.refreshToken();
      // Retry the request
      const retryResponse = await fetch(`${this.baseURL}${endpoint}`, {
        ...config,
        headers: {
          ...config.headers,
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      });
      const data = await retryResponse.json();
      return { data, status: retryResponse.status };
    }

    const data = await response.json();
    return { data, status: response.status };
  }

  private async refreshToken(): Promise<void> {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await fetch(`${this.baseURL}/token/refresh/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('access_token', data.access);
    } else {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/auth';
    }
  }

  // Auth endpoints
  async login(email: string, password: string) {
    return this.request('/accounts/login/', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async register(userData: any) {
    return this.request('/accounts/register/', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async getUserProfile() {
    return this.request('/accounts/profile/');
  }

  // Jobs endpoints
  async getJobs(params?: URLSearchParams) {
    const query = params ? `?${params.toString()}` : '';
    return this.request(`/jobs/${query}`);
  }

  async getJob(id: string) {
    return this.request(`/jobs/${id}/`);
  }

  async createJob(jobData: any) {
    return this.request('/jobs/create/', {
      method: 'POST',
      body: JSON.stringify(jobData),
    });
  }

  async applyToJob(jobId: string, applicationData: any) {
    return this.request('/jobs/apply/', {
      method: 'POST',
      body: JSON.stringify({ job: jobId, ...applicationData }),
    });
  }

  async getApplications() {
    return this.request('/jobs/applications/');
  }

  async toggleWishlist(jobId: string, action: 'add' | 'remove') {
    return this.request(`/jobs/${jobId}/wishlist/`, {
      method: action === 'add' ? 'POST' : 'DELETE',
    });
  }

  async getWishlist() {
    return this.request('/jobs/wishlist/');
  }

  async getJobCategories() {
    return this.request('/jobs/categories/');
  }

  // Recommendations
  async getRecommendations() {
    return this.request('/recommendations/jobs/');
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
