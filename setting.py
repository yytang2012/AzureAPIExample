# settings.py
from dotenv import load_dotenv
import os

# load all environment variables from .env
load_dotenv()

ADDRESS = os.getenv("ADDRESS")
USER = os.getenv("EVENT_HUB_USER")
KEY = os.getenv("KEY")



print(ADDRESS, USER, KEY)

