import instagram_functions as itf


def test_get_profile():
    url = "https://www.instagram.com/hoducci/"
    profile = itf.get_profile(url)
    print(profile)


def test_get_post_info():
    url = ""
    item = {
        'platform': 'INSTAGRAM',
        'post_url': 'https://www.instagram.com/p/Coi-ZJAvaVm/',
        # 'post_url': 'https://www.instagram.com/p/CrkpTDtJeLH/',
    }
    post = itf.get_post_info(item)
    print(post)


def test_get_naver_post():
    url = "https://blog.naver.com/popote2014/223084374518"
    url = "https://blog.naver.com/starprincessko/223071280217"

    naver = itf.get_naver_post(url)

    print(naver)
