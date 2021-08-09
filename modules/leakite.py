import requests
from bs4 import BeautifulSoup
from re import search

LIST_CLASS_NAME = "rig columns-4"
DB_URL = "https://www.leakite.com/"
brand_s = 'download-'
### Find by Model Name Ex. Alcatel hh41nh ###

def Brand_LIST(page=0):
    global DB_URL
    database = requests.get(url = DB_URL + "download-android-firmware/")
    if database.status_code == 200:
        response_html = BeautifulSoup(database.text, 'html.parser')
        response_array = response_html.find_all('tbody')
        response_details = response_array[0].find_all('a', href=True)
        tmp_return = []
        for brand in response_details:
            if brand.get_text() != "" and brand.get_text() != "Other Brands":
                tmp_return.append(brand.get_text())
        return tmp_return
    else:
        return None

def Brand_Model_List(brand = None):
    global DB_URL
    if brand != "" or brand != None:
        NEW_DB_URL = DB_URL + brand.lower() + "/"
        database = requests.get(url = NEW_DB_URL)
        if database.status_code == 200:
            response_html = BeautifulSoup(database.text, 'html.parser')
            response_array = response_html.find_all('h2', class_="title front-view-title")
            tmp_return = []
            for model in response_array:
                if model.get_text() != "":
                    url = model.find_all('a', href=True)[0]['href']
                    tmp_return.append(prepare_model(url, brand.lower()))
            return tmp_return
        else:
            return None
    else:
        return "Missing Brand!.."


def prepare_model(model=None, brand=None):
    global brand_s
    brand_s = brand_s + brand + '-'
    if model != None or model != "" and brand != None or brand != "":
        if len(model.split('/')) != -1:
            model = model.split('/')[3]
        return model
    return model


def get_Download_LINK(model=None):
    global DB_URL
    tmp_return = []
    response = []
    if model != None or model != "":
        NEW_DB_URL = DB_URL + model
        print(NEW_DB_URL)
        database = requests.get(url = NEW_DB_URL)
        if database.status_code == 200:
            response_html = BeautifulSoup(database.text, 'html.parser')
            response_target_data = response_html.find_all('p')
            for response_target in response_target_data:
                response_target = response_target.find_all('a', href=True)
                if len(response_target) != 0:
                    if response_target[0].get_text() == "Download" or response_target[0].get_text() == "download":
                        response.append({"name": response_target[0].get_text(), "link": response_target[0]['href']})
            response_target_data = response_target_data[4].get_text().split('\n')
            fnm = ""
            fsz = ""
            for data in response_target_data:
                data = data.split(":")
                if len(data) != -1:
                    if search('File Name', data[0]):
                        fnm = data[1]
                    if search('Size', data[0]):
                        fsz = data[1]
                tmp_return.append({"filename": fnm, "size": fsz})
                tmp_return.append(response)
            return tmp_return
        else:
            return None
    else:
        return "Missing Model Info!.."

### List of Support Devices Brand_LIST() ###
### List of Support Models for Device Brand Brand_Model_List('alcate') ###
### List of Download Link(s) for Device Model Brand get_Download_LINK('alcatel-onetouch-flip-2-4047f') ###

print(get_Download_LINK('download-acer-e380-stock-firmware-flash-file'))