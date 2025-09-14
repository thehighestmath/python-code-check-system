import React from 'react';
import { useAuth } from '../contexts/AuthContext.tsx';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
  const { user } = useAuth();

  return (
    <div>
      <div className="card">
        <h1>Добро пожаловать в систему проверки Python кода!</h1>
        <p>
          Эта система позволяет студентам решать задания по программированию на Python
          и получать автоматическую проверку своих решений.
        </p>
        
        {user ? (
          <div>
            <p>Привет, {user.username}!</p>
            <div style={{ marginTop: '1rem' }}>
              <Link to="/tasks" className="btn btn-primary" style={{ marginRight: '1rem' }}>
                Посмотреть задания
              </Link>
              <Link to="/solutions" className="btn btn-success">
                Мои решения
              </Link>
            </div>
          </div>
        ) : (
          <div>
            <p>Для начала работы необходимо войти в систему или зарегистрироваться.</p>
            <div style={{ marginTop: '1rem' }}>
              <Link to="/login" className="btn btn-primary" style={{ marginRight: '1rem' }}>
                Войти
              </Link>
              <Link to="/register" className="btn btn-success">
                Регистрация
              </Link>
            </div>
          </div>
        )}
      </div>

      <div className="card">
        <h2>Возможности системы</h2>
        <ul>
          <li>Решение заданий различной сложности</li>
          <li>Автоматическая проверка кода</li>
          <li>Проверка на использование запрещенных функций</li>
          <li>Ограничения по времени и памяти</li>
          <li>История решений</li>
        </ul>
      </div>
    </div>
  );
};

export default Home;
