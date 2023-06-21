import React, { useEffect, useRef } from 'react';
import axios, { CancelTokenSource } from 'axios';

import { Settings } from './Settings';

interface PollForReadyProps {
  onReady: () => void;
  settings: Settings;
}

function PollForReady({ onReady, settings }: PollForReadyProps) {
  const cancelTokenSourceRef = useRef<CancelTokenSource | null>(null);

  useEffect(() => {
    const cancelTokenSource = axios.CancelToken.source();
    cancelTokenSourceRef.current = cancelTokenSource;

    const intervalId = setInterval(() => {
      axios
        .post('/api/ready', settings, { cancelToken: cancelTokenSource.token })
        .then((response) => { if (response.data.ready) { onReady(); } })
        .catch((error) => {
          if (axios.isCancel(error)) {
            console.log('Request canceled:', error.message);
          } else {
            console.error(error);
          }
        });
    }, 1000);

    return () => {
      clearInterval(intervalId);
      cancelTokenSourceRef.current?.cancel('Component unmounted');
    };
  }, [onReady, settings]);

  return (
    <div>
      <p>Waiting for the backend to be ready...</p>
    </div>
  );
}

export default PollForReady;
