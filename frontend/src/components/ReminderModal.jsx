import { useEffect, useState } from 'react';

import httpClient from '../api/http-client';

const eventTypeLabels = {
  birthday: '生日',
  anniversary: '纪念日',
  other: '其他',
};

function ReminderModal({ isAuthenticated }) {
  const [todoReminders, setTodoReminders] = useState([]);
  const [calendarReminders, setCalendarReminders] = useState([]);
  const [isDismissed, setIsDismissed] = useState(false);

  useEffect(() => {
    let isMounted = true;

    async function fetchReminders() {
      if (!isAuthenticated) {
        if (isMounted) {
          setTodoReminders([]);
          setCalendarReminders([]);
        }
        return;
      }

      if (isDismissed) {
        return;
      }

      const [todoResult, calendarResult] = await Promise.allSettled([
        httpClient.get('/todos/reminders'),
        httpClient.get('/calendar-events/reminders'),
      ]);

      if (!isMounted) {
        return;
      }

      setTodoReminders(todoResult.status === 'fulfilled' ? todoResult.value.data.items : []);
      setCalendarReminders(calendarResult.status === 'fulfilled' ? calendarResult.value.data.items : []);
    }

    fetchReminders();

    return () => {
      isMounted = false;
    };
  }, [isAuthenticated, isDismissed]);

  if (!isAuthenticated || isDismissed || todoReminders.length + calendarReminders.length === 0) {
    return null;
  }

  return (
    <div className="reminder-modal" role="dialog" aria-modal="true" aria-labelledby="reminder-modal-title">
      <button className="reminder-backdrop" type="button" onClick={() => setIsDismissed(true)} />
      <section className="reminder-panel">
        <div className="reminder-header">
          <h2 id="reminder-modal-title">提醒中心</h2>
          <button className="text-button" type="button" onClick={() => setIsDismissed(true)}>
            关闭
          </button>
        </div>

        <div className="reminder-groups">
          {todoReminders.length > 0 ? (
            <section className="reminder-group">
              <h3>待办提醒</h3>
              <div className="reminder-list">
                {todoReminders.map((todo) => (
                  <article key={todo.id}>
                    <strong>{todo.title}</strong>
                    <span>{todo.due_date ? `截止 ${todo.due_date}` : '无截止日期'}</span>
                    {todo.category ? <small>{todo.category}</small> : null}
                  </article>
                ))}
              </div>
            </section>
          ) : null}

          {calendarReminders.length > 0 ? (
            <section className="reminder-group">
              <h3>日历提醒</h3>
              <div className="reminder-list">
                {calendarReminders.map((event) => (
                  <article key={`${event.id}-${event.display_date}`}>
                    <strong>{event.title}</strong>
                    <span>
                      {eventTypeLabels[event.event_type]} · {event.display_date}
                      {event.is_yearly ? ' · 每年重复' : ''}
                    </span>
                    {event.note ? <small>{event.note}</small> : null}
                  </article>
                ))}
              </div>
            </section>
          ) : null}
        </div>
      </section>
    </div>
  );
}

export default ReminderModal;
