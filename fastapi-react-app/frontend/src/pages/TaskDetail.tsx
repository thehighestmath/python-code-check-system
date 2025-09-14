import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext.tsx';
import { taskService, Task } from '../services/taskService.ts';
import { solutionService, Solution } from '../services/solutionService.ts';

const TaskDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [task, setTask] = useState<Task | null>(null);
  const [solutions, setSolutions] = useState<Solution[]>([]);
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      if (!id) return;
      
      try {
        const [taskData, solutionsData] = await Promise.all([
          taskService.getTask(parseInt(id)),
          solutionService.getSolutions()
        ]);
        
        setTask(taskData);
        setSolutions(solutionsData.filter(s => s.task_id === parseInt(id)));
      } catch (err: any) {
        setError('Ошибка загрузки данных');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!task || !code.trim()) return;

    setSubmitting(true);
    setError('');
    setSuccess('');

    try {
      await solutionService.createSolution({
        source_code: code,
        task_id: task.id
      });
      
      setSuccess('Решение отправлено на проверку!');
      setCode('');
      
      // Refresh solutions
      const solutionsData = await solutionService.getSolutions();
      setSolutions(solutionsData.filter(s => s.task_id === task.id));
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка отправки решения');
    } finally {
      setSubmitting(false);
    }
  };

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

  if (!task) {
    return <div className="alert alert-error">Задание не найдено</div>;
  }

  if (!user) {
    return (
      <div className="alert alert-error">
        Для решения заданий необходимо войти в систему.
      </div>
    );
  }

  return (
    <div>
      <div className="card">
        <h1>{task.name}</h1>
        <span className={`task-complexity ${getComplexityClass(task.complexity)}`}>
          {getComplexityText(task.complexity)}
        </span>
        <div style={{ marginTop: '1rem' }}>
          <h3>Описание:</h3>
          <p style={{ whiteSpace: 'pre-wrap' }}>{task.description}</p>
        </div>
      </div>

      <div className="card">
        <h2>Отправить решение</h2>
        
        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        {success && (
          <div className="alert alert-success">
            {success}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="code">Код на Python:</label>
            <textarea
              id="code"
              className="code-editor"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="Введите ваш код здесь..."
              required
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={submitting || !code.trim()}
          >
            {submitting ? 'Отправка...' : 'Отправить решение'}
          </button>
        </form>
      </div>

      {solutions.length > 0 && (
        <div className="card">
          <h2>Мои решения</h2>
          {solutions.map((solution) => (
            <div key={solution.id} style={{ marginBottom: '1rem', padding: '1rem', border: '1px solid #ddd', borderRadius: '4px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <span>Решение #{solution.id}</span>
                <span className={`solution-status ${getStatusClass(solution.is_accepted, solution.error_message)}`}>
                  {getStatusText(solution.is_accepted, solution.error_message)}
                </span>
              </div>
              {solution.error_message && (
                <div style={{ color: '#721c24', fontSize: '0.9rem', marginBottom: '0.5rem' }}>
                  {solution.error_message}
                </div>
              )}
              <pre style={{ background: '#f8f9fa', padding: '0.5rem', borderRadius: '4px', fontSize: '0.9rem', overflow: 'auto' }}>
                {solution.source_code}
              </pre>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TaskDetail;
