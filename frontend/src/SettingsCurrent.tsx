import React from 'react';

import { Settings } from './Settings';


interface CurrentSettingsProps {
  settings: Settings;
}

function CurrentSettings({ settings }: CurrentSettingsProps) {
  return (
    <div aria-label="Current Settings">
      <h2>Current Settings:</h2>
      <p>No. of messages: {settings.numberOfMessages}</p>
      <p>No. of processes: {settings.numberOfProcesses}</p>
      <p>Failure rate (0.0-1.0): {settings.failureRate}</p>
      <p>Monitoring interval (seconds): {settings.monitoringInterval}</p>
    </div>
  );
}

export default CurrentSettings;
