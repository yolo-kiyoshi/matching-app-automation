import time

from scraping import parser
from scraping.login import login
from scraping.util import get_random_wait_time

if __name__ == "__main__":

    # ログイン
    driver = login()
    driver.get("https://pairs.lv/visitor")
    time.sleep(2)
    user_ids_like = parser.get_user_ids_like(driver.page_source)
    print(user_ids_like)
    get_random_wait_time()

    for user in user_ids_like:
        # 足跡一覧からlike押下
        t = driver.find_element_by_id(user)
        t.find_element_by_css_selector("div.css-1gstcy3 > div > div.css-jdiqmq > button").click()
        get_random_wait_time()
        # pop upよりlike押下
        t = driver.find_element_by_id("dialog-root")
        t.find_element_by_css_selector("button.css-ipjbrn").click()
        get_random_wait_time()

    driver.quit()
