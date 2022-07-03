import datetime
import logging.config
import os
import time

from dateutil import tz
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from scraping import parser, util
from scraping.util import get_random_wait_time

JST = tz.gettz("Asia/Tokyo")

# ロガー設定
logging.config.fileConfig(os.path.join(os.path.dirname(__file__), "..", "config/logging.ini"))
logging.getLogger("__name__")


def scroll_to_end(driver):
    """
    lazy loadに対応するためにページをスクロールする
    """
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


def footprint(driver):

    now_str = datetime.datetime.now(JST).strftime("%Y%m%d%H%M%S")
    
    try:
        driver.find_element_by_css_selector("#onetrust-accept-btn-handler").click()
        time.sleep(3)
    except Exception as e:
        print("confirming cookie is disable.")
    
    # 検索画面
    # 初回はpick upにレンダリングされる可能性があるため、2回実施
    for i in range(2):
        driver.get("https://pairs.lv/search")
        WebDriverWait(driver=driver, timeout=30).until(EC.presence_of_all_elements_located)

    # lazy load対応
    scroll_to_end(driver)

    # 検索画面上のuser_idを取得
    user_ids = parser.get_user_ids(driver.page_source)
    logging.info(f"there are {len(user_ids)} users on the search page.")
    # 既に足跡を付けたユーザー
    footprinted_users = util.get_footprinted_users()
    logging.info(f"there are {len(footprinted_users)} users who have already been footprinted.")
    # まだ足跡をつけていないユーザー
    user_ids = list(set(user_ids) - set(footprinted_users))
    logging.info(f"there are {len(user_ids)} users who haven't been footprinted yet.")

    # 対象ユーザーが存在しない場合
    if len(user_ids) < 1:
        logging.info("there are no footprint target users.")
        return driver

    user_ids_successed = list()
    user_ids_failed = list()
    for user_id in user_ids:
        try:
            get_random_wait_time()
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
