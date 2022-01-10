import re

from bs4 import BeautifulSoup


def get_user_ids(html):
    """
    検索ページのhtmlからuseridを取得する
    """
    soup = BeautifulSoup(html, "html.parser")
    users = soup.select("a.css-opde7s")
    user_ids = [re.sub("/user/profile/search/grid/[0-9]*/", "", user.attrs.get("href")) for user in users]
    return user_ids


def get_user_ids_like(html):
    """
    足跡ページからlikeを押せるユーザーを取得する
    """
    soup = BeautifulSoup(html, "html.parser")
    users_footprint = soup.select("li.css-1iaafed")
    user_ids_like = list()
    for user in users_footprint:
        user_id = user.attrs.get("id")
        botton_kind = user.select("div.css-1gstcy3 > div > div.css-jdiqmq > button")[0].attrs.get("data-test")
        if botton_kind == "like-button":
            user_ids_like.append(user_id)
    return user_ids_like
