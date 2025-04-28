// deviceManager.js

const fs = require('fs');
const path = require('path');
const os = require('os');
const { v4: uuidv4 } = require('uuid');

const TESS_FOLDER = path.join(os.homedir(), "TessAI");
const DEVICE_ID_FILE = path.join(TESS_FOLDER, "device_id.txt");
const USERNAME_FILE = path.join(TESS_FOLDER, "user_prefix.txt"); // new file to store prefix

function askUserPrefix() {
  const readline = require('readline-sync');
  const prefix = readline.question("Enter your device name (e.g., Pratham_Macbook): ");
  return prefix.trim().replace(/\s+/g, '_'); // replace spaces with underscore
}

function getOrCreateDeviceId() {
  if (!fs.existsSync(TESS_FOLDER)) {
    fs.mkdirSync(TESS_FOLDER, { recursive: true });
  }

  if (fs.existsSync(DEVICE_ID_FILE)) {
    return fs.readFileSync(DEVICE_ID_FILE, 'utf-8').trim();
  }

  let prefix = "";
  if (fs.existsSync(USERNAME_FILE)) {
    prefix = fs.readFileSync(USERNAME_FILE, 'utf-8').trim();
  } else {
    prefix = askUserPrefix();
    fs.writeFileSync(USERNAME_FILE, prefix);
  }

  const platform = os.platform(); // e.g., darwin, win32
  const hostname = os.hostname(); // e.g., Prathams-MacBook-Air.local
  const shortid = uuidv4().slice(0, 8); // only 8 chars

  const deviceId = `${prefix}_${platform}_${hostname}_${shortid}`;
  fs.writeFileSync(DEVICE_ID_FILE, deviceId);

  return deviceId;
}

module.exports = {
  getOrCreateDeviceId
};
