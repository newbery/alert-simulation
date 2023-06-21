import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import axios from 'axios';

import App from './App';
import PollForReady from './PollForReady';
import PollForStatus from './PollForStatus';


describe('App', () => {
  test('when appState is INIT, renders SettingsForm', () => {
    render(<App />);
    const settingsForm = screen.getByLabelText('Settings Form');
    
    expect(settingsForm).toBeInTheDocument();
  });

  test('when appState is POLLING, renders CurrentSettings, StartButton, ResetButton, and PollForReady', () => {
    render(<App />);
    
    fireEvent.click(screen.getByText('Submit')); // Trigger state change to POLLING

    const currentSettings = screen.getByLabelText('Current Settings');
    expect(currentSettings).toBeInTheDocument();
    
    const startButton = screen.getByText('Start');
    expect(startButton).toBeInTheDocument();

    const resetButton = screen.getByText('Reset');
    expect(resetButton).toBeInTheDocument();

    const pollForReady = screen.getByText('Waiting for the backend to be ready...');
    expect(pollForReady).toBeInTheDocument();
  });

  test('when appState is READY, renders CurrentSettings, StartButton, and ResetButton', () => {
    render(<App />);

    fireEvent.click(screen.getByText('Submit')); // Trigger state change to POLLING
    // ... Change state to READY
    
    const currentSettings = screen.getByLabelText('Current Settings');
    expect(currentSettings).toBeInTheDocument();
    
    const startButton = screen.getByText('Start');
    expect(startButton).toBeInTheDocument();

    const resetButton = screen.getByText('Reset');
    expect(resetButton).toBeInTheDocument();
    
    // TODO: Add an assert that the 'Waiting...' text is not in document
  });

  test('when appState is RUNNING, renders the CurrentSettings, StartButton, ResetButton, and PollForStatus component', () => {
    render(<App />);

    fireEvent.click(screen.getByText('Submit')); // Trigger a state change to POLLING
    // ... Change state to READY
    fireEvent.click(screen.getByText('Start')); // Trigger a state change to RUNNING

    const status = screen.getByLabelText('Status');
    expect(status).toBeInTheDocument();

  });

});
