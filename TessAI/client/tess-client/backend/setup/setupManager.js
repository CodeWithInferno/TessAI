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
