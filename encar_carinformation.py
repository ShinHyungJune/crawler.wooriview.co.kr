# -*- coding: utf-8 -*-
import json
import requests
import shutil
import subprocess

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

def crawal_get_debugger_driver(url, is_true):
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    options = webdriver.ChromeOptions()

    if is_true:
        options.add_argument('headless')

    try:
        shutil.rmtree(r"C:\chrometemp")  # remove Cookie, Cache files
    except FileNotFoundError:
        pass

    subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')
    options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    return driver

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")


def kb_db_insert(info_set):

#{'info_title': '쌍용 G4 렉스턴  디젤 2.2 4WD 헤리티지 스페셜', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=34562820&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g1&tempht_arg=awM1Og361NO7_0', 'info_brand': '쌍용', 'info_model': '디젤 2.2 4WD 헤리티지 스페셜', 'info_caryear': '20/01식', 'info_usedmileage': '15,525km', 'info_area': '광주', 'info_pay': '2,790만원', 'info_fuel': '디젤', 'image_list': ['http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_001.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_002.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_003.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_004.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_005.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_005.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_006.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_007.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_008.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_009.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_010.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_015.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_016.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_017.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_018.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_019.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_020.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_021.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_022.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_023.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_024.jpg'], 'detail_information': {'주행거리': '15,525Km', '연식': '20년 01월', '연료': '디젤', '차종': 'SUV', '배기량': '2,157cc', '변속기': '오토', '색상': '검정색', '차량번호': '297너4382'}}
    try:
        url = info_set['info_url']
    except:
        url = ''

    try:
        title = info_set['info_title']
    except:
        title = ''

    try:
        number = info_set['detail_information']['차량번호']
    except:
        number = ''

    try:
        price_sell = info_set['info_pay']
    except:
        price_sell = ''

    try:
        year = info_set['detail_information']['연식']
    except:
        year = ''

    try:
        distance = info_set['detail_information']['주행거리']
    except:
        distance = ''

    try:
        transmission = info_set['detail_information']['변속기']
    except:
        transmission = ''

    try:
        fuel = info_set['detail_information']['연료']
    except:
        fuel = ''

    try:
        displacement = info_set['detail_information']['배기량']
    except:
        displacement = ''

    try:
        type = info_set['detail_information']['차종']
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
        color = info_set['detail_information']['색상']
    except:
        color = ''

    try:
        accident = info_set['info_history'].replace("엔카진단","")
    except:
        accident = ''

    import ast
    try:
        # temp_image = []
        # for key, value in enumerate(info_set['image_list']):
        #     temp_image.append("\'{}\'".format(value))
        #
        # img_urls = "[" + ",".join(info_set['image_list']) + "]"
        # print(img_urls)
        img_urls = str(info_set['image_list']).replace("'", '\"')
    except:
        img_urls = ''

    try:
        now = datetime.now()
        created_at = now.strftime("%Y-%m-%d %H:%M:%S")
    except:
        created_at = ''

    platform = 'ENCAR'


    # sql_insert = "INSERT INTO cars (platform, url, img_urls, title, number, price_sell, year, distance, transmission, fuel, displacement, type, creator, model, color, accident, created_at) VALUES "
    # sql_insert = sql_insert + "('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
    # sql_insert = sql_insert.format(platform, url, img_urls, title, number, price_sell, year, distance, transmission, fuel, displacement, type, creator, model, color, accident, created_at)

    print(sql_insert)

    db_con = db_module.db_common_connect()
    db_module.db_execution_upd_from_sql(db_con, sql_insert)
    db_con.commit()
    db_con.close()


# info_set = {'info_title': '쌍용 G4 렉스턴  디젤 2.2 4WD 헤리티지 스페셜', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=34562820&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g1&tempht_arg=awM1Og361NO7_0', 'info_brand': '쌍용', 'info_model': '디젤 2.2 4WD 헤리티지 스페셜', 'info_caryear': '20/01식', 'info_usedmileage': '15,525km', 'info_area': '광주', 'info_pay': '2,790만원', 'info_fuel': '디젤', 'image_list': ['http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_001.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_002.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_003.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_004.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_005.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_005.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_006.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_007.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_008.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_009.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_010.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_015.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_016.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_017.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_018.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_019.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_020.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_021.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_022.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_023.jpg', 'http://ci.encar.com/carpicture/carpicture05/pic3455/34555960_024.jpg'], 'detail_information': {'주행거리': '15,525Km', '연식': '20년 01월', '연료': '디젤', '차종': 'SUV', '배기량': '2,157cc', '변속기': '오토', '색상': '검정색', '차량번호': '297너4382'}}
# kb_db_insert(info_set)
# exit()

def encar_get_list(driver):

    detail_list = []
    url_origin = driver.current_url
    print('url_origin patter :', url_origin)
    url_origin = url_origin.replace('page%22%3A1','page%22%3A{}')

    #페이지 진행
    for page in range(1, 3):
        url = url_origin.format(str(page))
        print("current page url : ", url)
        driver.get(url)
        time.sleep(3)
        # input_wait = input("wait...")

        bsObj = bs4.BeautifulSoup(driver.page_source, "html.parser")
        try:
            bsObjList = bsObj.find("tbody", {"id":"sr_normal"}).find_all("tr")
        except:
            bsObjList = []

        for key, value in enumerate(bsObjList):
            info_set = {}
            info_url = "http://www.encar.com/" + value.find("td",{"class":"inf"}).a.attrs['href']
            info_title = value.find("td",{"class":"inf"}).a.get_text().strip()
            info_brand = value.find("td",{"class":"inf"}).find("span", {"class":"cls"}).strong.get_text().strip()
            info_model = value.find("td",{"class":"inf"}).find("span", {"class":"dtl"}).get_text().strip()
            info_pay = value.find("td",{"class":"prc_hs"}).get_text().strip().strip()

            info_caryear = value.find("td",{"class":"inf"}).find("span", {"class":"detail"}).find("span", {"class":"yer"}).get_text().strip().strip()
            info_usedmileage = value.find("td",{"class":"inf"}).find("span", {"class":"detail"}).find("span", {"class":"km"}).get_text().strip().strip()
            info_area =  value.find("td",{"class":"inf"}).find("span", {"class":"detail"}).find("span", {"class":"loc"}).get_text().strip().strip()
            info_fuel =  value.find("td",{"class":"inf"}).find("span", {"class":"detail"}).find("span", {"class":"fue"}).get_text().strip()

            info_set['info_title'] = info_title
            info_set['info_url'] = info_url
            info_set['info_brand'] = info_brand
            info_set['info_model'] = info_model

            info_set['info_caryear'] = info_caryear
            info_set['info_usedmileage'] = info_usedmileage
            info_set['info_area'] = info_area
            info_set['info_pay'] = info_pay
            info_set['info_fuel'] = info_fuel

            print(info_set)
            detail_list.append(info_set)
    return detail_list


def encar_get_detail_information(kbcha_product_list):
    driver = crawal_get_debugger_driver('https://www.naver.com/', False)
    wait_out = 'N'

    kbcha_product_list_final = []
    for key, value in enumerate(kbcha_product_list):
        # print("───────────────────────────────")
        # print(value)

        info_set = value

        if key == 0:
            driver.get(info_set['info_url'])
        else:
            driver = crawal_get_debugger_driver(info_set['info_url'], False)

        # driver.get(info_set['info_url'])
        bsObj = bs4.BeautifulSoup(driver.page_source, "html.parser")
        time.sleep(1)

        iframes = driver.find_elements(By.TAG_NAME, 'iframe')
        for i, iframe in enumerate(iframes):
            try:
                driver.switch_to.frame(iframes[i])
                bsObj = bs4.BeautifulSoup(driver.page_source, "html.parser")
                if bsObj.find("label", {"class":"rc-anchor-center-item rc-anchor-checkbox-label"}) is not None and bsObj.find("label", {"class":"rc-anchor-center-item rc-anchor-checkbox-label"}).get_text().strip() == '로봇이 아닙니다.':
                    # wait_minute = input("로봇 점검을 마쳤다면 다음을 진행하세요!")
                    print("로봇이 감지되었습니다.!")
                    time.sleep(1)
                    driver.switch_to.default_content()
                    driver.find_element(By.XPATH, '//*[@id="headerDIV"]/h1/a').click()
                    time.sleep(2)
                    driver.get(info_set['info_url'])
                    time.sleep(1)
                    break;
            except:
                driver.switch_to.default_content()
                print('pass by except : iframes[%d]' % i)
                pass

        bsObj = bs4.BeautifulSoup(driver.page_source, "html.parser")
        append_service_comment = ''
        if bsObj.find("ul", {"class":"append_service"}) is not None:
            append_serviceObj = bsObj.find("ul", {"class": "append_service"}).find_all("li")
            for key_l, value_l in enumerate(append_serviceObj):

                try:
                    if value_l.a.attrs['data-enlog-dt-eventname'] == '엔카진단':
                        append_service_comment = value_l.get_text().replace('엔카에서 책임지는', '').replace('  ', '').replace('\n', '').replace('\t', '').replace('앤카진단', '').strip()
                        break
                except:
                    continue

        info_set['info_history'] = append_service_comment

        image_list = []
        if bsObj.find("span", {"id" : re.compile("thumnail_\d+_pic_desc")}) is not None:
            bsObjFrame = bsObj.find_all("span", {"id": re.compile("thumnail_\d+_pic_desc")})
            for key, value in enumerate(bsObjFrame):
                image_src = value.a.attrs['onmouseover']
                image_src = image_src.replace("javascript:car_swapPicture('", "")
                image_src = image_src.split("'")[0]

                image_list.append(image_src)

        info_set['image_list'] = image_list

        info_set['detail_information'] = []
        info_detail = {}
        if bsObj.find("div", {"class":"prod_informain"}) is not None:
            bsObjLi = bsObj.find("div", {"class": "prod_informain"}).find_all("li")

            for key_l, value_l in enumerate(bsObjLi):
                detail_information = value_l.get_text().strip().split(":")
                name_field = detail_information[0].strip()
                value_field = detail_information[1].strip()

                info_detail[name_field] = value_field
        elif bsObj.find("ul", {"class":"list_carinfo"}) is not None:
            bsObjLi = bsObj.find("ul", {"class": "list_carinfo"}).find_all("li")
            for key_l, value_l in enumerate(bsObjLi):
                try:
                    detail_information = value_l.get_text().strip().split(":")
                    name_field = detail_information[0].strip()
                    value_field = detail_information[1].replace("  ","").replace("\n","").replace("자세히보기","").strip()
                except:
                    name_field = ''
                    value_field= ''

                if name_field == '':
                    try:
                        detail_information = value_l.get_text().strip().split(" ")
                        name_field = detail_information[0].strip()
                        value_field = detail_information[1].replace("  ","").replace("\n","").replace("자세히보기","").strip()
                    except:
                        name_field = ''
                        value_field= ''

                info_detail[name_field] = value_field

        info_set['detail_information'] = info_detail
        print(info_set)
        driver.close()
        time.sleep(4)

        try:
            shutil.rmtree(r"C:\chrometemp")  # remove Cookie, Cache files
        except FileNotFoundError:
            pass

        kb_db_insert(info_set)


def start_encar():
    driver = crawal_get_debugger_driver('https://www.instagram.com/foret_pilates/', False)

    time.sleep(5)

    getFollower();
    bsObj = bs4.BeautifulSoup(driver.page_source, "html.parser")

    counts = bsObj.find_all("span", {"class":"_ac2a"})

    print(counts[1].find("span").get_text())

    # driver.find_element(By.XPATH, '//*[@id="indexSch1"]/div[1]/a').click()
    time.sleep(1)
    # encar_product_list = encar_get_list(driver)
    driver.close()
    time.sleep(2)

    try:
        shutil.rmtree(r"C:\chrometemp")  # remove Cookie, Cache files
    except FileNotFoundError:
        pass

    # encar_product_list = [{'info_title': '쌍용 G4 렉스턴  디젤 2.2 4WD 헤리티지 스페셜', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=34562820&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g1&tempht_arg=awM1Og361NO7_0', 'info_brand': '쌍용', 'info_model': '디젤 2.2 4WD 헤리티지 스페셜', 'info_caryear': '20/01식', 'info_usedmileage': '15,525km', 'info_area': '광주', 'info_pay': '2,790만원', 'info_fuel': '디젤'}, {'info_title': '기아 스포티지 4세대  디젤 1.7 2WD 트렌디', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=34748165&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g2&tempht_arg=awM1Og361NO7_1', 'info_brand': '기아', 'info_model': '디젤 1.7 2WD 트렌디', 'info_caryear': '18/05식', 'info_usedmileage': '53,695km', 'info_area': '경기', 'info_pay': '1,390만원', 'info_fuel': '디젤'}, {'info_title': '현대 아이오닉 일렉트릭  N', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=33701361&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g3&tempht_arg=awM1Og361NO7_2', 'info_brand': '현대', 'info_model': 'N', 'info_caryear': '16/07식(17년형)', 'info_usedmileage': '44,113km', 'info_area': '광주', 'info_pay': '1,730만원', 'info_fuel': '전기'}, {'info_title': '기아 더 뉴 쏘렌토  디젤 2.2 2WD 노블레스 스페셜', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=33701369&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g4&tempht_arg=awM1Og361NO7_3', 'info_brand': '기아', 'info_model': '디젤 2.2 2WD 노블레스 스페셜', 'info_caryear': '18/02식', 'info_usedmileage': '46,746km', 'info_area': '광주', 'info_pay': '2,350만원', 'info_fuel': '디젤'}, {'info_title': '현대 아이오닉6  롱레인지 익스클루시브 플러스', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=34549289&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g5&tempht_arg=awM1Og361NO7_4', 'info_brand': '현대', 'info_model': '롱레인지 익스클루시브 플러스', 'info_caryear': '22/10식(23년형)', 'info_usedmileage': '1,067km', 'info_area': '경기', 'info_pay': '4,720만원', 'info_fuel': '전기'}, {'info_title': '현대 아이오닉6  롱레인지 익스클루시브 플러스', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=34534046&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g6&tempht_arg=awM1Og361NO7_5', 'info_brand': '현대', 'info_model': '롱레인지 익스클루시브 플러스', 'info_caryear': '22/10식(23년형)', 'info_usedmileage': '908km', 'info_area': '경기', 'info_pay': '4,770만원', 'info_fuel': '전기'}, {'info_title': '제네시스 G80 (RG3)  가솔린 2.5 터보 2WD', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=34267794&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g7&tempht_arg=awM1Og361NO7_6', 'info_brand': '제네시스', 'info_model': '가솔린 2.5 터보 2WD', 'info_caryear': '21/01식', 'info_usedmileage': '10,837km', 'info_area': '부산', 'info_pay': '5,240만원', 'info_fuel': '가솔린'}, {'info_title': '르노코리아(삼성) SM5 노바  LPLi 택시렌터카 최고급형', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=34582924&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g8&tempht_arg=awM1Og361NO7_7', 'info_brand': '르노코리아(삼성)', 'info_model': 'LPLi 택시렌터카 최고급형', 'info_caryear': '16/03식', 'info_usedmileage': '99,145km', 'info_area': '부산', 'info_pay': '730만원', 'info_fuel': 'LPG(일반인 구입)'}, {'info_title': '기아 스포티지 4세대  디젤 1.7 2WD 노블레스', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=34582918&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g9&tempht_arg=awM1Og361NO7_8', 'info_brand': '기아', 'info_model': '디젤 1.7 2WD 노블레스', 'info_caryear': '16/05식', 'info_usedmileage': '94,218km', 'info_area': '부산', 'info_pay': '1,160만원', 'info_fuel': '디젤'}, {'info_title': '기아 K5 3세대  2.0 LPI(렌터카용) 스탠다드', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=34331382&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g10&tempht_arg=awM1Og361NO7_9', 'info_brand': '기아', 'info_model': '2.0 LPI(렌터카용) 스탠다드', 'info_caryear': '20/06식', 'info_usedmileage': '37,632km', 'info_area': '부산', 'info_pay': '1,870만원', 'info_fuel': 'LPG(일반인 구입)'}, {'info_title': '현대 쏘나타 뉴 라이즈  LPI 스타일', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=34582920&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g11&tempht_arg=awM1Og361NO7_10', 'info_brand': '현대', 'info_model': 'LPI 스타일', 'info_caryear': '18/03식', 'info_usedmileage': '98,071km', 'info_area': '부산', 'info_pay': '1,190만원', 'info_fuel': 'LPG(일반인 구입)'}, {'info_title': '현대 팰리세이드  디젤 2.2 4WD VIP', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=34298091&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g12&tempht_arg=awM1Og361NO7_11', 'info_brand': '현대', 'info_model': '디젤 2.2 4WD VIP', 'info_caryear': '21/01식', 'info_usedmileage': '31,413km', 'info_area': '충북', 'info_pay': '4,890만원', 'info_fuel': '디젤'}, {'info_title': '기아 모닝 어반  밴', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=33981154&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g13&tempht_arg=awM1Og361NO7_12', 'info_brand': '기아', 'info_model': '밴', 'info_caryear': '21/06식', 'info_usedmileage': '2,593km', 'info_area': '경기', 'info_pay': '840만원', 'info_fuel': '가솔린'}, {'info_title': '현대 제네시스 DH  G380 파이니스트 에디션 AWD', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=34258430&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g14&tempht_arg=awM1Og361NO7_13', 'info_brand': '현대', 'info_model': 'G380 파이니스트 에디션 AWD', 'info_caryear': '16/02식', 'info_usedmileage': '31,136km', 'info_area': '서울', 'info_pay': '3,049만원', 'info_fuel': '가솔린'}, {'info_title': '현대 싼타페 TM  가솔린 2.0T 4WD 인스퍼레이션', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=34052373&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g15&tempht_arg=awM1Og361NO7_14', 'info_brand': '현대', 'info_model': '가솔린 2.0T 4WD 인스퍼레이션', 'info_caryear': '18/12식(19년형)', 'info_usedmileage': '53,225km', 'info_area': '경기', 'info_pay': '2,999만원', 'info_fuel': '가솔린'}, {'info_title': '쉐보레(GM대우) 더 뉴 트랙스  1.4 블레이드', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=34582919&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g16&tempht_arg=awM1Og361NO7_15', 'info_brand': '쉐보레(GM대우)', 'info_model': '1.4 블레이드', 'info_caryear': '18/06식', 'info_usedmileage': '15,325km', 'info_area': '부산', 'info_pay': '1,580만원', 'info_fuel': '가솔린'}, {'info_title': '현대 아이오닉6  롱레인지 익스클루시브 플러스', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=34549289&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g17&tempht_arg=awM1Og361NO7_16', 'info_brand': '현대', 'info_model': '롱레인지 익스클루시브 플러스', 'info_caryear': '22/10식(23년형)', 'info_usedmileage': '1,067km', 'info_area': '경기', 'info_pay': '4,720만원', 'info_fuel': '전기'}, {'info_title': '현대 쏘나타 (DN8)  2.0 프리미엄', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=33713530&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g18&tempht_arg=awM1Og361NO7_17', 'info_brand': '현대', 'info_model': '2.0 프리미엄', 'info_caryear': '19/11식(20년형)', 'info_usedmileage': '40,476km', 'info_area': '경기', 'info_pay': '1,950만원', 'info_fuel': '가솔린'}, {'info_title': '쌍용 렉스턴 스포츠  디젤 2.2 2WD 프레스티지', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=34505135&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g19&tempht_arg=awM1Og361NO7_18', 'info_brand': '쌍용', 'info_model': '디젤 2.2 2WD 프레스티지', 'info_caryear': '18/06식', 'info_usedmileage': '49,471km', 'info_area': '부산', 'info_pay': '1,890만원', 'info_fuel': '디젤'}, {'info_title': '기아 카니발 4세대  가솔린 7인승 노블레스', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=34512034&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g20&tempht_arg=awM1Og361NO7_19', 'info_brand': '기아', 'info_model': '가솔린 7인승 노블레스', 'info_caryear': '21/06식', 'info_usedmileage': '13,212km', 'info_area': '부산', 'info_pay': '3,930만원', 'info_fuel': '가솔린'}, {'info_title': '기아 카니발 4세대  9인승 프레스티지', 'info_url': 'http://www.encar.com//dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid=34490848&view_type=hs_ad&adv_attribute=hs_ad&wtClick_korList=019&advClickPosition=kor_normal_p1_g21&tempht_arg=awM1Og361NO7_20', 'info_brand': '기아', 'info_model': '9인승 프레스티지', 'info_caryear': '20/09식(21년형)', 'info_usedmileage': '20,121km', 'info_area': '부산', 'info_pay': '3,430만원', 'info_fuel': '디젤'}]
    # print(encar_product_list)
    # encar_infor_list = encar_get_detail_information(encar_product_list)

# start_encar()
