import React, { useState, useEffect } from 'react';
import axios from 'axios';

import { Settings } from './Settings';


interface PollForStatusProps {
  settings: Settings;
}

type statusKeys = "count" | "failed" | "average_time"
type currentStatus = Record<statusKeys, number>

const defaultCurrentStatus: currentStatus = {
  count: 0,
  failed: 0,
  average_time: 0,
};

function PollForStatus({ settings }: PollForStatusProps) {
  const [currentStatus, setCurrentStatus] = useState<currentStatus>(defaultCurrentStatus);

  useEffect(() => {

    const intervalId = setInterval(() => {
      axios.post('/api/status', settings)
        .then((response) => { setCurrentStatus(response.data); })
        .catch((error) => { console.error(error); });
    }, settings.monitoringInterval * 1000);

    return () => clearInterval(intervalId);
  }, [settings]);

  return (
    <div>
        <p key="count">
          <span>Count: </span>
          <span>{currentStatus?.count}</span>
        </p>
        <p key="failed">
          <span>Failed: </span>
          <span>{currentStatus?.failed}</span>
        </p>
        <p key="average_time">
          <span>Average time: </span>
          <span>{currentStatus?.average_time}</span>
        </p>
    </div>
  );
}

export default PollForStatus;
