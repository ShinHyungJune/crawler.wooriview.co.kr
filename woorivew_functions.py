import os, threading, json, re, time, datetime, pathlib
import random
from pprint import pprint

import bs4, requests

real = 1
USER_URL = "https://api.wooriview.co.kr/api/craw/users" if real == 1 else "http://localhost/api/craw/users"
APPLICATION_URL = "https://api.wooriview.co.kr/api/craw/applications" if real == 1 else "http://localhost/api/craw/applications"

def get_wooriview_users():
    res = requests.get(USER_URL)
    result = res.json()['data']
    return result


def get_wooriview_applications():
    res = requests.get(APPLICATION_URL)
    result = res.json()['data']
    return result


def post_wooriview_user(uid, count, platform):
    if platform == 'naver':
        data = {
            'id': uid,
            'count_follower_naver': count,
        }
    else:
        data = {
            'id': uid,
            'count_follower_instagram': count,
        }


    print(data)

    res = requests.post(USER_URL, data=data)

    # print(res.json())
    # result = res.json()

    return res


def post_wooriview_application(aid, likes, comments):
    res = requests.post(APPLICATION_URL, data={
        'id': aid,
        'count_like': likes,
        'count_comment': comments,
    })

    result = res.json()

    return result