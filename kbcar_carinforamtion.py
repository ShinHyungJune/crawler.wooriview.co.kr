# -*- coding: utf-8 -*-
import json

import bs4
import pandas as pd
import time, os
import pyexcel
import re
import db_module

import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement, By
from selenium import webdriver
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager

def crawal_get_driver_chrome(url, is_true, download_path=None):
    import time

    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    options = webdriver.ChromeOptions()

    if is_true:
        options.add_argument('headless')

    options.add_argument("--start-maximized")
    options.add_argument("disable-infobars");
    options.add_argument('--no-sandbox')
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
    })
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("disable-gpu")
    options.add_argument("--disable-extensions")
    options.page_load_strategy = 'normal'

    prefs = {"download.default_directory": download_path};
    options.add_experimental_option("prefs", prefs);

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(2*60)
    driver.get(url)

    return driver

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")


def lxhausys_content(driver, info_set):

    file_list = os.listdir(info_set['info_download_path'])
    file_list_py = [file for file in file_list if file.endswith(".xls") or file.endswith(".xlsx")]

    for key, value in enumerate(file_list_py):
        os.remove(info_set['info_download_path'] + "/" + value)

    driver.find_element(By.XPATH, '//*[@id="header02"]/div[2]/div/ul/li[2]/a').click()
    driver.find_element(By.XPATH, '//*[@id="ha0204"]/a').click()
    time.sleep(1)

    driver.find_element(By.XPATH, '//*[@id="p_from_date"]').clear()
    driver.find_element(By.XPATH, '//*[@id="p_from_date"]').send_keys(info_set['info_start_date'])
    driver.find_element(By.XPATH, '//*[@id="search"]').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="excelDown"]').click()
    time.sleep(1)
    driver.switch_to.alert.accept();
    time.sleep(1)
    driver.find_element(By.XPATH,'//*[@id="header02"]/div[1]/ul/li[3]/a').click()

    return driver

def kbcha_get_list(driver):

    detail_list = []
    url_origin = 'https://www.kbchachacha.com/public/search/main.kbc#!?_menu=buy&sort=-orderDate&page={}'
    #Page 페이지 높이면 더 많이 크롤링
    for page in range(1, 3):
        url = url_origin.format(str(page))
        print(url)

        driver.get(url)
        time.sleep(1)

        bsObj = bs4.BeautifulSoup(driver.page_source, "html.parser")
        bsObjList = bsObj.find_all("div", {"class":"area"})

        if len(bsObjList) == 0:
            break;

        for key, value in enumerate(bsObjList):

            if value.a is not None:
                info_set = {}
                info_url = "https://www.kbchachacha.com" + value.a.attrs['href']
                info_title = value.find('strong', {'class':'tit'}).get_text().replace("실차주",'').strip()
                info_title = info_title.replace("직거래", "")
                info_title = info_title.replace("\t","")

                info_title = info_title.split()
                info_brand = info_title[0]
                info_model = " ".join(info_title[1:])

                info_pay = value.find("strong", {"class": "pay"}).get_text().strip()

                value_descrition = value.find('div', {'class':'data-line tp03'})
                if value_descrition is not None:
                    info_caryear = value_descrition.find("div",{"class":"first"}).get_text().strip()
                    info_usedmileagearea = value_descrition.find("div",{"class":"data-in"}).get_text().strip()
                    info_usedmileage = info_usedmileagearea.split("\n")[0]
                    info_area = info_usedmileagearea.split("\n")[1]

                else:
                    info_caryear = ''
                    info_usedmileage = ''
                    info_area = ''

                info_set['info_url'] = info_url
                info_set['info_brand'] = info_brand
                info_set['info_model'] = info_model

                info_set['info_caryear'] = info_caryear
                info_set['info_usedmileage'] = info_usedmileage
                info_set['info_area'] = info_area
                info_set['info_pay'] = info_pay

                detail_list.append(info_set)

    return detail_list


def kb_db_insert(info_set):

    #{'info_url': 'https://www.kbchachacha.com/public/car/detail.kbc?carSeq=24115714', 'info_brand': '기아', 'info_model': '더 뉴 카니발 11인승 2.2 디젤 디럭스', 'info_caryear': '2019년 02월 (19년형)', 'info_usedmileage': '6,045km', 'info_area': '경기', 'info_pay': '1,930만원', 'info_basic_information': {'차량정보': '71마3728', '연식': '18년05월(19년형)', '주행거리': '60,066km', '연료': 'LPG', '변속기': '오토', '연비': '정보없음', '차종': '승합', '배기량': '0cc', '색상': '노랑색', '세금미납': '정보없음', '압류': '없음', '저당': '1 건', '제시번호': '20231075195'}, 'info_history': {'전손이력': '없음', '침수이력': '없음', '용도이력': '없음', '소유자변경': '1회'}, 'info_cost': {'차량가격': '24,500,000원', '이전등록비 합계': '1,229,000 원', '취·등록세 (7%)': '1,225,000 원', '공채할인': '0 원', '증지대': '1,000 원', '인지대': '3,000 원', '부대비용': '판매자별도문의'}}
    #{'info_url': 'https://www.kbchachacha.com/public/car/detail.kbc?carSeq=24174296', 'info_brand': '현대', 'info_model': '그랜저IG 렌터카 3.0 LPi 모던 기본형', 'info_caryear': '2018년 03월 (18년형)', 'info_usedmileage': '69,400km', 'info_area': '대구', 'info_pay': '1,630만원', 'info_basic_information': {'차량정보': '71마3728', '연식': '18년05월(19년형)', '주행거리': '60,066km', '연료': 'LPG', '변속기': '오토', '연비': '정보없음', '차종': '승합', '배기량': '0cc', '색상': '노랑색', '세금미납': '정보없음', '압류': '없음', '저당': '1 건', '제시번호': '20231075195'}, 'info_history': {'전손이력': '없음', '침수이력': '없음', '용도이력': '없음', '소유자변경': '1회'}, 'info_cost': {'차량가격': '24,500,000원', '이전등록비 합계': '1,229,000 원', '취·등록세 (7%)': '1,225,000 원', '공채할인': '0 원', '증지대': '1,000 원', '인지대': '3,000 원', '부대비용': '판매자별도문의'}}
    # info_set = {'info_url': 'https://www.kbchachacha.com/public/car/detail.kbc?carSeq=24115714', 'info_brand': '기아', 'info_model': '더 뉴 카니발 11인승 2.2 디젤 디럭스', 'info_caryear': '2019년 02월 (19년형)', 'info_usedmileage': '6,045km', 'info_area': '경기', 'info_pay': '1,930만원', 'info_image_url': ['https://img.kbchachacha.com/IMG/carimg/l/img02/img2412/24128643_1935465633918114.jpeg?width=320', 'https://img.kbchachacha.com/IMG/carimg/l/img02/img2412/24128643_1935465633918114.jpeg?width=320', 'https://img.kbchachacha.com/IMG/carimg/l/img02/img2412/24128643_1935465766622754.jpeg?width=320', 'https://img.kbchachacha.com/IMG/carimg/l/img02/img2412/24128643_1935465892238324.jpeg?width=320', 'https://img.kbchachacha.com/IMG/carimg/l/img02/img2412/24128643_1935466013893621.jpeg?width=320', 'https://img.kbchachacha.com/IMG/carimg/l/img02/img2412/24128643_1935466164860202.jpeg?width=320', 'https://img.kbchachacha.com/IMG/carimg/l/img02/img2412/24128643_1935466303764446.jpeg?width=320', 'https://img.kbchachacha.com/IMG/carimg/l/img02/img2412/24128643_1935466414804310.jpeg?width=320', 'https://img.kbchachacha.com/IMG/carimg/l/img02/img2412/24128643_1935466587192574.jpeg?width=320', 'https://img.kbchachacha.com/IMG/carimg/l/img02/img2412/24128643_1935466705428159.jpeg?width=320', 'https://img.kbchachacha.com/IMG/carimg/l/img02/img2412/24128643_1935466865350823.jpeg?width=320', 'https://img.kbchachacha.com/IMG/carimg/l/img02/img2412/24128643_1935467021177785.jpeg?width=320', 'https://img.kbchachacha.com/IMG/carimg/l/img02/img2412/24128643_1935467197715071.jpeg?width=320', 'https://img.kbchachacha.com/IMG/carimg/l/img02/img2412/24128643_1935467323071967.jpeg?width=320', 'https://img.kbchachacha.com/IMG/carimg/l/img02/img2412/24128643_1935467436297549.jpeg?width=320', 'https://img.kbchachacha.com/IMG/carimg/l/img02/img2412/24128643_1935467553821739.jpeg?width=320', 'https://img.kbchachacha.com/IMG/carimg/l/img02/img2412/24128643_1935467631938826.jpeg?width=320', 'https://img.kbchachacha.com/IMG/carimg/l/img02/img2412/24128643_1935467749595423.jpeg?width=320', 'https://img.kbchachacha.com/IMG/carimg/l/img02/img2412/24128643_1935467811825916.jpeg?width=320', 'https://img.kbchachacha.com/IMG/carimg/l/img02/img2412/24128643_1935467907067141.jpeg?width=320', 'https://img.kbchachacha.com/IMG/carimg/l/img02/img2412/24128643_1935468065338593.jpeg?width=320'], 'info_basic_information': {'차량정보': '71마3728', '연식': '18년05월(19년형)', '주행거리': '60,066km', '연료': 'LPG', '변속기': '오토', '연비': '정보없음', '차종': '승합', '배기량': '0cc', '색상': '노랑색', '세금미납': '정보없음', '압류': '없음', '저당': '1 건', '제시번호': '20231075195'}, 'info_history': {'전손이력': '없음', '침수이력': '없음', '용도이력': '없음', '소유자변경': '1회'}, 'info_cost': {'차량가격': '24,500,000원', '이전등록비 합계': '1,229,000 원', '취·등록세 (7%)': '1,225,000 원', '공채할인': '0 원', '증지대': '1,000 원', '인지대': '3,000 원', '부대비용': '판매자별도문의'}}

    try:
        url = info_set['info_url']
    except:
        url = ''

    try:
        title = info_set['info_brand'] + " " + info_set['info_model']
    except:
        title = ''

    try:
        number = info_set['info_basic_information']['차량정보']
    except:
        number = ''

    try:
        price_sell = info_set['info_pay']
    except:
        price_sell = ''

    try:
        year = info_set['info_basic_information']['연식']
    except:
        year = ''

    try:
        distance = info_set['info_basic_information']['주행거리']
    except:
        distance = ''

    try:
        transmission = info_set['info_basic_information']['변속기']
    except:
        transmission = ''

    try:
        fuel = info_set['info_basic_information']['연료']
    except:
        fuel = ''

    try:
        displacement = info_set['info_basic_information']['배기량']
    except:
        displacement = ''

    try:
        type = info_set['info_basic_information']['차종']
    except:
        type = ''

    try:
        type = info_set['info_basic_information']['차종']
    except:
        type = ''

    try:
        creator = info_set['info_brand']
    except:
        creator = ''

    try:
        model = info_set['info_model']
    except:
        model = ''

    try:
        color = info_set['info_basic_information']['색상']
    except:
        color = ''

    try:
        accident = info_set['info_history']['전손이력']
    except:
        accident = ''

    try:
        img_urls = info_set['info_image_url']

        img_urls = json.dumps(img_urls)
        print(img_urls)
    except:
        img_urls = ''

    try:
        platform = "KB"
    except:
        platform = ''

    try:
        now = datetime.now()
        created_at = now.strftime("%Y-%m-%d %H:%M:%S")
    except:
        created_at = ''


    sql_insert = "INSERT IGNORE INTO cars (url, img_urls, title, number, price_sell, year, distance, transmission, fuel, displacement, type, creator, model, color, accident, platform, created_at) VALUES "
    sql_insert = sql_insert + "('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
    sql_insert = sql_insert.format(url, img_urls, title, number, price_sell, year, distance, transmission, fuel, displacement, type, creator, model, color, accident, platform, created_at)

    db_con = db_module.db_common_connect()
    db_module.db_execution_upd_from_sql(db_con, sql_insert)
    db_con.commit()
    db_con.close()

def kbcha_get_detail_information(kbcha_product_list, driver):

    kbcha_product_list_final = []
    for key, value in enumerate(kbcha_product_list):
        info_set = value

        driver.get(info_set['info_url'])
        # print(info_set['info_url'])
        # driver.get("https://www.kbchachacha.com/public/car/detail.kbc?carSeq=24128643")

        time.sleep(1)
        bsObj = bs4.BeautifulSoup(driver.page_source, "html.parser")


        bsObj = bs4.BeautifulSoup(driver.page_source, "html.parser")
        image_set = []
        if bsObj.find("div", {"id":"bx-pager"}) is not None:
            image_box = bsObj.find("div", {"id": "bx-pager"}).find_all("div", {"class":re.compile("page")})

            for key, value_image in enumerate(image_box):
                image_url = value_image.find_all("img")

                for key_image, value_image in enumerate(image_url):
                    image_url = value_image.attrs['src']
                    image_set.append(image_url)

        info_set['info_image_url'] = image_set


        info_set['info_basic_information'] = {}
        if bsObj.find('div', {'class':'car-detail-info'}) is not None and bsObj.find('div', {'class':'car-detail-info'}).find('table', {'class':'detail-info-table'}):
            car_detail = bsObj.find('div', {'class':'car-detail-info'}).find('table', {'class':'detail-info-table'}).tbody.find_all('tr')

            for key_l, value_l in enumerate(car_detail):
                th_all = value_l.find_all('th')
                td_all = value_l.find_all('td')

                for key_th, value_th in enumerate(th_all):
                    value_th_title = value_th.get_text().strip()
                    value_td_value = td_all[key_th].get_text().strip()

                    info_set['info_basic_information'][value_th_title] = value_td_value
                    # print(value_th_title, value_td_value)

        info_set['info_history'] = {}
        if bsObj.find("div", {"class":"mg-t40"}) is not None:
            car_history = bsObj.find("div", {"class": "mg-t40"}).dl
            his_dt = car_history.find_all('dt')
            his_dd = car_history.find_all('dd')

            for key_his, value_his in enumerate(his_dt):
                his_dt_title = value_his.get_text().strip()
                his_dd_value = his_dd[key_his].get_text().strip()

                info_set['info_history'][his_dt_title] = his_dd_value


        try:
            info_set['info_cost'] = {}
            driver.find_element(By.XPATH, '//*[@id="btnTotalBuyPriceCalc"]').click()
            time.sleep(1)
            bsObj = bs4.BeautifulSoup(driver.page_source, "html.parser")
            iframes = driver.find_elements(By.TAG_NAME, 'iframe')
        except:
            print("exception {}".format(info_set['info_url']))

        for i, iframe in enumerate(iframes):
            try:
                driver.switch_to.frame(iframes[i])
                bsObj = bs4.BeautifulSoup(driver.page_source, "html.parser")

                if bsObj.find('div', {'class': 'cmm-table pc-cost mg-t30'}) is None:
                    driver.switch_to.default_content()
                    continue

                bsObjTbody = bsObj.find('div', {'class': 'cmm-table pc-cost mg-t30'}).tbody.find_all('tr')
                for key_body, value_body in enumerate(bsObjTbody):
                    value_body_td = value_body.find_all("td")

                    value_body_td_key = value_body_td[0].get_text().strip()
                    value_body_td_value = value_body_td[1].get_text().strip()

                    info_set['info_cost'][value_body_td_key] = value_body_td_value

                while True:
                    bsObj = bs4.BeautifulSoup(driver.page_source, "html.parser")
                    if bsObj.find('button', {'class':'pBtn pb-blue'}) is not None:
                        driver.find_element(By.XPATH, '//*[@id="btnClose"]').click()
                        break
                    time.sleep(1)

                driver.switch_to.default_content()
            except:
                driver.switch_to.default_content()
                print('pass by except : iframes[%d]' % i)
                pass

        print(info_set)
        kb_db_insert(info_set)
        time.sleep(1)

def start_kbchacha():
    driver = crawal_get_driver_chrome('https://www.kbchachacha.com/public/search/main.kbc#!?_menu=buy', False)
    kbcha_product_list = kbcha_get_list(driver)
    kbcha_get_detail_information(kbcha_product_list, driver)
    driver.close()

# start_kbchacha()