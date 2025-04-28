// Simple renderer.js for Tess AI Client
document.addEventListener("DOMContentLoaded", () => {
  // Add initial welcome message
  addMessage("Hello! I'm Tess, your AI assistant. How can I help you today?", false)

  // Focus the input field
  document.getElementById("userInput").focus()

  // Add event listener for Enter key
  document.getElementById("userInput").addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
      sendMessage()
    }
  })
})

// Function to get current time in HH:MM format
function getCurrentTime() {
  const now = new Date()
  return now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
}

// Function to escape HTML to prevent XSS
function escapeHtml(unsafe) {
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;")
}

// Function to extract thinking section from response
function extractThinking(text) {
  // Look for <think> or <thinking> tags (case insensitive)
  const thinkRegex = /<think(?:ing)?>([\s\S]*?)<\/think(?:ing)?>/i
  const match = text.match(thinkRegex)

  if (match) {
    const thinking = match[1].trim()
    const response = text.replace(thinkRegex, "").trim()
    return { thinking, response }
  }

  return { thinking: "", response: text }
}

// Function to toggle thinking section visibility
window.toggleThinking = (button) => {
  const thinkingContent = button.nextElementSibling
  const isExpanded = thinkingContent.classList.toggle("expanded")
  button.classList.toggle("expanded")

  if (isExpanded) {
    button.querySelector(".toggle-text").textContent = "Hide thinking"
    button.querySelector("svg").innerHTML = '<polyline points="18 15 12 9 6 15"></polyline>'
  } else {
    button.querySelector(".toggle-text").textContent = "Show thinking"
    button.querySelector("svg").innerHTML = '<polyline points="6 9 12 15 18 9"></polyline>'
  }
}

// Function to add a message to the chat
// Function to add a message to the chat
function addMessage(content, isUser = false) {
  const chatDiv = document.getElementById('chat')
  const messageType = isUser ? "user" : "system"
  const time = getCurrentTime()

  let processedContent
  let thinkingContent = ""

  if (isUser) {
    // For user messages, just escape HTML
    processedContent = escapeHtml(content)
  } else {
    // For system messages, check for thinking section
    const { thinking, response } = extractThinking(content)

    if (thinking) {
      thinkingContent = thinking
    }

    // Here is the IMPORTANT part:
    // Render Markdown safely using marked.js
    processedContent = marked.parse(response)
  }

  let messageHTML = `<div class="message ${messageType}">`

  // Add thinking section if it exists
  if (thinkingContent && !isUser) {
    messageHTML += `
      <div class="thinking-container">
        <button class="thinking-toggle" onclick="toggleThinking(this)">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
          <span class="toggle-text">Show thinking</span>
        </button>
        <div class="thinking-content">
          <div class="thinking-content-inner">${escapeHtml(thinkingContent)}</div>
        </div>
      </div>
    `
  }

  messageHTML += `
    <div class="message-content">
      <div>${processedContent}</div> <!-- Notice this is DIV because marked returns HTML -->
    </div>
    <div class="message-time">${time}</div>
  </div>`

  chatDiv.innerHTML += messageHTML

  // Scroll to the bottom
  chatDiv.scrollTop = chatDiv.scrollHeight

  // After adding the message, highlight any code blocks
  document.querySelectorAll('pre code').forEach((block) => {
    hljs.highlightElement(block)
  });
}


// Send message function
async function sendMessage() {
  const input = document.getElementById("userInput")
  const userMessage = input.value.trim()

  if (!userMessage) return

  addMessage(userMessage, true)
  input.value = ""

  try {
    const serverResponse = await window.electronAPI.sendChat(userMessage)
    console.log("📩 Server Response:", serverResponse)

    // Try to parse special actions
    const extractedAction = extractActionFromResponse(serverResponse);

    if (extractedAction) {
      console.log("🛠 Detected Action:", extractedAction)
      await window.electronAPI.sendAction(extractedAction);
    } else {
      addMessage(serverResponse)
    }

  } catch (error) {
    console.error("Error sending message:", error)
    addMessage("❌ Server error.")
  }
}


function extractActionFromResponse(text) {
  try {
    // First: Try normal JSON parsing
    const jsonMatch = text.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      const parsed = JSON.parse(jsonMatch[0]);
      if (parsed.run) {
        return { type: "terminal_command", command: parsed.run };
      } else if (parsed.open_file) {
        return { type: "open_file", path: parsed.open_file };
      } else if (parsed.open_url) {
        return { type: "open_url", url: parsed.open_url };
      }
    }
  } catch (err) {
    console.warn("⚠️ JSON parse failed:", err.message);
  }

  // Second: Try smart text parsing like old Python
  const bashMatch = text.match(/```bash\s+([\s\S]*?)\s+```/i);
  if (bashMatch) {
    const command = bashMatch[1].trim();
    if (command) {
      return { type: "terminal_command", command };
    }
  }

  const lineMatch = text.match(/^(open|run|start|cd|ls|echo|python|java)[^\n]*$/m);
  if (lineMatch) {
    const command = lineMatch[0].trim();
    if (command) {
      return { type: "terminal_command", command };
    }
  }

  return null; // No special action detected
}


