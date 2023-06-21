import React from 'react';
import axios from 'axios';


interface ResetButtonProps {
  onReset: () => void;
}

function ResetButton({ onReset }: ResetButtonProps) {
  const handleReset = () => {
    onReset();
    // Make an API call to reset the action
    axios.post('/api/reset')
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
