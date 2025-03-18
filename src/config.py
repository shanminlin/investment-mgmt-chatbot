import os
from dotenv import load_dotenv

# Load environment variables from .env file (local development)
load_dotenv()

# API keys - these will be set in Streamlit Cloud secrets
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LLM Model Configuration
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4000"))

# Application Configuration
APP_TITLE = "Investment Management Assistant"
APP_SUBTITLE = "Ask questions about investment policies, portfolio construction, and risk management"

# Example Questions
EXAMPLE_QUESTIONS = [
    "What are the key components of an investment policy statement?",
    "How should I diversify a portfolio during market volatility?",
    "What risk management strategies work best for institutional investors?",
    "How do asset allocation models adjust for different risk tolerances?",
    "What factors should I consider when constructing a fixed income portfolio?"
]

# System Message for the chatbot
SYSTEM_MESSAGE = """
You are an Investment Management Assistant, an AI specialized in providing information about investment policies,
portfolio construction, and risk management. Your answers should be:

1. Informative and accurate based on the investment knowledge
2. Well-structured and easy to understand
3. Include appropriate citations to sources when available
4. Professional but conversational in tone
5. Focused on providing objective information rather than specific financial advice

When you don't know the answer, acknowledge it clearly rather than providing misleading information.
"""

# Framework Configuration
RAG_FRAMEWORK = os.getenv("RAG_FRAMEWORK", "langchain")  # Options: langchain, llamaindex
CONVERSATION_FRAMEWORK = os.getenv("CONVERSATION_FRAMEWORK", "haystack")  # Options: haystack, rasa

# Vector Store Configuration
VECTORSTORE_PROVIDER = os.getenv("VECTORSTORE_PROVIDER", "pinecone")  # Options: pinecone, weaviate, qdrant, milvus

# Pinecone Configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "investment-mgmt")

# Weaviate Configuration
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

# Qdrant Configuration
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "investment-mgmt")

# Milvus Configuration
MILVUS_URI = os.getenv("MILVUS_URI")
MILVUS_COLLECTION = os.getenv("MILVUS_COLLECTION", "investment-mgmt")

# PostgreSQL Configuration for Keyword Search
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "investment_mgmt")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Default parameters that can be customized in experiments
# Chunking parameters
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
CHUNKING_STRATEGY = os.getenv("CHUNKING_STRATEGY", "fixed_size")

# Embedding parameters
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", "1536"))

# Retrieval parameters
RETRIEVAL_TOP_K = int(os.getenv("RETRIEVAL_TOP_K", "5"))
RETRIEVAL_SCORE_THRESHOLD = float(os.getenv("RETRIEVAL_SCORE_THRESHOLD", "0.7"))
RETRIEVAL_TYPE = os.getenv("RETRIEVAL_TYPE", "hybrid")  # Options: semantic, keyword, hybrid

# Function to load experiment configs from JSON files
def load_experiment_config(config_file):
    """
    Load experiment configuration from a JSON file.
    Used in experimental notebooks, not in production code.

    Args:
        config_file (str): Path to the JSON configuration file

    Returns:
        dict: Configuration parameters
    """
    import json
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config file: {e}")
        return {}
