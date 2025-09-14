import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext.tsx';
import { solutionService, Solution } from '../services/solutionService.ts';

const Solutions: React.FC = () => {
  const [solutions, setSolutions] = useState<Solution[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { user } = useAuth();

  useEffect(() => {
    const fetchSolutions = async () => {
      try {
        const data = await solutionService.getSolutions();
        setSolutions(data);
      } catch (err: any) {
        setError('Ошибка загрузки решений');
      } finally {
        setLoading(false);
      }
    };

    fetchSolutions();
  }, []);

  const getStatusClass = (isAccepted: boolean, errorMessage?: string) => {
    if (isAccepted) return 'status-accepted';
    if (errorMessage) return 'status-failed';
    return 'status-pending';
  };

  const getStatusText = (isAccepted: boolean, errorMessage?: string) => {
    if (isAccepted) return 'Принято';
    if (errorMessage) return 'Ошибка';
    return 'Проверяется...';
  };

  if (loading) {
    return <div className="card">Загрузка...</div>;
  }

  if (error) {
    return <div className="alert alert-error">{error}</div>;
  }

  if (!user) {
    return (
      <div className="alert alert-error">
        Для просмотра решений необходимо войти в систему.
      </div>
    );
  }

  return (
    <div>
      <div className="card">
        <h1>Мои решения</h1>
        <p>История всех ваших решений</p>
      </div>

      {solutions.length === 0 ? (
        <div className="card">
          <p>У вас пока нет решений</p>
          <Link to="/tasks" className="btn btn-primary">
            Посмотреть задания
          </Link>
        </div>
      ) : (
        <div>
          {solutions.map((solution) => (
            <div key={solution.id} className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h3>
                  {solution.task ? solution.task.name : `Задание #${solution.task_id}`}
                </h3>
                <span className={`solution-status ${getStatusClass(solution.is_accepted, solution.error_message)}`}>
                  {getStatusText(solution.is_accepted, solution.error_message)}
                </span>
              </div>
              
              {solution.task && (
                <p style={{ marginBottom: '1rem', color: '#666' }}>
                  Сложность: {solution.task.complexity}
                </p>
              )}

              {solution.error_message && (
                <div className="alert alert-error" style={{ marginBottom: '1rem' }}>
                  <strong>Ошибка:</strong> {solution.error_message}
                </div>
              )}

              <div style={{ marginBottom: '1rem' }}>
                <h4>Код:</h4>
                <pre style={{ 
                  background: '#f8f9fa', 
                  padding: '1rem', 
                  borderRadius: '4px', 
                  overflow: 'auto',
                  maxHeight: '300px'
                }}>
                  {solution.source_code}
                </pre>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.9rem', color: '#666' }}>
                <span>
                  Создано: {new Date(solution.created_at).toLocaleString()}
                </span>
                {solution.task && (
                  <Link to={`/tasks/${solution.task.id}`} className="btn btn-primary">
                    К заданию
                  </Link>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Solutions;
