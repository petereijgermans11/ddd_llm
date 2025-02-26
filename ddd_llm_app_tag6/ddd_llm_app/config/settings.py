import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")  #alternatives: gpt-3.5-turbo-instruct

# Anthropic Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-2.1")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL","https://api.deepseek.com")

# Custom Provider Configuration
CUSTOM_PROVIDER_MODEL = os.getenv("CUSTOM_PROVIDER_MODEL", "google/flan-t5-base")

# LLM Provider Choice
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # Default to OpenAI

VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "/ddd_llm_data/prorail_dom_idx")