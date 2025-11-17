"""
Configuration file - Centralized application settings
"""

# API Configuration
API_URL_OPTIONS = [
    "http://localhost:8080/invocations",
    "http://localhost:5000/api/chat",
    "http://127.0.0.1:8080/invocations",
]
REQUEST_TIMEOUT = 30  # seconds

# Model Configuration
MODEL_OPTIONS = [
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash-lite",
]

# Page Configuration
PAGE_TITLE = "AI Chat Assistant"
PAGE_ICON = "✨"
LAYOUT = "wide"

# Message Configuration
USER_INPUT_PLACEHOLDER = "Type your message here..."
THINKING_MESSAGE = "Thinking..."

# Avatar Configuration
USER_AVATAR = "👤"
ASSISTANT_AVATAR = "💡"
