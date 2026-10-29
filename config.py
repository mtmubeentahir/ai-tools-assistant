import os
from dotenv import load_dotenv

load_dotenv()

API_KEY: str | None = os.getenv("GEMINAI_API_KEY")
BASE_URL: str = os.getenv("BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
MODEL: str = os.getenv("MODEL", "gemini-3.5-flash-lite")

if not API_KEY:
    raise SystemExit("Error: GEMINAI_API_KEY is missing. Add it to your .env file.")