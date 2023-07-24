import schedule
import time
from datetime import datetime
import instagram_functions
import naver_functions
import woorivew_functions


def schedule_start():
    print("────────────────────────────")
    print("Server Working Start────────")

    get_users()
    get_applications()



    # kbcar_carinforamtion.start_kbchacha()


def get_users():
    users = woorivew_functions.get_wooriview_users()

    for user in users:
        try:
            followers = None
            if user['instagram']:
                followers = instagram_functions.get_profile(user['instagram'])["followers"]
                woorivew_functions.post_wooriview_user(user['id'], followers, "instagram")
        except:
            print("예외발생")
            # fe = traceback.format_exc()
            # print(fe)

        # if user['naver']:
            # print(naver_functions.get_html(user['naver'])['neighbor'], "naver")
            # followers = naver_functions.get_html(user['naver'])["neighbor"]
            # woorivew_functions.post_wooriview_user(user['id'], followers, "naver")

        # if followers:
            # woorivew_functions.post_wooriview_user(user['id'], followers)

def get_applications():
    applications = woorivew_functions.get_wooriview_applications()

    for application in applications:
        try:

            if application["platform"] == 'NAVER':
                result = naver_functions.get_html(application['url_review'])
                # print(result['counter'])
                # woorivew_functions.post_wooriview_application(application['id'])

            if application["platform"] == 'INSTAGRAM':
                result = instagram_functions.get_post_info(application['url_review'])
                # print(result['counter'])
                woorivew_functions.post_wooriview_application(application['id'], result['comments'], result['likes'])
        except:
            print("error on get post")
            print(application)


schedule_start()
schedule.every(1).minutes.do(schedule_start)

while True:
    schedule.run_pending()

    now = datetime.now()
    current_time = now.strftime('%Y-%m-%d %H:%M:%S')
    print("--server active : {}".format(current_time))
    time.sleep(1)