import os
from dotenv import load_dotenv

load_dotenv()

path = os.getenv("DATABASE_URL")
print("DATABASE_URL =", path)