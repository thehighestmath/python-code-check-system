import React from 'react';
import { useAuth } from '../contexts/AuthContext.tsx';

const Profile: React.FC = () => {
  const { user } = useAuth();

  if (!user) {
    return (
      <div className="alert alert-error">
        Для просмотра профиля необходимо войти в систему.
      </div>
    );
  }

  return (
    <div>
      <div className="card">
        <h1>Профиль пользователя</h1>
        
        <div style={{ marginBottom: '1rem' }}>
          <strong>Имя пользователя:</strong> {user.username}
        </div>
        
        <div style={{ marginBottom: '1rem' }}>
          <strong>Email:</strong> {user.email}
        </div>
        
        <div style={{ marginBottom: '1rem' }}>
          <strong>Статус:</strong> {user.is_student ? 'Студент' : 'Преподаватель'}
        </div>
        
        <div style={{ marginBottom: '1rem' }}>
          <strong>Активен:</strong> {user.is_active ? 'Да' : 'Нет'}
        </div>
        
        <div style={{ marginBottom: '1rem' }}>
          <strong>Дата регистрации:</strong> {new Date(user.created_at).toLocaleString()}
        </div>
      </div>
    </div>
  );
};

export default Profile;
