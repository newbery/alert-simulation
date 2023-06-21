import React, { useState, ChangeEvent, FormEvent } from 'react';
import axios from 'axios';

import { Settings, defaultSettings } from './Settings';


interface SettingsFormProps {
  onSubmit: (settings: Settings) => void;
}

function SettingsForm({ onSubmit }: SettingsFormProps) {
  const [settings, setSettings] = useState<Settings>(defaultSettings);

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setSettings((prevSettings) => ({...prevSettings, [name]: value}));
  };

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    axios.post('/api/init', settings)
      .then((response) => { console.log(response.data); })
      .catch((error) => { console.error(error); });
    onSubmit(settings);
  };

  return (
    <form aria-label="Settings Form" onSubmit={handleSubmit}>
      <div id="numberOfMessages">
        <label htmlFor="numberOfMessages">No. of messages:</label>
        <input type="text" id="numberOfMessages" name="numberOfMessages"
          value={settings.numberOfMessages} onChange={handleChange} />
      </div>

      <div id="processCount">
        <label htmlFor="numberOfProcesses">No. of processes:</label>
        <input type="text" id="numberOfProcesses" name="numberOfProcesses"
          value={settings.numberOfProcesses} onChange={handleChange} />
      </div>

      <div id="failureRate">
        <label htmlFor="failureRate">Failure rate (0.0-1.0):</label>
        <input type="text" id="failureRate" name="failureRate"
          value={settings.failureRate} onChange={handleChange} />
      </div>

      <div id="monitoringInterval">
        <label htmlFor="monitoringInterval">Monitoring interval (sec):</label>
        <input type="text" id="monitoringInterval" name="monitoringInterval"
          value={settings.monitoringInterval} onChange={handleChange} />
      </div>

      <button type="submit">Submit</button>
    </form>
  );
}

export default SettingsForm;
