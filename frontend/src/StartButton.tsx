import React from 'react';
import axios from 'axios';

import { Settings } from './Settings';


interface StartButtonProps {
  onStart: () => void;
  settings: Settings;
  disabled: boolean;
}

function StartButton({ onStart, settings, disabled }: StartButtonProps) {

  const handleStart = () => {
    onStart();
    // Make an API call to start the action
    axios.post('/api/start', settings)
      .then((response) => { console.log(response.data); })
      .catch((error) => { console.error(error); });
  };

  return (
    <div>
      <button aria-label="Start" onClick={handleStart} disabled={disabled}>Start</button>
    </div>
  );
}

export default StartButton;
