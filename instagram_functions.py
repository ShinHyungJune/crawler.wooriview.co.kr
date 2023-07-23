import os, threading, json, re, time, datetime, pathlib
from pprint import pprint

import bs4, requests

USER_URL = "https://api.wooriview.co.kr/api/craw/users"
APPLICATION_URL = "https://api.wooriview.co.kr/api/craw/applications"


def extract_interactions(isoup):
    script = isoup.select_one("script:-soup-contains('userInteractionCount')")
    if not script:
        return None
    data = json.loads(script.text)
    # pprint(data)
    if isinstance(data, dict):
        if '@type' in data and data['@type'] == 'ProfilePage':
            pprint(data)
            interactions = data['interactionStatistic']
        else:
            return None
    elif isinstance(data, list):
        for item in data:
            if '@type' in item and item['@type'] == 'ProfilePage':
                interactions = item['interactionStatistic']
                break
        else:
            return None
    else:
        return None

    return interactions


def get_profile(profile_url):
    print(profile_url)
    res = requests.get(profile_url)
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    interactions = extract_interactions(soup)

    posts = None
    followers = None
    for i in interactions:
        itype = i['interactionType']
        if 'WriteAction' in itype:
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
    if not interactions:
        p = post_url.split("/")
        s = list(filter(lambda x: x, p))[-1]
        post_url = f"https://www.instagram.com/graphql/query?query_hash=2b0673e0dc4580674a88d426fe00ea90&variables=%7B%22shortcode%22%3A%22{s}%22%7D"
        res = requests.get(post_url, headers={
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        })

        data = res.json()
        media = data['data']['shortcode_media']
        likes = media['edge_media_preview_like']['count']
        comments = media['edge_media_to_comment']['count']

    else:
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


