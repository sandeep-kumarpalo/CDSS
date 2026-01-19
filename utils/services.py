# utils/services.py
import json
from loguru import logger
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

# Load .env (with explicit path if needed; adjust if .env is elsewhere)
load_dotenv()  # Or load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env')) if in subdir

# Log env vars for debugging
logger.info(f"OPENAI_API_KEY loaded: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")
logger.info(f"AZURE_OPENAI_ENDPOINT: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
logger.info(f"DEPLOYMENT: {os.getenv('DEPLOYMENT')}")
logger.info(f"OPENAI_API_VERSION: {os.getenv('OPENAI_API_VERSION')}")

# Initialize LLM client (commented for demo; uncomment when env loads)
# client = AzureOpenAI(
#     api_key=os.getenv("OPENAI_API_KEY"),
#     azure_endpoint=os.getenv("LLM_ENDPOINT"),
#     api_version=os.getenv("OPENAI_API_VERSION")
# )

def load_insights():
    """Load AI-derived insights from centralized JSON."""
    try:
        with open("data/ai_insights.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading insights: {e}")
        return {}

# General service to fetch insights (simulates agent derivation via JSON for demo)
def get_insight(section, key):
    insights = load_insights()
    return insights.get(section, {}).get(key, "Insight derivation in progress...")

# Placeholder for agent-based derivation (integrate CrewAI/Azure for production)
def derive_insight_via_agents(query):
    # In production: Orchestrate CrewAI agents here.
    # For demo: Simulate with hardcoded response (or uncomment LLM call once env fixed)
    # try:
    #     response = client.chat.completions.create(
    #         model=os.getenv("DEPLOYMENT"),
    #         messages=[{"role": "user", "content": query}]
    #     )
    #     return response.choices[0].message.content
    # except Exception as e:
    #     logger.error(f"Error in agent derivation: {e}")
    #     return "Unable to derive insight at this time."
    return f"Simulated AI response for query: '{query}' (enable LLM for real derivation)."

# Admin-specific insight fetch
def get_admin_insight(key):
    return get_insight("admin_data", key)

# Doctor-specific insight fetch
def get_doctor_insight(patient_id, key):
    insights = load_insights()
    return insights.get("doctor", {}).get("hero_patients", {}).get(patient_id, {}).get(key, "Patient insight not available")