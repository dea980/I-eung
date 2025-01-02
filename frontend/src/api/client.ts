import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 인터셉터 설정
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// API 타입 정의
export interface Recipe {
  id: number;
  name: string;
  instructions: string;
  cooking_time: number;
  difficulty: string;
  is_ai_generated: boolean;
}

export interface Ingredient {
  id: number;
  name: string;
  quantity?: number;
  unit?: string;
  price?: number;
}

export interface Tool {
  id: number;
  name: string;
}

// API 함수들
export const api = {
  // 사용자 관련
  login: async (email: string, password: string) => {
    const response = await client.post('/users/login', { email, password });
    return response.data;
  },

  register: async (name: string, email: string, password: string) => {
    const response = await client.post('/users', { name, email, password });
    return response.data;
  },

  // 레시피 관련
  getRecipes: async () => {
    const response = await client.get<Recipe[]>('/recipes');
    return response.data;
  },

  getRecipeById: async (id: number) => {
    const response = await client.get<Recipe>(`/recipes/${id}`);
    return response.data;
  },

  recommendRecipes: async (ingredients: Ingredient[], tools: string[]) => {
    const response = await client.post('/recipes/recommend', { ingredients, tools });
    return response.data;
  },

  generateRecipe: async (ingredients: string[]) => {
    const response = await client.post<Recipe>('/recipes/generate', { ingredients });
    return response.data;
  },

  // 재료 관련
  getIngredients: async () => {
    const response = await client.get<Ingredient[]>('/ingredients');
    return response.data;
  },

  addIngredient: async (ingredient: Omit<Ingredient, 'id'>) => {
    const response = await client.post('/ingredients', ingredient);
    return response.data;
  },

  // 도구 관련
  getTools: async () => {
    const response = await client.get<Tool[]>('/tools');
    return response.data;
  },

  addTool: async (name: string) => {
    const response = await client.post('/tools', { name });
    return response.data;
  },

  // 즐겨찾기 관련
  addToFavorites: async (userId: number, recipeId: number) => {
    const response = await client.post(`/users/${userId}/favorites/${recipeId}`);
    return response.data;
  },

  getFavorites: async (userId: number) => {
    const response = await client.get(`/users/${userId}/favorites`);
    return response.data;
  },

  // 장보기 목록 관련
  addToShoppingList: async (userId: number, item: { ingredient_id: number; quantity: number; unit: string }) => {
    const response = await client.post(`/users/${userId}/shopping-list`, item);
    return response.data;
  },

  getShoppingList: async (userId: number) => {
    const response = await client.get(`/users/${userId}/shopping-list`);
    return response.data;
  },
};

export default api;