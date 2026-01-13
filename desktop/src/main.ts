import { app, BrowserWindow } from "electron";
import * as path from "path";
import { spawn, ChildProcess } from "child_process";

let mainWindow: BrowserWindow | null = null;
let backendProcess: ChildProcess | null = null;
const BACKEND_PORT = 8000;

async function startBackend(): Promise<void> {
  return new Promise((resolve, reject) => {
    const backendPath = path.join(__dirname, "../../backend");
    const pythonCmd = process.platform === "win32" ? "python" : "python3";

    console.log("Starting backend at:", backendPath);

    // Start uvicorn
    backendProcess = spawn(
      pythonCmd,
      ["-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", BACKEND_PORT.toString()],
      {
        cwd: backendPath,
        stdio: "inherit",
      }
    );

    backendProcess.on("error", (error) => {
      console.error("Failed to start backend:", error);
      reject(error);
    });

    // Wait for backend to be ready (simple polling)
    const maxRetries = 20;
    let retries = 0;

    const checkBackend = setInterval(() => {
      fetch(`http://127.0.0.1:${BACKEND_PORT}/health`)
        .then((response) => {
          if (response.ok) {
            clearInterval(checkBackend);
            console.log("Backend is ready");
            resolve();
          }
        })
        .catch(() => {
          retries++;
          if (retries >= maxRetries) {
            clearInterval(checkBackend);
            reject(new Error("Backend failed to start in time"));
          }
        });
    }, 500);
  });
}

function createWindow(): void {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  // Load frontend
  if (process.env.NODE_ENV === "development") {
    mainWindow.loadURL("http://localhost:5173");
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, "../../frontend/index.html"));
  }

  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

app.whenReady().then(async () => {
  try {
    await startBackend();
    createWindow();
  } catch (error) {
    console.error("Failed to start application:", error);
    app.quit();
  }
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  if (mainWindow === null) {
    createWindow();
  }
});

app.on("before-quit", () => {
  if (backendProcess) {
    console.log("Stopping backend process");
    backendProcess.kill("SIGTERM");
    backendProcess = null;
  }
});

process.on("SIGTERM", () => {
  app.quit();
});
