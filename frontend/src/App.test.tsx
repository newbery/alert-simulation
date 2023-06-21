import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import App from './App';

describe('App', () => {
  test('when appState is INIT, renders SettingsForm', () => {
    const { getByLabelText } = render(<App />);
    const settingsForm = getByLabelText('Settings Form');
    
    expect(settingsForm).toBeInTheDocument();
  });

  test('when appState is POLLING, renders CurrentSettings, StartButton, ResetButton, and PollForReady', () => {
    const { getByLabelText, getByText } = render(<App />);
    
    fireEvent.click(getByText('Submit')); // Trigger state change to POLLING

    const currentSettings = getByLabelText('Current Settings');
    expect(currentSettings).toBeInTheDocument();
    
    const startButton = getByText('Start');
    expect(startButton).toBeInTheDocument();

    const resetButton = getByText('Reset');
    expect(resetButton).toBeInTheDocument();

    const pollForReady = getByText('Waiting for the backend to be ready...');
    expect(pollForReady).toBeInTheDocument();
  });

  test('when appState is READY, renders CurrentSettings, StartButton, and ResetButton', () => {
    const { getByLabelText, getByText } = render(<App />);

    fireEvent.click(getByText('Submit')); // Trigger a state change to POLLING

    // TODO: Do something here to trigger state change to READY
    
    const currentSettings = getByLabelText('Current Settings');
    expect(currentSettings).toBeInTheDocument();
    
    const startButton = getByText('Start');
    expect(startButton).toBeInTheDocument();

    const resetButton = getByText('Reset');
    expect(resetButton).toBeInTheDocument();
    
    // TODO: Add an assert that the 'Waiting...' text is not in document
  });

  test('when appState is RUNNING, renders the CurrentSettings, StartButton, ResetButton, and PollForStatus component', () => {
    const { getByLabelText, getByText } = render(<App />);

    fireEvent.click(getByText('Submit')); // Trigger a state change to POLLING

    // TODO: Do something here to trigger state change to READY

    fireEvent.click(getByText('Start')); // Trigger a state change to RUNNING

    const status = getByLabelText('Status');
    expect(status).toBeInTheDocument();

  });

});
