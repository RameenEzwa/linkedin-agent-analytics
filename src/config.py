import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")
LINKEDIN_API_URL = os.getenv("LINKEDIN_API_URL", "")
LINKEDIN_API_TOKEN = os.getenv("LINKEDIN_API_TOKEN", "")