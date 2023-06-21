import React, { useState } from 'react';

import { Settings, defaultSettings } from './Settings';
import CurrentSettings from './SettingsCurrent';
import SettingsForm from './SettingsForm';
import PollForReady from './PollForReady';
import PollForStatus from './PollForStatus';
import StartButton from './StartButton';
import ResetButton from './ResetButton';

export enum AppState {
  INIT,
  POLLING,
  READY,
  RUNNING,
}

function App() {
  const [appState, setAppState] = useState<AppState>(AppState.INIT);
  const [currentSettings, setCurrentSettings] = useState<Settings>({ ...defaultSettings });

  const handleSettingsSubmit = (settings: Settings) => {
    setCurrentSettings(settings);
    setAppState(AppState.POLLING);
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
        {showSettings.includes(appState) && (
          <>
            <CurrentSettings settings={currentSettings} />
            <div id="buttons">
              <StartButton onStart={handleStart} settings={currentSettings} disabled={disableStart.includes(appState)} />
              <ResetButton onReset={handleReset} />
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
