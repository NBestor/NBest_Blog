import { useCallback, useEffect, useMemo, useState } from 'react';

import httpClient from '../api/http-client';

const eventTypeLabels = {
  birthday: '生日',
  anniversary: '纪念日',
  other: '其他',
};

const emptyForm = {
  title: '',
  event_date: '',
  event_type: 'other',
  note: '',
  is_yearly: false,
};

function formatMonth(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  return `${year}-${month}`;
}

function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function buildCalendarDays(monthDate) {
  const year = monthDate.getFullYear();
  const month = monthDate.getMonth();
  const firstDay = new Date(year, month, 1);
  const start = new Date(year, month, 1 - firstDay.getDay());
  return Array.from({ length: 42 }, (_, index) => {
    const day = new Date(start);
    day.setDate(start.getDate() + index);
    return {
      date: formatDate(day),
      dayNumber: day.getDate(),
      isCurrentMonth: day.getMonth() === month,
    };
  });
}

function buildPayload(formData) {
  return {
    title: formData.title.trim(),
    event_date: formData.event_date,
    event_type: formData.event_type,
    note: formData.note.trim() || null,
    is_yearly: formData.is_yearly,
  };
}

function CalendarPage() {
  const [currentMonth, setCurrentMonth] = useState(() => new Date());
  const [events, setEvents] = useState([]);
  const [formData, setFormData] = useState(() => ({ ...emptyForm, event_date: formatDate(new Date()) }));
  const [editingId, setEditingId] = useState(null);
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const monthKey = formatMonth(currentMonth);
  const days = useMemo(() => buildCalendarDays(currentMonth), [currentMonth]);
  const eventsByDate = useMemo(() => {
    return events.reduce((groups, event) => {
      const group = groups[event.display_date] || [];
      return { ...groups, [event.display_date]: [...group, event] };
    }, {});
  }, [events]);

  const getEvents = useCallback(async () => {
    const response = await httpClient.get('/calendar-events', { params: { month: monthKey } });
    return response.data.items;
  }, [monthKey]);

  const refreshEvents = useCallback(async () => {
    try {
      setEvents(await getEvents());
    } catch {
      setMessage('日历事件加载失败');
    } finally {
      setIsLoading(false);
    }
  }, [getEvents]);

  useEffect(() => {
    let isMounted = true;

    async function loadEvents() {
      setIsLoading(true);
      try {
        const items = await getEvents();
        if (isMounted) {
          setEvents(items);
        }
      } catch {
        if (isMounted) {
          setMessage('日历事件加载失败');
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadEvents();

    return () => {
      isMounted = false;
    };
  }, [getEvents]);

  function changeMonth(offset) {
    setCurrentMonth((date) => new Date(date.getFullYear(), date.getMonth() + offset, 1));
  }

  function handleFormChange(event) {
    const { checked, name, type, value } = event.target;
    setFormData((currentData) => ({ ...currentData, [name]: type === 'checkbox' ? checked : value }));
  }

  function resetForm() {
    setEditingId(null);
    setFormData({ ...emptyForm, event_date: formatDate(new Date()) });
  }

  function startEdit(event) {
    setEditingId(event.id);
    setFormData({
      title: event.title,
      event_date: event.event_date,
      event_type: event.event_type,
      note: event.note || '',
      is_yearly: event.is_yearly,
    });
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setMessage('');
    if (!formData.title.trim() || !formData.event_date) {
      return;
    }

    try {
      if (editingId) {
        await httpClient.put(`/calendar-events/${editingId}`, buildPayload(formData));
      } else {
        await httpClient.post('/calendar-events', buildPayload(formData));
      }
      resetForm();
      await refreshEvents();
    } catch {
      setMessage('日历事件保存失败');
    }
  }

  async function handleDelete(event) {
    setMessage('');
    try {
      await httpClient.delete(`/calendar-events/${event.id}`);
      if (editingId === event.id) {
        resetForm();
      }
      await refreshEvents();
    } catch {
      setMessage('日历事件删除失败');
    }
  }

  return (
    <section className="page-section">
      <div className="page-heading">
        <h1>日历备忘录</h1>
        <p>记录生日、纪念日和重要日期，支持每年重复提醒。</p>
      </div>

      <div className="calendar-layout">
        <section className="content-panel calendar-panel">
          <div className="calendar-toolbar">
            <button className="secondary-button" type="button" onClick={() => changeMonth(-1)}>
              上个月
            </button>
            <h2>{monthKey}</h2>
            <button className="secondary-button" type="button" onClick={() => changeMonth(1)}>
              下个月
            </button>
          </div>
          <div className="calendar-weekdays">
            {['日', '一', '二', '三', '四', '五', '六'].map((day) => (
              <span key={day}>{day}</span>
            ))}
          </div>
          <div className="calendar-grid">
            {days.map((day) => (
              <div className={`calendar-day ${day.isCurrentMonth ? '' : 'is-muted'}`} key={day.date}>
                <strong>{day.dayNumber}</strong>
                <div className="calendar-day-events">
                  {(eventsByDate[day.date] || []).slice(0, 3).map((event) => (
                    <button className={`calendar-event-chip ${event.event_type}`} key={event.id} type="button" onClick={() => startEdit(event)}>
                      {event.title}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>

        <form className="content-panel calendar-form" onSubmit={handleSubmit}>
          <h2>{editingId ? '编辑事件' : '新增事件'}</h2>
          <label>
            标题
            <input name="title" value={formData.title} onChange={handleFormChange} maxLength={120} required />
          </label>
          <label>
            日期
            <input name="event_date" type="date" value={formData.event_date} onChange={handleFormChange} required />
          </label>
          <label>
            类型
            <select name="event_type" value={formData.event_type} onChange={handleFormChange}>
              <option value="birthday">生日</option>
              <option value="anniversary">纪念日</option>
              <option value="other">其他</option>
            </select>
          </label>
          <label className="calendar-check">
            <input name="is_yearly" type="checkbox" checked={formData.is_yearly} onChange={handleFormChange} />
            每年重复
          </label>
          <label>
            备注
            <textarea name="note" value={formData.note} onChange={handleFormChange} rows={4} maxLength={1000} />
          </label>
          <div className="editor-actions">
            <button type="submit">{editingId ? '保存事件' : '新增事件'}</button>
            {editingId ? (
              <button className="secondary-button" type="button" onClick={resetForm}>
                取消
              </button>
            ) : null}
          </div>
        </form>
      </div>

      {message ? <p className="form-error relation-error">{message}</p> : null}
      {isLoading ? <div className="content-panel">正在加载日历事件...</div> : null}

      <div className="calendar-event-list">
        {events.map((event) => (
          <article className="content-panel calendar-event-item" key={`${event.id}-${event.display_date}`}>
            <div>
              <h2>{event.title}</h2>
              <p>
                {eventTypeLabels[event.event_type]} · {event.display_date}
                {event.is_yearly ? ' · 每年重复' : ''}
              </p>
              {event.note ? <p>{event.note}</p> : null}
            </div>
            <div className="editor-actions">
              <button type="button" onClick={() => startEdit(event)}>
                编辑
              </button>
              <button className="secondary-button" type="button" onClick={() => handleDelete(event)}>
                删除
              </button>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

export default CalendarPage;
