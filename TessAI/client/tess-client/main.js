// const { app, BrowserWindow, ipcMain } = require('electron')
// const path = require('path')
// const axios = require('axios') // Install axios if needed
// const { runSetup } = require('./backend/setup/setupManager');



// app.whenReady().then(async () => {
//   await runSetup(); // <-- FIRST run setup if needed
//   createWindow();
// });
// function createWindow() {
//   const win = new BrowserWindow({
//     width: 900,
//     height: 700,
//     webPreferences: {
//       preload: path.join(__dirname, 'preload.js')
//     }
//   })

//   win.loadFile('index.html')
// }

// app.whenReady().then(() => {
//   createWindow()

//   app.on('activate', function () {
//     if (BrowserWindow.getAllWindows().length === 0) createWindow()
//   })

//   ipcMain.handle('chat-message', async (event, message) => {
//     try {
//       const res = await axios.post('https://selections-minority-nightlife-safer.trycloudflare.com/chat', {
//         query: message,
//         device_id: "Darwin_Prathams-MacBook-Air.local_775abecf" // replace dynamically later
//       })
//       return res.data.response
//     } catch (err) {
//       console.error("API Error:", err)
//       return "❌ Tess server not reachable."
//     }
//   })
// }) // <-- this closes the app.whenReady() properly!!

// app.on('window-all-closed', function () {
//   if (process.platform !== 'darwin') app.quit()
// })

const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')
const axios = require('axios')
const { exec } = require('child_process')
const { runSetup } = require('./backend/setup/setupManager')

// === Create Browser Window ===
function createWindow() {
  const win = new BrowserWindow({
    width: 900,
    height: 700,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  })

  win.loadFile('index.html')
}

// === When Electron App is Ready ===
app.whenReady().then(async () => {
  await runSetup(); // First-time setup
  createWindow();
})

// === IPC Handlers ===

// Handle Chat Message to Tess Server
ipcMain.handle('chat-message', async (event, message) => {
  try {
    const res = await axios.post('https://working-screw-fairy-cake.trycloudflare.com/chat', {
      query: message,
      device_id: "Darwin_Prathams-MacBook-Air.local_775abecf"
    });

    console.log("📡 Full server response:", res.data);

    return {
      intent: res.data.intent || "chat",
      response: res.data.response || "❌ No response from server."
    };

  } catch (err) {
    console.error("API Error:", err)
    return {
      intent: "error",
      response: "❌ Tess server not reachable."
    };
  }
});


// Handle Tess Actions (Run commands / Open file / Open URL)
ipcMain.handle('tess-action', async (event, action) => {
  console.log("⚙️ Received Action:", action);

  if (!action || !action.type) {
    console.error("⚠️ Invalid action object.");
    return;
  }

  try {
    if (action.type === "terminal_command") {
      const command = action.command;
      if (!command) throw new Error("No command provided.");

      if (process.platform === "darwin") { // macOS
        exec(`osascript -e 'tell application "Terminal" to do script "${command}"'`);
      } else if (process.platform === "win32") { // Windows
        exec(`start cmd /k "${command}"`);
      } else { // Linux
        exec(command);
      }

      return "✅ Terminal command executed.";
    }
    else if (action.type === "open_file" || action.type === "open_url") {
      const { default: open } = await import('open'); // <-- move import INSIDE here!
      const target = action.type === "open_file" ? action.path : action.url;
      if (!target) throw new Error("No path or URL provided.");
      await open(target);
      return `✅ ${action.type === "open_file" ? "File" : "URL"} opened.`;
    }
    else {
      console.error("⚠️ Unknown action type:", action.type);
      return "⚠️ Unknown action.";
    }
  } catch (error) {
    console.error("❌ Error executing action:", error.message);
    return `❌ Error: ${error.message}`;
  }
})

// === Handle app close ===
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})

// === Handle app re-activate on Mac ===
app.on('activate', function () {
  if (BrowserWindow.getAllWindows().length === 0) createWindow()
})


