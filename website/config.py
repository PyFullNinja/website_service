import os
from pathlib import Path

from dotenv import load_dotenv

# Явно вказуємо шлях до .env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

NAME = os.getenv("DBNAME")
DBUSER = os.getenv("DBUSER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
#
# print("DONE!")
# print(f"NAME: {NAME}")
# print(f"DBUSER: {DBUSER}")
# print(f"PASSWORD: {PASSWORD}")
# print(f"HOST: {HOST}")
# print(f"PORT: {PORT}")
