import requests
from bs4 import BeautifulSoup
from re import search

LIST_CLASS_NAME = "rig columns-4"
DB_URL = "https://firmwarefile.com/"

### Find by Model Name Ex. Alcatel hh41nh ###

def Brand_LIST(page = 1):
    global DB_URL, LIST_CLASS_NAME
    if page < 9 or page == 9:
        database = requests.get(url = DB_URL + "page-" + str(page))
        if database.status_code == 200:
            response_html = BeautifulSoup(database.text, 'html.parser')
            response_array = response_html.find_all('ul', class_=LIST_CLASS_NAME)
            response_details = response_array[0].get_text().split('\n')
            tmp_return = []
            for brand in response_details:
                if brand != "" and "Page" not in brand:
                    tmp_return.append(brand)
            return tmp_return
        else:
            return None
    else:
        return "Length is min: 1, max: 9!.."

def Brand_Model_List(brand = None, page = 0):
    global DB_URL, LIST_CLASS_NAME
    if brand != "" or brand != None:
        if page == 0:
            NEW_DB_URL = DB_URL + "category/" + brand
        else:
            NEW_DB_URL = DB_URL + "category/" + brand + "/page/" + str(page)
        database = requests.get(url = NEW_DB_URL)
        if database.status_code == 200:
            response_html = BeautifulSoup(database.text, 'html.parser')
            response_array = response_html.find_all('ul', class_=LIST_CLASS_NAME)
            response_details = response_array[0].get_text().split(brand.capitalize())
            tmp_return = []
            for model in response_details:
                if model != " " and "Page" not in model:
                    tmp_return.append(prepare_model(brand + model))
            return tmp_return
        else:
            return None
    else:
        return "Missing Brand!.."


def prepare_model(model=None):
    if model != None or model != "":
        model = model.replace(" ", "-")
        return model[0:len(model) - 2]
    return model

def prepare_info_data(data=None):
    if data != None or data != "":
        tmp = data.split('\n')
        fname = tmp[0].split(': ')[1]
        fsize = tmp[1].split(': ')[1]
        return [fname, fsize]
    return data

def get_Download_LINK(model=None):
    global DB_URL
    tmp_return = []
    response = []
    if model != None or model != "":
        NEW_DB_URL = DB_URL + "/" + model
        database = requests.get(url = NEW_DB_URL)
        if database.status_code == 200:
            response_html = BeautifulSoup(database.text, 'html.parser')
            response_target = response_html.find_all('a', href=True)
            response_target_data = response_html.find_all('p')
            for data in response_target_data:
                if search('File Name:', data.get_text()) or search('File Size', data.get_text()):
                    response_data = prepare_info_data(data.get_text())
                    tmp_return.append({"filename": response_data[0], "size": response_data[1]})
            for line in response_target:
                if search('Mirror', line.get_text()) or search('Get Link', line.get_text()):
                    response.append({"name": line.get_text(), "link": line['href']})
            tmp_return.append(response)
            return tmp_return
        else:
            return None
    else:
        return "Missing Model Info!.."

### List of Support Devices Brand_LIST() for next page Brand_LIST(2) ###
### List of Support Models for Device Brand Brand_Model_List('alcate') for next page Brand_Model_List('alcatel', 2) ###
### List of Download Link(s) for Device Model Brand get_Download_LINK('alcatel-onetouch-flip-2-4047f') ###
