import React from 'react';
import { Link } from 'react-router-dom';
import { Recipe } from '../api/client';

interface RecipeCardProps {
  recipe: Recipe;
  missingIngredients?: Array<{
    name: string;
    quantity: number;
    unit: string;
    price?: number;
  }>;
  missingTools?: string[];
}

const RecipeCard: React.FC<RecipeCardProps> = ({
  recipe,
  missingIngredients = [],
  missingTools = [],
}) => {
  const formatDifficulty = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'easy':
      case '쉬움':
        return '쉬움';
      case 'medium':
      case '보통':
        return '보통';
      case 'hard':
      case '어려움':
        return '어려움';
      default:
        return difficulty;
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="p-6">
        <div className="flex justify-between items-start mb-4">
          <h2 className="text-xl font-semibold text-gray-800">{recipe.name}</h2>
          {recipe.is_ai_generated && (
            <span className="bg-purple-100 text-purple-800 text-xs font-medium px-2.5 py-0.5 rounded">
              AI 생성
            </span>
          )}
        </div>

        <div className="mb-4">
          <div className="flex items-center text-gray-600 mb-2">
            <span className="mr-2">조리시간:</span>
            <span>{recipe.cooking_time}분</span>
          </div>
          <div className="flex items-center text-gray-600">
            <span className="mr-2">난이도:</span>
            <span>{formatDifficulty(recipe.difficulty)}</span>
          </div>
        </div>

        {(missingIngredients.length > 0 || missingTools.length > 0) && (
          <div className="mb-4">
            {missingIngredients.length > 0 && (
              <div className="mb-2">
                <h3 className="text-sm font-semibold text-red-600 mb-1">
                  부족한 재료:
                </h3>
                <ul className="text-sm text-gray-600">
                  {missingIngredients.map((ingredient, index) => (
                    <li key={index} className="flex justify-between">
                      <span>
                        {ingredient.name} ({ingredient.quantity} {ingredient.unit})
                      </span>
                      {ingredient.price && (
                        <span className="text-green-600">
                          ₩{ingredient.price.toLocaleString()}
                        </span>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {missingTools.length > 0 && (
              <div>
                <h3 className="text-sm font-semibold text-red-600 mb-1">
                  필요한 도구:
                </h3>
                <ul className="text-sm text-gray-600">
                  {missingTools.map((tool, index) => (
                    <li key={index}>{tool}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        <Link
          to={`/recipe/${recipe.id}`}
          className="inline-block bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors"
        >
          자세히 보기
        </Link>
      </div>
    </div>
  );
};

export default RecipeCard;