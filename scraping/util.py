import os
import random
import time


def get_random_wait_time(min=2, max=5):
    """
    指定したパラメータの一様分布から生成された値をもとにsleepする
    """
    time.sleep(random.uniform(min, max))


def get_footprinted_users():
    """
    過去に足跡を付けたユーザーを取得する
    """
    file_name = "user_ids_successed"
    files = [i for i in os.listdir("./data/") if file_name in i]
    foot_printed_users = list()
    for i in files:
        with open(f"./data/{i}", "r") as f:
            foot_printed_users.extend(f.read().split("\n"))
    return list(set(foot_printed_users))
