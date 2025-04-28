// // setupManager.js

// const fs = require("fs");
// const path = require("path");
// const os = require("os");
// const { v4: uuidv4 } = require("uuid"); // npm install uuid
// const { scanAndStoreFiles } = require("../filesystem/scanFiles");
// const { initDb, DB_FILE } = require("../filesystem/database");
// const axios = require("axios");
// const { getOrCreateDeviceId } = require("./deviceManager");

// const SERVER_URL = "https://your-server.com/upload-files"; // <-- Replace with your FastAPI URL
// const SETUP_MARKER_FILE = path.join(os.homedir(), "TessAI", "setup_done.txt");
// const DEVICE_ID_FILE = path.join(os.homedir(), "TessAI", "device_id.txt");
// const CHUNK_SIZE = 500; // number of files per upload batch

// // ==== Device ID Management ====

// // ==== Setup Check ====

// function isSetupDone() {
//   return fs.existsSync(SETUP_MARKER_FILE);
// }

// // ==== Chunked Upload Logic ====

// async function uploadFiles() {
//   const db = initDb();
//   const rows = db.prepare('SELECT path, name, is_dir, extension, size FROM files').all();
//   const deviceId = getOrCreateDeviceId();
//   const CHUNK_SIZE = 10; // tiny

//   console.log(`📄 Preparing ${rows.length} file entries to upload...`);

//   for (let i = 0; i < rows.length; i += CHUNK_SIZE) {
//     const chunk = rows.slice(i, i + CHUNK_SIZE).map(row => ({
//       device_id: deviceId,
//       path: row.path,
//       name: row.name,
//       is_dir: row.is_dir,
//       extension: row.extension,
//       size: row.size
//     }));

//     try {
//       const res = await axios.post(SERVER_URL, chunk, {
//         headers: { 'Content-Type': 'application/json' },
//         maxContentLength: Infinity,
//         maxBodyLength: Infinity,
//         timeout: 30000 // 30 seconds for bigger uploads
//       });
//       console.log(`✅ Uploaded chunk ${i / CHUNK_SIZE + 1}:`, res.data.message);
//     } catch (err) {
//       console.error(`❌ Failed uploading chunk ${i / CHUNK_SIZE + 1}:`, err.message);
//       break;
//     }
//   }

//   console.log("✅ All files uploaded!");
// }


// // ==== Full Setup Runner ====

// async function runSetup() {
//   if (isSetupDone()) {
//     console.log("✅ Setup already completed.");
//     return;
//   }

//   console.log("⚙️ Starting first-time setup...");

//   scanAndStoreFiles();
//   await uploadFiles();

//   fs.writeFileSync(
//     SETUP_MARKER_FILE,
//     "Setup completed at " + new Date().toISOString()
//   );
//   console.log("✅ Setup completed and marker saved.");
// }

// module.exports = {
//   runSetup,
//   isSetupDone,
// };




// setupManager.js

const fs = require("fs");
const path = require("path");
const os = require("os");
const { scanAndStoreFiles } = require("../filesystem/scanFiles");
const { uploadDbFile } = require("../filesystem/uploadDbFile");

const SETUP_MARKER_FILE = path.join(os.homedir(), "TessAI", "setup_done.txt");

// ==== Setup Done Check ====

function isSetupDone() {
  return fs.existsSync(SETUP_MARKER_FILE);
}

// ==== Full Setup Runner ====

async function runSetup() {
  if (isSetupDone()) {
    console.log("✅ Setup already completed.");
    return;
  }

  console.log("⚙️ Starting first-time setup...");

  scanAndStoreFiles(); // <-- Scans files and saves into File_Dir.db
  await uploadDbFile(); // <-- Uploads the File_Dir.db to server

  fs.writeFileSync(
    SETUP_MARKER_FILE,
    "Setup completed at " + new Date().toISOString()
  );

  console.log("✅ Setup completed and marker saved.");
}

// ==== Exports ====

module.exports = {
  runSetup,
  isSetupDone
};
