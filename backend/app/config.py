"""
Configuration module for the Short Report Rebuttal Assistant
Loads environment variables and sets up paths
"""
import os
from pathlib import Path

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, use environment variables directly
    pass

# Base directory - backend is in rag_demo/backend, so go up one level to rag_demo root
# In Railway, Root Directory is set to 'backend', so the working directory is 'backend'
# We need to detect this and adjust BASE_DIR accordingly

# Start with the directory containing this config file
_config_dir = Path(__file__).parent.parent  # backend/app -> backend
BASE_DIR = _config_dir  # This is 'backend' directory

# Check if we're in Railway with Root Directory = 'backend'
# In this case, company directory should be at backend/company (we copied it there)
# So BASE_DIR should stay as 'backend' directory
if (BASE_DIR / 'company').exists():
    # Company is in backend/company, so BASE_DIR = backend (current)
    pass
elif (BASE_DIR.parent / 'company').exists():
    # Company is in parent directory, so BASE_DIR = parent (project root)
    BASE_DIR = BASE_DIR.parent
else:
    # Try to find company directory
    # Check if we're in a 'backend' subdirectory
    if BASE_DIR.name == 'backend':
        # Try parent directory
        if (BASE_DIR.parent / 'company').exists():
            BASE_DIR = BASE_DIR.parent
        # Try relative path from current working directory
        elif Path('../company').exists():
            BASE_DIR = Path('../').resolve()
        # Try absolute path from config file location
        elif (Path(__file__).parent.parent.parent.parent / 'company').exists():
            BASE_DIR = Path(__file__).parent.parent.parent.parent

# LLM Provider configuration: "openai" or "ollama"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Provider-specific defaults
if LLM_PROVIDER == "openai":
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
    EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-large")
    EMBED_DIMENSION = 3072  # text-embedding-3-large dimension
else:
    # Ollama configuration
    LLM_MODEL = os.getenv("LLM_MODEL", "llama3.1:8b")
    EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")
    EMBED_DIMENSION = 768  # nomic-embed-text dimension

# Ollama configuration (used when LLM_PROVIDER=ollama)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Initialize OpenAI client if provider is openai
openai_client = None
if LLM_PROVIDER == "openai":
    if not OPENAI_API_KEY:
        import warnings
        warnings.warn("LLM_PROVIDER is 'openai' but OPENAI_API_KEY is not set. Please set OPENAI_API_KEY environment variable.")
    else:
        try:
            from openai import OpenAI
            openai_client = OpenAI(api_key=OPENAI_API_KEY)
        except ImportError:
            import warnings
            warnings.warn("OpenAI package not installed. Please run: pip install openai")

# Storage paths - relative to rag_demo root (one level up from backend)
# Handle both relative and absolute paths from environment variables
def _resolve_path(env_var: str, default_path: Path) -> Path:
    """Resolve path from environment variable or use default, ensuring absolute path"""
    env_path = os.getenv(env_var)
    if env_path:
        path = Path(env_path)
        # If relative path, resolve relative to BASE_DIR (rag_demo root)
        if not path.is_absolute():
            path = BASE_DIR / path
        return path.resolve()
    return default_path.resolve()

CHROMA_DIR = _resolve_path("CHROMA_DIR", BASE_DIR / "storage" / "chroma")
INTERNAL_DATA_DIR = _resolve_path("INTERNAL_DATA_DIR", BASE_DIR / "company" / "EDU")
REPORTS_DIR = _resolve_path("REPORTS_DIR", BASE_DIR / "storage" / "reports")

# Ensure directories exist
CHROMA_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
INTERNAL_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Processing configuration
MAX_PAGES = 3  # Only process first 3 pages
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50
DEFAULT_TOP_K = 6
MAX_CLAIMS = 30
MIN_CLAIMS = 8

# LLM configuration
TEMPERATURE = 0.3  # Lower temperature for more deterministic output

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


# Embedding dimension tracking
def get_expected_embedding_dimension() -> int:
    """Get the expected embedding dimension for the current LLM provider"""
    if LLM_PROVIDER == "openai":
        if "3-large" in EMBED_MODEL:
            return 3072
        elif "3-small" in EMBED_MODEL:
            return 1536
        else:
            return 3072  # Default for OpenAI
    else:
        # Ollama models
        if "nomic" in EMBED_MODEL:
            return 768
        elif "bge" in EMBED_MODEL.lower():
            return 1024
        else:
            return 768  # Default for Ollama


def is_embedding_dimension_mismatch(stored_dimension: int) -> bool:
    """Check if stored embedding dimension matches current configuration"""
    return stored_dimension != EMBED_DIMENSION


def get_dimension_change_info(old_dim: int, new_dim: int) -> str:
    """Generate a user-friendly message about dimension change"""
    return f"Embedding dimension changed from {old_dim} to {new_dim} (likely due to LLM_PROVIDER or EMBED_MODEL change)"
