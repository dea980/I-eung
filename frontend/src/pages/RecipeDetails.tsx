import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import api from '../api/client';
import { Recipe, RecipeIngredient, RecipeTool } from '../types';

interface RecipeDetailsProps {}

const RecipeDetails: React.FC<RecipeDetailsProps> = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [addingToFavorites, setAddingToFavorites] = useState(false);
  const [addingToShoppingList, setAddingToShoppingList] = useState(false);

  useEffect(() => {
    const fetchRecipe = async () => {
      try {
        if (!id) return;
        const data = await api.getRecipeById(parseInt(id));
        setRecipe(data);
      } catch (err) {
        setError('레시피를 불러오는데 실패했습니다.');
        console.error('레시피 조회 에러:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchRecipe();
  }, [id]);

  const handleAddToFavorites = async () => {
    if (!isAuthenticated || !user || !recipe) return;
    
    try {
      setAddingToFavorites(true);
      await api.addToFavorites(user.id, recipe.id);
      alert('즐겨찾기에 추가되었습니다.');
    } catch (err) {
      console.error('즐겨찾기 추가 에러:', err);
      alert('즐겨찾기 추가에 실패했습니다.');
    } finally {
      setAddingToFavorites(false);
    }
  };

  const handleAddToShoppingList = async () => {
    if (!isAuthenticated || !user || !recipe) return;
    
    try {
      setAddingToShoppingList(true);
      // 레시피의 모든 재료를 장보기 목록에 추가
      for (const recipeIngredient of recipe.ingredients) {
        await api.addToShoppingList(user.id, {
          ingredient_id: recipeIngredient.ingredient.id,
          quantity: recipeIngredient.quantity,
          unit: recipeIngredient.unit,
        });
      }
      alert('장보기 목록에 추가되었습니다.');
    } catch (err) {
      console.error('장보기 목록 추가 에러:', err);
      alert('장보기 목록 추가에 실패했습니다.');
    } finally {
      setAddingToShoppingList(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-xl">로딩 중...</div>
      </div>
    );
  }

  if (error || !recipe) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-xl text-red-600">{error || '레시피를 찾을 수 없습니다.'}</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex justify-between items-start mb-6">
          <h1 className="text-3xl font-bold text-gray-900">{recipe.name}</h1>
          {recipe.is_ai_generated && (
            <span className="bg-purple-100 text-purple-800 text-sm font-medium px-2.5 py-0.5 rounded">
              AI 생성
            </span>
          )}
        </div>

        <div className="grid grid-cols-2 gap-6 mb-8">
          <div>
            <h2 className="text-xl font-semibold mb-4">기본 정보</h2>
            <div className="space-y-2">
              <p className="text-gray-600">
                <span className="font-medium">조리 시간:</span> {recipe.cooking_time}분
              </p>
              <p className="text-gray-600">
                <span className="font-medium">난이도:</span> {recipe.difficulty}
              </p>
            </div>
          </div>

          {isAuthenticated && (
            <div className="flex flex-col gap-4">
              <button
                onClick={handleAddToFavorites}
                disabled={addingToFavorites}
                className="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600 disabled:bg-gray-400"
              >
                {addingToFavorites ? '추가 중...' : '즐겨찾기에 추가'}
              </button>
              <button
                onClick={handleAddToShoppingList}
                disabled={addingToShoppingList}
                className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 disabled:bg-gray-400"
              >
                {addingToShoppingList ? '추가 중...' : '장보기 목록에 추가'}
              </button>
            </div>
          )}
        </div>

        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">필요한 재료</h2>
          <ul className="grid grid-cols-2 gap-4">
            {recipe.ingredients.map((recipeIngredient, index) => (
              <li key={index} className="flex justify-between items-center bg-gray-50 p-3 rounded">
                <span className="font-medium">{recipeIngredient.ingredient.name}</span>
                <span className="text-gray-600">
                  {recipeIngredient.quantity} {recipeIngredient.unit}
                </span>
              </li>
            ))}
          </ul>
        </div>

        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">필요한 도구</h2>
          <ul className="grid grid-cols-2 gap-4">
            {recipe.tools.map((recipeTool, index) => (
              <li key={index} className="bg-gray-50 p-3 rounded">
                {recipeTool.tool.name}
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h2 className="text-xl font-semibold mb-4">조리 방법</h2>
          <div className="prose max-w-none">
            {recipe.instructions.split('\n').map((instruction, index) => (
              <p key={index} className="mb-4">
                {instruction}
              </p>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecipeDetails;