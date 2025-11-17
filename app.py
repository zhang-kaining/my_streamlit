"""
AI Chat Assistant - Streamlit Frontend Application

A clean and simple chat interface for interacting with backend model services.
"""
import requests
import logging
from typing import Dict, List
import streamlit as st
import config

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s >>> %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# Helper Functions
# ============================================================================

def initialize_session_state() -> None:
    """Initialize session state for storing chat history and token usage."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "total_tokens" not in st.session_state:
        st.session_state.total_tokens = 0
    if "total_prompt_tokens" not in st.session_state:
        st.session_state.total_prompt_tokens = 0
    if "total_completion_tokens" not in st.session_state:
        st.session_state.total_completion_tokens = 0


def clear_chat_history() -> None:
    """Clear chat history and token statistics."""
    st.session_state.messages = []
    st.session_state.total_tokens = 0
    st.session_state.total_prompt_tokens = 0
    st.session_state.total_completion_tokens = 0
    st.rerun()


def call_backend_api(api_url: str, messages: List[Dict[str, str]], model: str) -> Dict:
    """
    Call backend API to get model response with conversation history.

    Args:
        api_url: Backend API URL
        messages: List of conversation messages with role and content
        model: Model name to use

    Returns:
        Dict with response text and usage information
    """
    try:
        payload = {"model": model, "messages": messages}
        
        response = requests.post(api_url, json=payload, timeout=config.REQUEST_TIMEOUT)
        response.raise_for_status()
        
        response_data = response.json()
        logger.info(f"Received response: {response_data.get('response', '')[:100]}...")
        
        return {
            "text": response_data["response"],
            "usage": response_data.get("usage", {})
        }
        
    except Exception as e:
        logger.error(f"API error: {str(e)}", exc_info=True)
        return {"text": f"❌ Error: {str(e)}", "usage": {}}


def render_sidebar() -> tuple[str, str]:
    """
    Render sidebar configuration panel.

    Returns:
        Tuple of (api_url, model)
    """
    with st.sidebar:
        st.header("⚙️ Configuration")

        api_url = st.selectbox(
            "Backend API URL",
            options=config.API_URL_OPTIONS,
            index=0,
            help="Select your model service API URL"
        )

        model = st.selectbox(
            "Model",
            options=config.MODEL_OPTIONS,
            index=0,
            help="Select the AI model to use"
        )

        if st.button("🗑️ Clear Chat", use_container_width=True):
            clear_chat_history()

        st.divider()

        # Display token statistics
        st.subheader("📊 Total Token Usage")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Prompt", st.session_state.get("total_prompt_tokens", 0))
            st.metric("Completion", st.session_state.get("total_completion_tokens", 0))
        with col2:
            st.metric("Total", st.session_state.get("total_tokens", 0))

        st.divider()
        st.caption("💡 Tip: Just send a message after changing settings")

    return api_url, model


def render_chat_history() -> None:
    """Render chat history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # Display token usage for assistant messages
            if message["role"] == "assistant" and message.get("usage"):
                usage = message["usage"]
                st.caption(
                    f"💰 Token: {usage.get('prompt_tokens', 0)} prompt + "
                    f"{usage.get('completion_tokens', 0)} completion = "
                    f"{usage.get('total_tokens', 0)} total"
                )


def handle_user_input(api_url: str, user_input: str, model: str) -> None:
    """
    Handle user input and get model response.

    Args:
        api_url: Backend API URL
        user_input: User input message
        model: Model name to use
    """
    logger.info(f"User input: {user_input}")

    # Save and display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Get and display assistant response
    with st.chat_message("assistant"):
        with st.spinner(config.THINKING_MESSAGE):
            logger.info(f"Sending {len(st.session_state.messages)} messages to backend")
            result = call_backend_api(api_url, st.session_state.messages, model)

        assistant_reply = result["text"]
        usage = result["usage"]

        st.markdown(assistant_reply)

        # Update session totals
        st.session_state.total_prompt_tokens += usage.get("prompt_tokens", 0)
        st.session_state.total_completion_tokens += usage.get("completion_tokens", 0)
        st.session_state.total_tokens += usage.get("total_tokens", 0)

    # Save assistant message with usage info
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_reply,
            "usage": usage
        }
    )
    logger.info(f"Total messages in history: {len(st.session_state.messages)}")
    
    # Rerun to update sidebar with new token counts
    st.rerun()


# ============================================================================
# Main Application
# ============================================================================

def main() -> None:
    """Main application entry point."""
    # Page configuration
    st.set_page_config(
        layout=config.LAYOUT,
        page_title=config.PAGE_TITLE,
        page_icon=config.PAGE_ICON
    )

    # Initialize
    initialize_session_state()

    # Page title
    st.title(f"{config.PAGE_ICON} {config.PAGE_TITLE}")

    # Sidebar
    api_url, model = render_sidebar()

    # Display chat history
    render_chat_history()

    # Handle user input
    if user_input := st.chat_input(config.USER_INPUT_PLACEHOLDER):
        handle_user_input(api_url, user_input, model)


if __name__ == "__main__":
    main()
