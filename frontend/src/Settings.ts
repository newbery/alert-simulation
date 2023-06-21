
export interface Settings {
  numberOfMessages: string;
  numberOfProcesses: string;
  failureRate: string;
  monitoringInterval: string;
};

export const defaultSettings: Settings = {
  numberOfMessages: '1000',
  numberOfProcesses: '1',
  failureRate: '.5',
  monitoringInterval: '10',
};
