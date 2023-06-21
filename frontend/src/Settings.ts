
export interface Settings {
  numberOfMessages: number;
  numberOfProcesses: number;
  failureRate: number;
  monitoringInterval: number;
};

export const defaultSettings: Settings = {
  numberOfMessages: 1000,
  numberOfProcesses: 10,
  failureRate: 0.0,
  monitoringInterval: 1.0,
};
