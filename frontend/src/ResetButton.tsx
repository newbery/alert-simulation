import React from 'react';
import axios from 'axios';

import { Settings } from './Settings';


interface ResetButtonProps {
  settings: Settings;
  onReset: () => void;
}

function ResetButton({ settings, onReset }: ResetButtonProps) {
  const handleReset = () => {
    onReset();
    axios.post('/api/reset', settings)
      .then((response) => { console.log(response.data); })
      .catch((error) => { console.error(error); });
  };

  return (
    <div>
      <button onClick={handleReset}>Reset</button>
    </div>
  );
}

export default ResetButton;
