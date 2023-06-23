import React from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';

import { Settings, defaultSettings } from './Settings';


interface SettingsFormProps {
  onSubmit: (settings: Settings) => void;
}

function SettingsForm({ onSubmit }: SettingsFormProps) {
  const { register, handleSubmit, formState: { errors } } = useForm<Settings>({ defaultValues: defaultSettings });

  const handleSubmit2 = (settings: Settings) => {
    axios.post('/api/init', settings)
      .then((response) => { console.log(response.data); })
      .catch((error) => { console.error(error); });
    onSubmit(settings);
  };

  const tooLow = "value is too low";
  const tooHigh = "value is too high";
  const isNumber = (value: any) => (typeof value == "number" && !Number.isNaN(value)) || "value is not a number";
  const one_to_million = { 
    valueAsNumber: true, validate: isNumber, min: {value: 1, message: tooLow}, max: {value: 1000000, message: tooHigh }
  };
  const one_to_forty = {
    valueAsNumber: true, validate: isNumber, min: {value: 1, message: tooLow}, max: {value: 40, message: tooHigh }
  };
  const zero_to_one = {
    valueAsNumber: true, validate: isNumber, min: {value: 0.0, message: tooLow}, max: {value: 1.0, message: tooHigh }
  };
  const one_tenth = {
    valueAsNumber: true, validate: isNumber, min: {value: 0.1, message: tooLow}
};

  return (
    <form aria-label="Settings Form" onSubmit={ handleSubmit(handleSubmit2) }>
      <div id="numberOfMessages" className="row">
        <label htmlFor="numberOfMessages">No. of messages (max: 1000000):</label>
        <input type="text" { ...register("numberOfMessages", one_to_million) } />
        { errors.numberOfMessages && <span className="error">{errors.numberOfMessages.message}</span> }
      </div>

      <div id="processCount" className="row">
        <label htmlFor="numberOfProcesses">No. of processes (max: 40):</label>
        <input type="text" { ...register("numberOfProcesses", one_to_forty) } />
        { errors.numberOfProcesses && <span className="error">{errors.numberOfProcesses.message}</span> }
      </div>

      <div id="failureRate" className="row">
        <label htmlFor="failureRate">Failure rate (0.0 - 1.0):</label>
        <input type="text" { ...register("failureRate", zero_to_one) } />
        { errors.failureRate && <span className="error">{errors.failureRate.message}</span> }
      </div>

      <div id="monitoringInterval" className="row">
        <label htmlFor="monitoringInterval">Monitoring interval (min: 0.1 sec):</label>
        <input type="text" { ...register("monitoringInterval", one_tenth) } />
        { errors.monitoringInterval && <span className="error">{errors.monitoringInterval.message}</span> }
      </div>

      <button type="submit" className="row">Submit</button>
    </form>
  );
}

export default SettingsForm;
