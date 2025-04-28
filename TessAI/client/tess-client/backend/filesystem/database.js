// database.js

const path = require('path');
const fs = require('fs');
const Database = require('better-sqlite3'); // Install this: npm install better-sqlite3

const HOME_PATH = require('os').homedir();
const DB_FOLDER = path.join(HOME_PATH, "TessAI");
const DB_FILE = path.join(DB_FOLDER, "File_Dir.db");

function initDb() {
  if (!fs.existsSync(DB_FOLDER)) {
    fs.mkdirSync(DB_FOLDER, { recursive: true });
  }

  const db = new Database(DB_FILE);

  db.exec(`
    CREATE TABLE IF NOT EXISTS files (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      path TEXT,
      name TEXT,
      is_dir BOOLEAN,
      extension TEXT,
      size INTEGER
    )
  `);
  db.exec(`CREATE INDEX IF NOT EXISTS idx_path ON files(path)`);

  return db;
}

module.exports = {
  initDb,
  DB_FILE
};
