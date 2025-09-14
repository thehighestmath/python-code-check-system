import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext.tsx';

const Navbar: React.FC = () => {
  const { user, logout } = useAuth();

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        Python Code Check
      </Link>
      <ul className="navbar-nav">
        <li>
          <Link to="/">Главная</Link>
        </li>
        <li>
          <Link to="/tasks">Задания</Link>
        </li>
        {user ? (
          <>
            <li>
              <Link to="/solutions">Мои решения</Link>
            </li>
            <li>
              <Link to="/profile">Профиль</Link>
            </li>
            <li>
              <button onClick={logout} className="btn btn-primary">
                Выйти
              </button>
            </li>
          </>
        ) : (
          <>
            <li>
              <Link to="/login">Войти</Link>
            </li>
            <li>
              <Link to="/register">Регистрация</Link>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;
