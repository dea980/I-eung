import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import api from '../api/client';
import { Recipe } from '../types';
import RecipeCard from '../components/RecipeCard';

const Profile: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const [favoriteRecipes, setFavoriteRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    fetchFavoriteRecipes();
  }, [isAuthenticated, navigate]);

  const fetchFavoriteRecipes = async () => {
    if (!user) return;

    try {
      setLoading(true);
      const data = await api.getFavorites(user.id);
      setFavoriteRecipes(data);
    } catch (err) {
      console.error('즐겨찾기 조회 에러:', err);
      setError('즐겨찾기 목록을 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-xl">로딩 중...</div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-xl text-red-600">사용자 정보를 찾을 수 없습니다.</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* 프로필 정보 */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <div className="flex justify-between items-start mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">{user.name}</h1>
            <p className="text-gray-600">{user.email}</p>
          </div>
          <button
            onClick={handleLogout}
            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
          >
            로그아웃
          </button>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gray-50 p-4 rounded">
            <h3 className="font-medium text-gray-700 mb-1">즐겨찾기한 레시피</h3>
            <p className="text-2xl font-bold text-blue-600">
              {favoriteRecipes.length}개
            </p>
          </div>
          <div className="bg-gray-50 p-4 rounded">
            <h3 className="font-medium text-gray-700 mb-1">최근 활동</h3>
            <p className="text-sm text-gray-600">
              최근 로그인: {new Date().toLocaleDateString()}
            </p>
          </div>
        </div>
      </div>

      {/* 즐겨찾기 목록 */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold mb-6">즐겨찾기한 레시피</h2>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {favoriteRecipes.length === 0 ? (
          <p className="text-gray-500 text-center py-8">
            아직 즐겨찾기한 레시피가 없습니다.
          </p>
        ) : (
          <div className="space-y-6">
            {favoriteRecipes.map((recipe) => (
              <RecipeCard
                key={recipe.id}
                recipe={recipe}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Profile;