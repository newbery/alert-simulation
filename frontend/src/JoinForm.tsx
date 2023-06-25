import React from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';

import { Settings, defaultSettings } from './Settings';


interface JoinFormProps {
  settings: Settings;
  onSubmit: (settings: Settings, showJoin: boolean) => void;
  showJoin?: boolean;
}

function JoinForm({ settings, onSubmit, showJoin = false }: JoinFormProps) {
  const { register, handleSubmit, formState: { errors } } = useForm<Settings>({ defaultValues: defaultSettings });

  const handleSubmit2 = (settings: Settings) => {
    axios.post('/api/ready', settings)
      .then((response) => {
        const data = response.data;
        console.log(data);
        // Once again, if another session exists, take those values and trigger joinForm again
        if (settings.sessionId !== data.session_id) {
          showJoin = true;
          settings.sessionId = data.session_id;
          settings.sessionSecret = "";
          settings.sessionName = data.session_name;
          settings.numberOfMessages = data.number_of_messages;
          settings.numberOfProcesses = data.number_of_processes;
          settings.failureRate = data.failure_rate;
          settings.monitoringInterval = data.monitoring_interval;
        };
        onSubmit(settings, showJoin);
      })
      .catch((error) => { console.error(error); });
  };

  return (
    <form aria-label="Join Form" onSubmit={ handleSubmit(handleSubmit2) }>

      <h3>Another session already exists. Join if you know the session key.</h3>

      <div aria-label="Current Settings">
        <p>Session name: {settings.sessionName}</p>

        <div id="sessionSecret" className="row">
        <label htmlFor="sessionSecret">Session key:</label>
        <input type="text" { ...register("sessionSecret", { required: "session key is required" }) } />
        { errors.sessionSecret && <span className="error">{errors.sessionSecret.message}</span> }
        </div>

        <p>No. of messages: {settings.numberOfMessages}</p>
        <p>No. of processes: {settings.numberOfProcesses}</p>
        <p>Failure rate (0.0-1.0): {settings.failureRate}</p>
        <p>Monitoring interval (seconds): {settings.monitoringInterval}</p>
      </div>

      <input type="hidden" { ...register("sessionName") } />
      <input type="hidden" { ...register("numberOfMessages") } />
      <input type="hidden" { ...register("numberOfProcesses") } />
      <input type="hidden" { ...register("failureRate") } />
      <input type="hidden" { ...register("monitoringInterval") } />
            
      <button type="submit" className="row">Submit</button>
    </form>

  );
}

export default JoinForm;
