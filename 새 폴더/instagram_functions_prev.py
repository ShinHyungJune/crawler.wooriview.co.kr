import os, threading, json, re, time, datetime, pathlib
from pprint import pprint

import openpyxl, bs4, requests

USER_URL = "https://api.wooriview.co.kr/api/craw/users"
APPLICATION_URL = "https://api.wooriview.co.kr/api/craw/applications"


def extract_interactions(isoup):
    print(isoup.prettify())
    script = isoup.select_one("script:-soup-contains('userInteractionCount')")
    data = json.loads(script.text)
    interactions = data['interactionStatistic']

    return interactions


def get_profile(profile_url):
    res = requests.get(profile_url)
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    interactions = extract_interactions(soup)
    print(interactions)
    posts = None
    followers = None
    for i in interactions:
        itype = i['interactionType']
        if 'FilmAction' in itype:
            posts = i['userInteractionCount']
        elif 'FollowAction' in itype:
            followers = i['userInteractionCount']

    result = {
        'posts': posts,
        'followers': followers,
    }

    return result


def get_post_info(post_url):
    res = requests.get(post_url)
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    interactions = extract_interactions(soup)
    print(interactions)
    comments = None
    likes = None

    for i in interactions:
        itype = i['interactionType']
        if 'CommentAction' in itype:
            comments = i['userInteractionCount']
        elif 'LikeAction' in itype:
            likes = i['userInteractionCount']

    result = {
        'comments': comments,
        'likes': likes,
    }

    return result


def get_wooriview_users():
    res = requests.get(USER_URL)
    result = res.json()['data']
    return result


def get_wooriview_applications():
    res = requests.get(APPLICATION_URL)
    result = res.json()['data']
    return result


def post_wooriview_user(uid, count):
    res = requests.post(USER_URL, data={
        'id': uid,
        'count_follower': count,
    })

    result = res.json()

    return result


def post_wooriview_application(aid, likes, comments):
    res = requests.post(APPLICATION_URL, data={
        'id': aid,
        'count_like': likes,
        'count_comment': comments,
    })

    result = res.json()

    return result

get_post_info("https://www.instagram.com/p/CrpPl0bIRi9")