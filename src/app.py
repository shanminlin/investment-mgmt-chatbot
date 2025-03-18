import streamlit as st
import openai
import json
import datetime
import os
import uuid
import sys

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import config

# Setup page configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon="💼",
    layout="wide"
)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

# Add a new session state variable to track if we need to process an example question
if "process_example" not in st.session_state:
    st.session_state.process_example = False

# Function to setup OpenAI client
def get_openai_client():
    api_key = None

    # Fall back to environment variable
    if not api_key:
        api_key = config.OPENAI_API_KEY

    # Check if we have a key
    if not api_key:
        st.error("OpenAI API key not found. Please set it in .streamlit/secrets.toml or as an environment variable.")
        st.stop()

    return openai.OpenAI(api_key=api_key)

# Function to log conversation
def log_conversation(user_query, bot_response):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "conversation_id": st.session_state.conversation_id,
        "timestamp": timestamp,
        "user_query": user_query,
        "bot_response": bot_response
    }

    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    # Append to log file
    with open(f"logs/conversation_logs.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

# Function to generate response
def generate_response(messages):
    client = get_openai_client()
    try:
        response = client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=messages,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return "I'm sorry, I encountered an error processing your request. Please try again later."

# Function to format citations in response
def format_response_with_citations(response):
    # This is a simple implementation - you would enhance this based on your citation format
    import re
    citation_pattern = r'\[(.*?)\]'
    formatted_text = re.sub(citation_pattern, r'*[\1]*', response)

    return formatted_text

# Function to process user input (both typed and example questions)
def process_user_input(prompt):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare messages for API call (including system message)
    api_messages = [
        {"role": "system", "content": config.SYSTEM_MESSAGE}
    ] + st.session_state.messages

    # Generate and display response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(api_messages)
            st.markdown(format_response_with_citations(response))

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Log the conversation
    log_conversation(prompt, response)

# App layout
def create_ui():
    # App header
    st.title(config.APP_TITLE)
    st.subheader(config.APP_SUBTITLE)

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                st.markdown(format_response_with_citations(message["content"]))
            else:
                st.markdown(message["content"])

    # Process example question if flag is set
    if st.session_state.process_example:
        # Get the last user message (which should be the example question)
        last_user_message = next((msg["content"] for msg in reversed(st.session_state.messages)
                              if msg["role"] == "user"), None)

        if last_user_message:
            # Prepare messages for API call (including system message)
            api_messages = [
                {"role": "system", "content": config.SYSTEM_MESSAGE}
            ] + st.session_state.messages[:-1]  # Exclude the last user message as we'll add it separately

            # Generate and display response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_response(api_messages + [{"role": "user", "content": last_user_message}])
                    st.markdown(format_response_with_citations(response))

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Log the conversation
            log_conversation(last_user_message, response)

        # Reset the flag
        st.session_state.process_example = False
        st.rerun()

    # Chat input
    if prompt := st.chat_input("Ask me about investment management..."):
        process_user_input(prompt)

# Add a sidebar with information and example questions
def create_sidebar():
    with st.sidebar:
        st.markdown("## About")
        st.markdown("""
        This Investment Management Assistant helps answer questions about
        investment policies, portfolio construction, and risk management.

        **Features:**
        - Real-time investment insights
        - Citations to information sources
        - Conversation logging for compliance
        """)

        # Example questions section
        st.markdown("## Example Questions")
        for question in config.EXAMPLE_QUESTIONS:
            if st.button(question, key=f"btn_{question[:20]}"):
                # Add the example question to messages
                st.session_state.messages.append({"role": "user", "content": question})
                # Set the flag to process this example on next rerun
                st.session_state.process_example = True
                st.rerun()

        # Add a clear button to reset the conversation
        st.markdown("## Options")
        if st.button("Clear Conversation"):
            st.session_state.messages = []
            st.rerun()

# Run the app
if __name__ == "__main__":
    create_sidebar()
    create_ui()
