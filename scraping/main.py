from scraping.footprint import footprint
from scraping.login import login

if __name__ == "__main__":
    # ログイン
    driver = login()
    # 足跡つける
    driver = footprint(driver)

    driver.quit()
