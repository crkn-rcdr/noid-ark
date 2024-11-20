from dotenv import load_dotenv
import os

#Load .env file
load_dotenv()

#define environment variable
DATABASE_URL = os.getenv("DB_URL")