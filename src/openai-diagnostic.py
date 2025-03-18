import os
import streamlit as st
import openai
import traceback
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("openai-diagnostic")

def check_openai_connection():
    """Test the OpenAI API connection and return diagnostic info"""
    results = {
        "api_key_set": False,
        "api_key_valid": False,
        "connection_successful": False,
        "error_message": None,
        "models_available": []
    }

    # Check if API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        results["api_key_set"] = True
        logger.info("API key is set in environment")
    else:
        logger.error("API key not found in environment variables")
        return results

    # Initialize the client
    client = openai.OpenAI(api_key=api_key)

    # Test connection with a simple models list request
    try:
        logger.info("Testing OpenAI connection...")
        models = client.models.list()
        results["connection_successful"] = True
        results["api_key_valid"] = True

        # Get available models
        results["models_available"] = [model.id for model in models.data]
        logger.info(f"Connection successful. Found {len(results['models_available'])} models.")

    except openai.AuthenticationError:
        results["error_message"] = "Authentication Error: Invalid API key"
        logger.error("API key is invalid")
    except openai.RateLimitError:
        results["error_message"] = "Rate Limit Error: You've exceeded your rate limit"
        logger.error("Rate limit exceeded")
    except Exception as e:
        results["error_message"] = f"Unexpected error: {str(e)}"
        logger.error(f"Unexpected error: {traceback.format_exc()}")

    return results

def test_chat_completion(model="gpt-3.5-turbo"):
    """Test a basic chat completion"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"success": False, "error": "API key not set"}

    client = openai.OpenAI(api_key=api_key)
    try:
        logger.info(f"Testing chat completion with model {model}...")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say hello world"}],
            max_tokens=10
        )
        return {
            "success": True,
            "response": response.choices[0].message.content,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }
    except Exception as e:
        logger.error(f"Chat completion test failed: {traceback.format_exc()}")
        return {"success": False, "error": str(e)}

# Streamlit UI
st.title("OpenAI API Diagnostic Tool")

st.write("This tool helps diagnose issues with OpenAI API connections in your Streamlit app.")

# Check current environment
st.header("Environment Check")
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    st.success("✅ OPENAI_API_KEY is set in environment")
    # Show masked key
    masked_key = api_key[:4] + "..." + api_key[-4:]
    st.code(f"API Key: {masked_key}")
else:
    st.error("❌ OPENAI_API_KEY not found in environment")
    st.info("You can set it in this session below:")
    temp_key = st.text_input("Enter your OpenAI API key", type="password")
    if temp_key:
        os.environ["OPENAI_API_KEY"] = temp_key
        st.rerun()

# Run connection test
if st.button("Run Connection Test"):
    with st.spinner("Testing OpenAI API connection..."):
        results = check_openai_connection()

        st.header("Connection Test Results")
        if results["connection_successful"]:
            st.success("✅ Successfully connected to OpenAI API")
            st.write(f"Found {len(results['models_available'])} available models")
            st.json({"available_models": results["models_available"]})
        else:
            st.error("❌ Failed to connect to OpenAI API")
            st.error(f"Error: {results['error_message']}")

            if not results["api_key_set"]:
                st.info("💡 Tip: Make sure your API key is set in your environment variables")
            elif not results["api_key_valid"]:
                st.info("💡 Tip: Your API key appears to be invalid or expired")

# Test chat completion
st.header("Test Chat Completion")
test_model = st.selectbox(
    "Select model to test",
    ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"]
)

if st.button("Run Chat Completion Test"):
    with st.spinner("Testing chat completion..."):
        result = test_chat_completion(test_model)

        if result["success"]:
            st.success("✅ Chat completion test successful")
            st.write("Response:", result["response"])
            st.json({"usage": result["usage"]})
        else:
            st.error("❌ Chat completion test failed")
            st.error(f"Error: {result['error']}")

st.header("Common Issues")
with st.expander("Environment Variables"):
    st.markdown("""
    - **In local development**: Make sure you have a `.env` file or have set the environment variable
    - **In Streamlit Cloud**: Set the secret in the app settings
    - **Using st.secrets**: If using `st.secrets`, access with `st.secrets["OPENAI_API_KEY"]` instead of environment variables
    """)

with st.expander("API Version Issues"):
    st.markdown("""
    - **OpenAI SDK version**: Make sure you're using the latest OpenAI Python SDK (1.x+)
    - **Older code**: If you're using `openai.Completion.create()` format, update to the new client format
    - **Import statement**: Ensure you're using `from openai import OpenAI` for newer versions
    """)

with st.expander("Network Issues"):
    st.markdown("""
    - **Firewall restrictions**: Check if your network allows API calls to OpenAI endpoints
    - **Proxy settings**: You might need to configure proxy settings for API calls
    - **Timeout issues**: Consider increasing timeout limits for API calls
    """)
