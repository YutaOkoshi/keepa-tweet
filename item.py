
from distutils.util import strtobool
import main
import datetime
import re
from time import mktime
import env

class Item:

    def __init__(self, item):

        self.id = item["guid"]
        self.asin = item["guid"][0:10].strip()
        self.published = datetime.datetime.fromtimestamp(
            mktime(item["published_parsed"]))
        self.affUrl = "https://www.amazon.co.jp/dp/" + \
            self.asin+"/ref=nosim?tag=" + env.AFF_TAG

        # 文字数制限280文字なのでそれを超えないように大体100文字にtitleを丸める
        self.title = item["title"][0:100]
        # A列がASIN記入欄という前提で[0]にしている
        affList = [r[0].strip() for r in main.AFFList]

        # スプレットシートに存在すればIndex、なければNone
        self.columnNumber = affList.index(
            self.asin) if self.asin in affList else None
        if self.columnNumber != None:
            # D列が最終更新日の前提で[3]にしている
            if re.match(
                r'[0-9]{4}\.[0-9]{2}\.[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}',
                    main.AFFList[self.columnNumber][3]):
                self.lastUpdate = datetime.datetime.strptime(
                    main.AFFList[self.columnNumber][3], '%Y.%m.%d %H:%M:%S')
            else:
                self.lastUpdate = None

            # B列がツイートを行うの前提で[1]にしている
            self.isTweet = strtobool(main.AFFList[self.columnNumber][1])
        else:
            self.lastUpdate = None
            self.isTweet = False

    def shouldTweet(self) -> bool:
        if not self.isTweet:
            return False
        if self.lastUpdate == None \
                or self.lastUpdate < self.published:
            return True
        return False

    def tweet(self) -> bool:
        text = '''
<Amazon>
にてお安く販売中！
お早目にチェックしてみてね！
#Amazon #アマゾン #お買い得

■商品名：{title}
■URL：{url}
［{date}]
'''.format(title=self.title, url=self.affUrl, date=self.published).strip()

        main.TweetApi.update_status(text)
        main.AFFSheet.update_cell(
            self.columnNumber+3,  # 先頭行2行削除した分を1から始まるので+3
            # main.TweetApi.update_status(text)
            # D列が最終ツイート日時の前提で4にしている
            # update_cell()は1から始めるので3ではない
            4,
            self.published.strftime('%Y.%m.%d %H:%M:%S'))  # (行,列,更新値)
        return True
