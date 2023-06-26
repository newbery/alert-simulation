import { v4 as uuid } from 'uuid';

export interface Settings {
  sessionId: string;
  sessionKey: string;
  numberOfMessages: number;
  numberOfProcesses: number;
  failureRate: number;
  monitoringInterval: number;
};

export const defaultSettings: Settings = {
  sessionId: uuid(),
  sessionKey: "",
  numberOfMessages: 1000,
  numberOfProcesses: 4,
  failureRate: 0.0,
  monitoringInterval: 1.0,
};
