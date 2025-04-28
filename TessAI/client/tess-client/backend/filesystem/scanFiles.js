// scanFiles.js

const fs = require('fs');
const path = require('path');
const { initDb, DB_FILE } = require('./database');
const { EXCLUDED_DIRS, USEFUL_EXTENSIONS } = require('./constants');
const os = require('os');

function shouldSkipDir(dirPath) {
  return dirPath.split(path.sep).some(part => EXCLUDED_DIRS.has(part));
}

function scanAndStoreFiles(basePath = os.homedir()) {
  const db = initDb();
  const insertFile = db.prepare(`
    INSERT INTO files (path, name, is_dir, extension, size)
    VALUES (?, ?, ?, ?, ?)
  `);

  function walkDirectory(dir) {
    if (shouldSkipDir(dir)) return;

    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch (err) {
      return;
    }

    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);

      if (entry.isDirectory()) {
        walkDirectory(fullPath);
        try {
          insertFile.run(fullPath, entry.name, true, "", 0);
        } catch (err) {
          continue;
        }
      } else if (entry.isFile()) {
        const ext = path.extname(entry.name).toLowerCase();
        if (USEFUL_EXTENSIONS.has(ext)) {
          try {
            const stat = fs.statSync(fullPath);
            insertFile.run(fullPath, entry.name, false, ext, stat.size);
          } catch (err) {
            continue;
          }
        }
      }
    }
  }

  walkDirectory(basePath);

  console.log(`✅ Done. Indexed files stored in ${DB_FILE}`);
}

module.exports = {
  scanAndStoreFiles
};
