import { useEffect, useState } from 'react';

import httpClient from '../api/http-client';

function ApiStatus() {
  const [status, setStatus] = useState(null);

  useEffect(() => {
    let isMounted = true;

    async function fetchHealth() {
      try {
        const response = await httpClient.get('/health');
        if (isMounted) {
          if (!response.data.databaseConnected) {
            setStatus('数据库未连接');
          } else {
            setStatus(null);
          }
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

  if (!status) return null;
  return <span className="api-status">{status}</span>;
}

export default ApiStatus;
