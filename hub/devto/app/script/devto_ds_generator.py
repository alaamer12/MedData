import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use environment variable for token
TOKEN = os.getenv("HUGGINGFACE_TOKEN")
MY_DATASET_NAME = "Alaamer/devto_articles"
PARQUET_PATH = "devto_articles.parquet"
OUT_DIR = "devto_data"

from huggingface_hub import login, whoami
login(token=TOKEN, add_to_git_credential=True)
