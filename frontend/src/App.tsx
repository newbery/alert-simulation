import React, { useState } from 'react';

import { Settings, defaultSettings } from './Settings';
import CurrentSettings from './SettingsCurrent';
import SettingsForm from './SettingsForm';
import JoinForm from './JoinForm';
import PollForReady from './PollForReady';
import PollForStatus from './PollForStatus';
import StartButton from './StartButton';
import ResetButton from './ResetButton';

export enum AppState {
  INIT,
  JOIN,
  POLLING,
  READY,
  RUNNING,
}

function App() {
  const [appState, setAppState] = useState<AppState>(AppState.INIT);
  const [currentSettings, setCurrentSettings] = useState<Settings>({ ...defaultSettings });

  const handleSettingsSubmit = (settings: Settings, showJoin: boolean) => {
    setCurrentSettings(settings);
    if (showJoin) {
      setAppState(AppState.JOIN);
    } else {
      setAppState(AppState.POLLING);
    };
  };

  const handleJoinSubmit = (settings: Settings, showJoin: boolean) => {
    setCurrentSettings(settings);
    if (showJoin) {
      setAppState(AppState.JOIN);
    } else {
      setAppState(AppState.RUNNING);
    };
  };

  const handleReady = () => {
    setAppState(AppState.READY);
  };

  const handleStart = () => {
    setAppState(AppState.RUNNING);
  };

  const handleReset = () => {
    setCurrentSettings({ ...defaultSettings });
    setAppState(AppState.INIT);
  };
  
  const showSettings = [AppState.POLLING, AppState.READY, AppState.RUNNING];
  const disableStart = [AppState.POLLING, AppState.RUNNING];

  return (
    <>
      <div id="controls">
        {appState === AppState.INIT && <SettingsForm onSubmit={handleSettingsSubmit} />}
        {appState === AppState.JOIN && <JoinForm settings={currentSettings} onSubmit={handleJoinSubmit} />}
        {showSettings.includes(appState) && (
          <>
            <CurrentSettings settings={currentSettings} />
            <div id="buttons">
              <StartButton settings={currentSettings} disabled={disableStart.includes(appState)} onStart={handleStart} />
              <ResetButton settings={currentSettings} onReset={handleReset} />
            </div>
          </>
        )}
      </div>
      <div id="results">
        {appState === AppState.POLLING && <PollForReady key="poll-ready" onReady={handleReady} settings={currentSettings} />}
        {appState === AppState.RUNNING && <PollForStatus key="poll-status" settings={currentSettings} />}
      </div>
    </>
  );
}

export default App;
