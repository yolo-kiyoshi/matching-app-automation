import datetime
import time

from dateutil import tz

from scraping import parser
from scraping.util import get_random_wait_time

JST = tz.gettz("Asia/Tokyo")


def footprint(driver):

    now_str = datetime.datetime.now(JST).strftime("%Y%m%d%H%M%S")

    # 検索画面
    driver.get("https://pairs.lv/search")
    time.sleep(2)

    # lazy loadされてる部分を読み込むために、スクロールダウンしていく
    lastHeight = driver.execute_script("return document.body.scrollHeight")  # スクロールされてるか判断する部分
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # スクロールダウン
        time.sleep(3)  # 読み込まれるのを待つ
        # スクロールされてるか判断する部分
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            break
        lastHeight = newHeight

    with open("./data/src.html", "w", encoding="utf-8") as f1:
        f1.write(driver.page_source)
    user_ids = parser.get_user_ids(driver.page_source)

    user_ids_successed = list()
    user_ids_failed = list()
    for user_id in user_ids:
        try:
            time.sleep(get_random_wait_time())
            driver.get(f"https://pairs.lv/user/profile/search/grid/0/{user_id}")
            user_ids_successed.append(user_id)
            print(f"search {user_id} was successed.")
        except Exception:
            user_ids_failed.append(user_id)
            print(f"try to search {user_id}, but error occured.")

    with open(f"./data/user_ids_successed_{now_str}.txt", mode="w") as f:
        f.write("\n".join(user_ids_successed))
    with open(f"./data/user_ids_failed_{now_str}.txt", mode="w") as f:
        f.write("\n".join(user_ids_failed))

    return driver
