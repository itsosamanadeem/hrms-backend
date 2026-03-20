import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
# load_env = dotenv.load_dotenv(dotenv.find_dotenv(Path(__file__).parent.parent / ".env"))
class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY")
    REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")

    if not SECRET_KEY or not REFRESH_SECRET_KEY:
        raise RuntimeError("JWT secret keys are not set")
    
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7

settings = Settings()