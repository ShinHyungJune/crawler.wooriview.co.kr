import os, threading, json, re, time, datetime, pathlib
import random
from pprint import pprint

import bs4, requests

ses = requests.Session()

NAVER_BLOG_URL = "https://blog.naver.com"


def get_html(post_url):
    res = ses.get(post_url)

    soup = bs4.BeautifulSoup(res.text, "html.parser")

    frame = soup.select_one("iframe#mainFrame")

    if frame:
        path = frame.attrs['src']
        frame_url = f"{NAVER_BLOG_URL}{path}"
        res = ses.get(frame_url)
        soup = bs4.BeautifulSoup(res.text, "html.parser")

        container = soup.select_one("div.se-main-container")

        description = container.text.split("\n")
        description = list(filter(lambda x: x != '', description))
        description = list(filter(lambda x: x != ' ', description))
        description = "\n".join(description)

        count_comment_tg = soup.select_one("em#floating_bottom_commentCount")
        count_comment = count_comment_tg.text.strip()
        count_comment = 0 if count_comment == '' else count_comment
        count_like = 0
    else:
        description = ""
        count_comment = 0
        count_like = 0

    # print(soup.prettify())

    reaction = get_reaction(soup)
    counter = get_counter(soup)
    neighbor = get_neighbor(soup)

    result = {
        'reaction': reaction,
        'counter': counter,
        'neighbor': neighbor,
        'description': description,
        'like': count_like,
        'comment': count_comment,
    }

    return result


def get_blog_id(isoup: bs4.BeautifulSoup):
    blog_id_tag = isoup.select_one("input[name='blogId']")
    if blog_id_tag:
        blog_id = blog_id_tag.attrs['value']
    else:
        blog_id_tag = isoup.select_one("div#_floating_menu_property")
        if blog_id_tag:
            blog_id = blog_id_tag.attrs['blogid']
        else:
            raise Exception

    return blog_id


def get_neighbor(isoup: bs4.BeautifulSoup):
    blog_id = get_blog_id(isoup)
    res = ses.get(f"https://m.blog.naver.com/api/blogs/{blog_id}",
                  headers={
                      'referer': f'https://m.blog.naver.com/PostList.naver?blogId={blog_id}'
                  })
    result = res.json()
    neighbor = result['result']['subscriberCount']
    return neighbor


def get_reaction(isoup: bs4.BeautifulSoup):
    reaction_module = isoup.select_one("div._reactionModule")
    cid = reaction_module.attrs['data-cid']

    timestamp1 = int(time.time()) + random.randrange(1, 900)
    timestamp2 = int(time.time()) + random.randrange(1, 900)
    callback = "jQuery32106482632769284706_1683009026985"
    q = f"BLOG[{cid}]"
    cssIds = "BASIC_PC,BLOG_PC"

    payload = {
        'suppress_response_codes': True,
        'callback': callback,
        'q': q,
        'isDuplication': True,
        'cssIds': cssIds,
        '_': timestamp2,
    }
    url = "https://blog.like.naver.com/v1/search/contents"
    res = ses.get(url, params=payload)

    pattern = f"{callback}\((.*)\);"
    p = re.compile(pattern)
    s = p.search(res.text)

    code = s.groups()[0]
    data = json.loads(code)

    reactions = data['contents'][0]['reactions']
    result = None
    for r in reactions:
        rtype = r['reactionType']
        if rtype == 'like':
            result = r['count']

    return result


def get_posts():
    url = "https://m.blog.naver.com/PostList.naver?blogId=ghkdcjd1004&categoryNo=0&listStyle=post"
    result = []

    res = ses.get(url)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    print(soup.prettify())

    return result


def get_counter(isoup: bs4.BeautifulSoup):
    """counter = get_counter(soup)"""
    blog_id = get_blog_id(isoup)
    payload = {
        'blogId': blog_id,
        'enableWidgetKeys': 'counter',
        'writingMaterialListType': '1',
        'skinId': 0,
        'skinType': 'C',
        'calType': '',
    }
    url = "https://blog.naver.com/mylog/WidgetListAsync.naver"
    res = ses.get(url, params=payload, headers={
        'referer': f'https://blog.naver.com/PostView.naver?blogId={blog_id}&redirect=Dlog&widgetTypeCall=true&directAccess=false'
    })
    p = re.compile(r"counter : { content : '(.*?)' },")
    s = p.search(res.text)
    html = s.groups()[0]
    csoup = bs4.BeautifulSoup(html, "html.parser")
    today = csoup.select_one(".cnt1").text.strip().replace(",", "")
    total = csoup.select_one(".cnt2").text.strip().replace(",", "")

    result = {
        'today': int(today),
        'total': int(total),
    }

    return result
