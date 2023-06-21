import React, { useState, useEffect } from 'react';
import axios from 'axios';

import { Settings } from './Settings';


interface PollForStatusProps {
  settings: Settings;
}

interface JsonData {
  [key: string]: string;
}

const defaultJsonData: JsonData = {
  count: '0',
  failed: '0',
  average_time: '0',
};

function PollForStatus({ settings }: PollForStatusProps) {
  const [jsonData, setJsonData] = useState<JsonData>(defaultJsonData);

  useEffect(() => {

    const intervalId = setInterval(() => {
      axios.get('/api/status')
        .then((response) => { setJsonData(response.data); })
        .catch((error) => { console.error(error); });
    }, parseFloat(settings.monitoringInterval) * 1000);

    // Cleanup the interval when component unmounts
    return () => clearInterval(intervalId);
  }, [settings.monitoringInterval]);

  return (
    <div>
        <p key="count">
          <span>Count: </span>
          <span>{jsonData['count']}</span>
        </p>
        <p key="failed">
          <span>Failed: </span>
          <span>{jsonData['failed']}</span>
        </p>
        <p key="average_time">
          <span>Average time: </span>
          <span>{jsonData['average_time']}</span>
        </p>
    </div>
  );
}

export default PollForStatus;
