import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import api from '../api/client';

interface ShoppingListItem {
  id: number;
  ingredient: {
    id: number;
    name: string;
    price: number | null;
  };
  quantity: number;
  unit: string;
}

const ShoppingList: React.FC = () => {
  const { user, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [items, setItems] = useState<ShoppingListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    fetchShoppingList();
  }, [isAuthenticated, navigate]);

  const fetchShoppingList = async () => {
    if (!user) return;

    try {
      setLoading(true);
      const data = await api.getShoppingList(user.id);
      setItems(data);
    } catch (err) {
      console.error('장보기 목록 조회 에러:', err);
      setError('장보기 목록을 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveItem = async (itemId: number) => {
    if (!user) return;

    try {
      // API 호출로 아이템 삭제
      await fetch(`/api/users/${user.id}/shopping-list/${itemId}`, {
        method: 'DELETE',
      });

      // 성공적으로 삭제되면 목록에서 제거
      setItems(items.filter(item => item.id !== itemId));
    } catch (err) {
      console.error('아이템 삭제 에러:', err);
      alert('아이템 삭제에 실패했습니다.');
    }
  };

  const calculateTotal = () => {
    return items.reduce((total, item) => {
      if (item.ingredient.price) {
        return total + (item.ingredient.price * item.quantity);
      }
      return total;
    }, 0);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-xl">로딩 중...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-xl text-red-600">{error}</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold mb-6">장보기 목록</h1>

        {items.length === 0 ? (
          <p className="text-gray-500 text-center py-8">
            장보기 목록이 비어있습니다.
          </p>
        ) : (
          <>
            <div className="space-y-4 mb-8">
              {items.map((item) => (
                <div
                  key={item.id}
                  className="flex justify-between items-center bg-gray-50 p-4 rounded"
                >
                  <div>
                    <h3 className="font-medium">{item.ingredient.name}</h3>
                    <p className="text-sm text-gray-600">
                      {item.quantity} {item.unit}
                    </p>
                  </div>
                  <div className="flex items-center gap-4">
                    {item.ingredient.price && (
                      <span className="text-green-600 font-medium">
                        ₩{(item.ingredient.price * item.quantity).toLocaleString()}
                      </span>
                    )}
                    <button
                      onClick={() => handleRemoveItem(item.id)}
                      className="text-red-500 hover:text-red-700"
                    >
                      삭제
                    </button>
                  </div>
                </div>
              ))}
            </div>

            <div className="border-t pt-4">
              <div className="flex justify-between items-center">
                <span className="text-lg font-medium">총 예상 금액:</span>
                <span className="text-xl font-bold text-green-600">
                  ₩{calculateTotal().toLocaleString()}
                </span>
              </div>
              <p className="text-sm text-gray-500 mt-2">
                * 일부 재료의 가격 정보가 없을 수 있습니다.
              </p>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default ShoppingList;