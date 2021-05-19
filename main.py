
import feedparser
import gspread
import os
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
import tweepy
import item

load_dotenv()

#------------ アフェリエイトURL用のタグ
AFF_TAG = os.environ['AFF_TAG']

#------------ twitter周り
API_KEY = os.environ['API_KEY']
API_SECRET_KEY = os.environ['API_SECRET_KEY']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_SECRET_TOKEN = os.environ['ACCESS_SECRET_TOKEN']

Auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
Auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET_TOKEN)
TweetApi = tweepy.API(Auth)


#------------ GSpreadSheet周り
ApiScope = ['https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive']
Credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'secure.json', ApiScope)
GspreadClient = gspread.authorize(Credentials)
MainSpreadSheet = GspreadClient.open("keepa-twitter連携管理画面")

# GSpreadSheetのリクエスト上限キビシイので先に取得
AFFSheet = MainSpreadSheet.worksheet('アフェリエイトMAP')
AFFList = AFFSheet.get_all_values()
# 先頭行は必要ないので削除
AFFList.pop(0)
AFFList.pop(0)
RssSheet = MainSpreadSheet.worksheet('Keepa-RSS一覧')
# RssList = RssSheet.get_all_values()


def main(event, context):
    rssList = getRssList()
    everyItem = getItems(rssList)
    for item in everyItem:
        if item.shouldTweet():
            item.tweet()


def getItems(rssList) -> list:
    everyItem = []
    for url in rssList:
        d = feedparser.parse(url)
        if d["status"] == 200 and d["entries"] != []:
            for i in d["entries"]:
                everyItem += [item.Item(i)]
    return everyItem


def getRssList() -> list:
    cell = RssSheet.find("RSS")
    rssList = RssSheet.col_values(cell.col)
    # 必要のない要素排除
    to_remove = ['※列の追加を行わないでください！', 'RSS']
    rssList = [i for i in rssList if i not in to_remove]
    return rssList
