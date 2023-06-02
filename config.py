from dotenv import load_dotenv
import os

# Env file should be in the same folder as config.py if you want to run scripts separately
# If you want to run the run.py script, check the path to sunrise folder in it.
load_dotenv('.env')


class Config:
    # Change this to your SUNRISE repo path.
    # If you haven't cloned it yet, do git clone https://github.com/commercetools/commercetools-sunrise-data.git
    SUNRISE_PATH = r"C:\Users\User_Name\commercetools-sunrise-data-master"

    PROJECT_KEY = os.getenv('CTP_PROJECT_KEY')
    CLIENT_ID = os.getenv('CTP_CLIENT_ID')
    CLIENT_SECRET = os.getenv('CTP_CLIENT_SECRET')
    AUTH_URL = os.getenv('CTP_AUTH_URL')
    API_URL = os.getenv('CTP_API_URL')
