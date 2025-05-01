// filesystem/scanFiles.js

const fs = require("fs");
const path = require("path");
const os = require("os");
const { initDb } = require("./database");

// Directories we always ignore
const EXCLUDED_DIRS = new Set([
  "node_modules", ".next", ".cache", "__pycache__", ".git", ".venv", "venv",
  "Library", "Applications", "System", "private", "Volumes", "usr", "bin", 
  "opt", "cores", "dev", "sbin", "etc", "tmp", "var", "Network", "Preboot", "Recovery", "home",
  "$Recycle.Bin", "Program Files", "Program Files (x86)", "Windows", "AppData"
]);

const APPLICATIONS_FOLDER = "/Applications";

// ===== Recursive Directory Scanner =====
function scanDirectory(dirPath, db) {
  if (!fs.existsSync(dirPath)) return;

  const entries = fs.readdirSync(dirPath, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dirPath, entry.name);

    if (EXCLUDED_DIRS.has(entry.name)) {
      continue; // Skip garbage folders
    }

    try {
      if (entry.isDirectory()) {
        db.prepare(`
          INSERT INTO files (path, name, is_dir, extension, size)
          VALUES (?, ?, ?, ?, ?)
        `).run(
          String(fullPath),
          String(entry.name),
          true,
          "",
          0 // Folders have no size
        );

        // Recursively scan subdirectories
        scanDirectory(fullPath, db);

      } else if (entry.isFile()) {
        const ext = path.extname(entry.name).toLowerCase();
        const stats = fs.statSync(fullPath);
        const size = (typeof stats.size === "number") ? stats.size : 0;

        db.prepare(`
          INSERT INTO files (path, name, is_dir, extension, size)
          VALUES (?, ?, ?, ?, ?)
        `).run(
          String(fullPath),
          String(entry.name),
          false,
          String(ext),
          size
        );
      }
    } catch (error) {
      console.warn(`⚠️ Skipped ${fullPath}: ${error.message}`);
    }
  }
}

// ===== Specific Applications Folder Scanner =====
function scanApplicationsFolder(db) {
  if (!fs.existsSync(APPLICATIONS_FOLDER)) return;

  const apps = fs.readdirSync(APPLICATIONS_FOLDER);

  for (const app of apps) {
    const fullPath = path.join(APPLICATIONS_FOLDER, app);

    if (!app.endsWith(".app")) continue; // Only scan .app bundles

    try {
      const stats = fs.statSync(fullPath);
      const size = (typeof stats.size === "number") ? stats.size : 0;

      db.prepare(`
        INSERT INTO files (path, name, is_dir, extension, size)
        VALUES (?, ?, ?, ?, ?)
      `).run(
        String(fullPath),
        String(app),
        true,
        ".app",
        size
      );

    } catch (error) {
      console.warn(`⚠️ Skipped application ${fullPath}: ${error.message}`);
    }
  }

  console.log(`✅ Scanned and stored apps from /Applications`);
}

// ===== Main Function to Scan Everything =====
async function scanAndStoreFiles() {
  const db = initDb();

  console.log("🔍 Scanning user directories...");

  const userDirs = [
    path.join(os.homedir(), "Desktop"),
    path.join(os.homedir(), "Documents"),
    path.join(os.homedir(), "Downloads"),
    os.homedir()
  ];

  for (const dir of userDirs) {
    scanDirectory(dir, db);
  }

  console.log("🔍 Scanning Applications folder...");
  scanApplicationsFolder(db);

  db.close();
  console.log("✅ Scanning complete!");
}

module.exports = {
  scanAndStoreFiles
};
