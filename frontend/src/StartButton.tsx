import React from 'react';
import axios from 'axios';

import { Settings } from './Settings';


interface StartButtonProps {
  settings: Settings;
  disabled: boolean;
  onStart: () => void;
}

function StartButton({ settings, disabled, onStart }: StartButtonProps) {

  const handleStart = () => {
    onStart();
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
