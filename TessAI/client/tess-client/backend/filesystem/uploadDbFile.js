const fs = require('fs');
const path = require('path');
const os = require('os');
const axios = require('axios');
const FormData = require('form-data');
const { getOrCreateDeviceId } = require('../setup/deviceManager');

const SERVER_URL = "https://selections-minority-nightlife-safer.trycloudflare.com/upload-db"; // <-- change this to your new FastAPI endpoint
const DB_FILE_PATH = path.join(os.homedir(), "TessAI", "File_Dir.db");

async function uploadDbFile() {
  if (!fs.existsSync(DB_FILE_PATH)) {
    console.error("❌ No database file found to upload:", DB_FILE_PATH);
    return;
  }

  const deviceId = getOrCreateDeviceId();

  console.log(`📦 Uploading database file for device: ${deviceId}`);

  const form = new FormData();
  form.append('device_id', deviceId);
  form.append('file', fs.createReadStream(DB_FILE_PATH));

  try {
    const res = await axios.post(SERVER_URL, form, {
      headers: form.getHeaders(),
      maxContentLength: Infinity,
      maxBodyLength: Infinity,
      timeout: 60000
    });

    console.log("✅ Database upload success:", res.data.message || res.statusText);
  } catch (error) {
    console.error("❌ Database upload failed:", error.message);
  }
}

module.exports = {
  uploadDbFile
};
