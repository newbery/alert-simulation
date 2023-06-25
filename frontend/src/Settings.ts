import { v4 as uuid } from 'uuid';
import { generate } from 'random-words';

export interface Settings {
  sessionId: string;
  sessionName: string;
  sessionSecret: string;
  numberOfMessages: number;
  numberOfProcesses: number;
  failureRate: number;
  monitoringInterval: number;
};

export const defaultSettings: Settings = {
  sessionId: uuid(),
  sessionName: "anon",
  sessionSecret: generate({ exactly: 3, maxLength: 6, join: "-" }),
  numberOfMessages: 1000,
  numberOfProcesses: 4,
  failureRate: 0.0,
  monitoringInterval: 1.0,
};
