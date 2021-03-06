import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

#------------ アフェリエイトURL用のタグ
AFF_TAG = os.environ.get('AFF_TAG')

#------------ twitter周り
API_KEY = os.environ.get('API_KEY')
API_SECRET_KEY = os.environ.get('API_SECRET_KEY')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_SECRET_TOKEN = os.environ.get('ACCESS_SECRET_TOKEN')
