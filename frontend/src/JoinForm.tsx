import React from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';

import { Settings } from './Settings';


interface JoinFormProps {
  settings: Settings;
  onSubmit: (settings: Settings, showJoin: boolean) => void;
  showJoin?: boolean;
}

function JoinForm({ settings, onSubmit, showJoin = false }: JoinFormProps) {
  const { register, handleSubmit, formState: { errors } } = useForm<Settings>({ defaultValues: settings });

  const handleSubmit2 = (settings: Settings) => {
    axios.post('/api/ready', settings)
      .then((response) => {
        const data = response.data;
        console.log(data);
        console.log(settings);
        // Once again, if another session exists, take those values and trigger joinForm again
        if (settings.sessionId !== data.session_id) {
          showJoin = true;
          settings.sessionId = data.session_id;
          settings.numberOfMessages = data.number_of_messages;
          settings.numberOfProcesses = data.number_of_processes;
          settings.failureRate = data.failure_rate;
          settings.monitoringInterval = data.monitoring_interval;
        };
        settings.sessionKey = "";
        console.log(settings);
        console.log(showJoin);
        onSubmit(settings, showJoin);
      })
      .catch((error) => { console.error(error); });
  };

  return (
    <form aria-label="Join Form" onSubmit={ handleSubmit(handleSubmit2) }>

      <p>Another session already exists. Join if you know the session key.</p>

      <div aria-label="Current Settings">

        <p>No. of messages: {settings.numberOfMessages}</p>
        <p>No. of processes: {settings.numberOfProcesses}</p>
        <p>Failure rate (0.0-1.0): {settings.failureRate}</p>
        <p>Monitoring interval (seconds): {settings.monitoringInterval}</p>

        <div id="sessionKey" className="row">
        <label htmlFor="sessionKey">Session key:</label>
        <input type="text" { ...register("sessionKey", { required: "session key is required" }) } />
        { errors.sessionKey && <span className="error">{errors.sessionKey.message}</span> }
        </div>
      </div>

      <input type="hidden" { ...register("sessionId") } />
      <input type="hidden" { ...register("numberOfMessages") } />
      <input type="hidden" { ...register("numberOfProcesses") } />
      <input type="hidden" { ...register("failureRate") } />
      <input type="hidden" { ...register("monitoringInterval") } />
            
      <button type="submit" className="row">Submit</button>
    </form>

  );
}

export default JoinForm;
