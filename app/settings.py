import os

from dotenv import load_dotenv


ROOT_DIR = os.path.dirname(os.path.abspath('.env'))
DOTENV_FILE = os.path.join(ROOT_DIR, '.env')

load_dotenv(DOTENV_FILE)

API_KEY = os.getenv('API_KEY')
