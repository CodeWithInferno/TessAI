// constants.js

const EXCLUDED_DIRS = new Set([
    "node_modules", ".next", ".cache", "__pycache__", ".git", ".venv", "venv", 
    "Library", "Applications", "System", "private", "Volumes", "usr", "bin", "opt", 
    "cores", "dev", "sbin", "etc", "tmp", "var", "Network", "Preboot", "Recovery", "home",
    "$Recycle.Bin", "Program Files", "Program Files (x86)", "Windows", "AppData"
  ]);
  
  const USEFUL_EXTENSIONS = new Set([
    ".txt", ".md", ".pdf", ".docx", ".xlsx", ".pptx", ".py", ".js", ".ts", ".json",
    ".html", ".css", ".cpp", ".c", ".java", ".swift", ".sh", ".sql", ".jpg", ".png"
  ]);
  
  module.exports = {
    EXCLUDED_DIRS,
    USEFUL_EXTENSIONS
  };
  