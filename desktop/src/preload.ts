import { contextBridge } from "electron";

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld("electronAPI", {
  getBackendURL: (): string => {
    return "http://127.0.0.1:8000/api";
  },
});

// Type declaration for window.electronAPI
declare global {
  interface Window {
    electronAPI: {
      getBackendURL: () => string;
    };
  }
}
