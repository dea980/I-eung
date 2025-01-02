// 사용자 관련 타입
export interface User {
  id: number;
  name: string;
  email: string;
}

// 레시피 관련 타입
export interface Recipe {
  id: number;
  name: string;
  instructions: string;
  cooking_time: number;
  difficulty: string;
  is_ai_generated: boolean;
  ingredients: RecipeIngredient[];
  tools: RecipeTool[];
}

export interface RecipeIngredient {
  id: number;
  ingredient: Ingredient;
  quantity: number;
  unit: string;
}

export interface RecipeTool {
  id: number;
  tool: Tool;
}

// 재료 관련 타입
export interface Ingredient {
  id: number;
  name: string;
  price?: number;
  quantity?: number;
  unit?: string;
}

// 도구 관련 타입
export interface Tool {
  id: number;
  name: string;
}

// API 응답 타입
export interface ApiResponse<T> {
  data: T;
  message?: string;
  error?: string;
}

// 레시피 추천 관련 타입
export interface RecipeRecommendation {
  recipe: Recipe;
  has_all_ingredients: boolean;
  missing_ingredients: MissingIngredient[];
  has_all_tools: boolean;
  missing_tools: string[];
}

export interface MissingIngredient {
  name: string;
  quantity: number;
  unit: string;
  price?: number;
}

// 장보기 목록 관련 타입
export interface ShoppingListItem {
  id: number;
  ingredient: Ingredient;
  quantity: number;
  unit: string;
}

// 인증 관련 타입
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials extends LoginCredentials {
  name: string;
}

export interface AuthResponse {
  user: User;
  token: string;
}

// 컴포넌트 Props 타입
export interface RecipeCardProps {
  recipe: Recipe;
  missingIngredients?: MissingIngredient[];
  missingTools?: string[];
}

export interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}