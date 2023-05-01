import os, threading, json, re, time, datetime, pathlib
from pprint import pprint

import bs4, requests

real = 1
USER_URL = "https://api.wooriview.co.kr/api/craw/users" if real == 1 else "http://localhost/api/craw/users"
APPLICATION_URL = "https://api.wooriview.co.kr/api/craw/applications" if real == 1 else "http://localhost/api/craw/applications"


def extract_description(isoup):
    script = isoup.select_one("script:-soup-contains('userInteractionCount')")
    if not script:
        return None
    data = json.loads(script.text)
    interactions = data['articleBody']

    return interactions


def extract_interactions(isoup):
    script = isoup.select_one("script:-soup-contains('userInteractionCount')")
    if not script:
        return None
    data = json.loads(script.text)
    interactions = data['articleBody']

    return interactions


def get_profile(profile_url):
    res = requests.get(profile_url)
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    interactions = extract_interactions(soup)

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


def get_post_info(item):
    res = requests.get(item["url_review"])
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    result = None

    if item["platform"] == "INSTAGRAM":
        result = get_parse_instagram(item, soup)
        # description = extract_description(soup)

    if item["platform"] == "NAVER":
        response = get_naver_post(item['url_review'])

        if response:
            result = {
                'comments': response[0],
                'likes': response[1],
                'description': response[2]
            }

    return result


def get_parse_instagram(item, soup):
    interactions = extract_interactions(soup)
    description = extract_description(soup)

    if not interactions:
        p = item['url_review'].split("/")
        s = list(filter(lambda x: x, p))[-1]
        item['url_review'] = f"https://www.instagram.com/graphql/query?query_hash=2b0673e0dc4580674a88d426fe00ea90&variables=%7B%22shortcode%22%3A%22{s}%22%7D"
        res = requests.get(item['url_review'], headers={
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        })

        data = res.json()
        media = data['data']['shortcode_media']
        description = media['edge_media_to_caption']["edges"][0]["node"]["text"]
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
        'description': description
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


def post_wooriview_application(aid, likes, comments, description):
    res = requests.post(APPLICATION_URL, data={
        'id': aid,
        'count_like': likes,
        'count_comment': comments,
        'description': description
    })

    result = res.json()

    return result


def collect_applications():
    items = get_wooriview_applications()

    for item in items:
        result = get_post_info(item)
        if "likes" in result:
            post_wooriview_application(item["id"], result["likes"], result["comments"], result["description"])


def collect_users():
    items = get_wooriview_users()

    for item in items:
        result = get_profile(item["instagram"])
        post_wooriview_user(item["id"], result["followers"])


def get_naver_post(post_url):
    ses = requests.Session()

    res = ses.get(post_url)
    soup = bs4.BeautifulSoup(res.content, 'html.parser')

    frame = soup.select_one("iframe#mainFrame")

    if frame:
        src = frame.attrs['src']
        url = f"https://blog.naver.com{src}"

        res = ses.get(url)

        soup = bs4.BeautifulSoup(res.text, "html.parser")

        # print(soup.prettify())

        container = soup.select_one("div.se-main-container")

        description = container.text.split("\n")
        description = list(filter(lambda x: x != '', description))
        description = list(filter(lambda x: x != ' ', description))
        description = "\n".join(description)

        count_comment_tg = soup.select_one("em#floating_bottom_commentCount")
        count_comment = count_comment_tg.text.strip()
        count_comment = 0 if count_comment == '' else count_comment
        count_like = 0
        # print(comment_count)
        # like_count_tag = soup.select_one("em.u_txt._label")
        # print(like_count_tag)

        return count_comment, count_like, description

    return False


collect_applications()
collect_users()

