import { useEffect, useState } from 'react';

import httpClient from '../api/http-client';

function ApiStatus() {
  const [status, setStatus] = useState('检测中');

  useEffect(() => {
    let isMounted = true;

    async function fetchHealth() {
      try {
        const response = await httpClient.get('/health');
        if (isMounted) {
          setStatus(response.data.databaseConnected ? '后端与数据库已连接' : '数据库未连接');
        }
      } catch {
        if (isMounted) {
          setStatus('等待后端启动');
        }
      }
    }

    fetchHealth();

    return () => {
      isMounted = false;
    };
  }, []);

  return <span className="api-status">{status}</span>;
}

export default ApiStatus;
