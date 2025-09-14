import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext.tsx';
import { taskService, Task } from '../services/taskService.ts';

const Tasks: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { user } = useAuth();

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const data = await taskService.getTasks(true);
        setTasks(data);
      } catch (err: any) {
        setError('Ошибка загрузки заданий');
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, []);

  const getComplexityClass = (complexity: string) => {
    switch (complexity) {
      case 'easy':
        return 'complexity-easy';
      case 'medium':
        return 'complexity-medium';
      case 'hard':
        return 'complexity-hard';
      default:
        return 'complexity-easy';
    }
  };

  const getComplexityText = (complexity: string) => {
    switch (complexity) {
      case 'easy':
        return 'Легкое';
      case 'medium':
        return 'Среднее';
      case 'hard':
        return 'Сложное';
      default:
        return 'Легкое';
    }
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
        Для просмотра заданий необходимо войти в систему.
      </div>
    );
  }

  return (
    <div>
      <div className="card">
        <h1>Задания</h1>
        <p>Выберите задание для решения</p>
      </div>

      {tasks.length === 0 ? (
        <div className="card">
          <p>Нет доступных заданий</p>
        </div>
      ) : (
        <div className="task-list">
          {tasks.map((task) => (
            <div key={task.id} className="task-card">
              <h3 className="task-title">{task.name}</h3>
              <span className={`task-complexity ${getComplexityClass(task.complexity)}`}>
                {getComplexityText(task.complexity)}
              </span>
              <p style={{ marginBottom: '1rem' }}>
                {task.description.length > 200
                  ? `${task.description.substring(0, 200)}...`
                  : task.description}
              </p>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <Link to={`/tasks/${task.id}`} className="btn btn-primary">
                  Решить
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Tasks;
