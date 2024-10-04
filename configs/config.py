import os 
from dotenv import load_dotenv

load_dotenv()

gitlab_url = os.getenv('GITLAB_URL')
gitlab_bot_uname = os.getenv('GITLAB_BOT_UNAME')
gitlab_pat = os.getenv('GITLAB_PAT')

# OPENAI
openai_api_key = os.getenv('OPENAI_API_KEY')

# LOCAL
default_tmp_dir = os.getenv('DEFAULT_TMP_DIR')