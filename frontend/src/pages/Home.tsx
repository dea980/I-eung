import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import api, { Recipe, Ingredient, Tool } from '../api/client';
import RecipeCard from '../components/RecipeCard';

interface RecipeRecommendation {
  recipe: Recipe;
  has_all_ingredients: boolean;
  missing_ingredients: Array<{
    name: string;
    quantity: number;
    unit: string;
    price?: number;
  }>;
  has_all_tools: boolean;
  missing_tools: string[];
}

const Home: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const [ingredients, setIngredients] = useState<Ingredient[]>([]);
  const [tools, setTools] = useState<Tool[]>([]);
  const [recommendations, setRecommendations] = useState<RecipeRecommendation[]>([]);
  const [newIngredient, setNewIngredient] = useState({ name: '', quantity: '', unit: '' });
  const [newTool, setNewTool] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAddIngredient = () => {
    if (newIngredient.name && newIngredient.quantity && newIngredient.unit) {
      setIngredients([
        ...ingredients,
        {
          id: Date.now(),
          name: newIngredient.name,
          quantity: parseFloat(newIngredient.quantity),
          unit: newIngredient.unit,
        },
      ]);
      setNewIngredient({ name: '', quantity: '', unit: '' });
    }
  };

  const handleRemoveIngredient = (id: number) => {
    setIngredients(ingredients.filter((ing) => ing.id !== id));
  };

  const handleAddTool = () => {
    if (newTool) {
      setTools([...tools, { id: Date.now(), name: newTool }]);
      setNewTool('');
    }
  };

  const handleRemoveTool = (id: number) => {
    setTools(tools.filter((tool) => tool.id !== id));
  };

  const getRecommendations = async () => {
    try {
      setLoading(true);
      const response = await api.recommendRecipes(
        ingredients,
        tools.map((t) => t.name)
      );
      setRecommendations(response);
    } catch (error) {
      console.error('레시피 추천 에러:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-2xl font-bold mb-6">재료 및 도구 입력</h2>

        {/* 재료 입력 섹션 */}
        <div className="mb-8">
          <h3 className="text-lg font-semibold mb-4">보유 재료</h3>
          <div className="flex gap-4 mb-4">
            <input
              type="text"
              placeholder="재료명"
              className="flex-1 p-2 border rounded"
              value={newIngredient.name}
              onChange={(e) =>
                setNewIngredient({ ...newIngredient, name: e.target.value })
              }
            />
            <input
              type="number"
              placeholder="수량"
              className="w-24 p-2 border rounded"
              value={newIngredient.quantity}
              onChange={(e) =>
                setNewIngredient({ ...newIngredient, quantity: e.target.value })
              }
            />
            <input
              type="text"
              placeholder="단위"
              className="w-24 p-2 border rounded"
              value={newIngredient.unit}
              onChange={(e) =>
                setNewIngredient({ ...newIngredient, unit: e.target.value })
              }
            />
            <button
              onClick={handleAddIngredient}
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              추가
            </button>
          </div>
          <ul className="space-y-2">
            {ingredients.map((ing) => (
              <li
                key={ing.id}
                className="flex justify-between items-center bg-gray-50 p-2 rounded"
              >
                <span>
                  {ing.name} ({ing.quantity} {ing.unit})
                </span>
                <button
                  onClick={() => handleRemoveIngredient(ing.id)}
                  className="text-red-500 hover:text-red-700"
                >
                  삭제
                </button>
              </li>
            ))}
          </ul>
        </div>

        {/* 도구 입력 섹션 */}
        <div className="mb-8">
          <h3 className="text-lg font-semibold mb-4">보유 도구</h3>
          <div className="flex gap-4 mb-4">
            <input
              type="text"
              placeholder="도구명"
              className="flex-1 p-2 border rounded"
              value={newTool}
              onChange={(e) => setNewTool(e.target.value)}
            />
            <button
              onClick={handleAddTool}
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              추가
            </button>
          </div>
          <ul className="space-y-2">
            {tools.map((tool) => (
              <li
                key={tool.id}
                className="flex justify-between items-center bg-gray-50 p-2 rounded"
              >
                <span>{tool.name}</span>
                <button
                  onClick={() => handleRemoveTool(tool.id)}
                  className="text-red-500 hover:text-red-700"
                >
                  삭제
                </button>
              </li>
            ))}
          </ul>
        </div>

        <button
          onClick={getRecommendations}
          className="w-full bg-green-500 text-white px-6 py-3 rounded-lg text-lg font-semibold hover:bg-green-600 disabled:bg-gray-400"
          disabled={loading || (!ingredients.length && !tools.length)}
        >
          {loading ? '추천 중...' : '레시피 추천 받기'}
        </button>
      </div>

      {/* 추천 결과 섹션 */}
      {recommendations.length > 0 && (
        <div className="space-y-6">
          <h2 className="text-2xl font-bold mb-6">추천 레시피</h2>
          {recommendations.map((rec) => (
            <RecipeCard
              key={rec.recipe.id}
              recipe={rec.recipe}
              missingIngredients={rec.missing_ingredients}
              missingTools={rec.missing_tools}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default Home;