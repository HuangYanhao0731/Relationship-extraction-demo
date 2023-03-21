import sys
import json
import base64
import requests
import ssl
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus

API_KEY = 'byPBzIjGCiAWfXUEUOV5ZGhi'# 要以字符串的形式哦！！！！
SECRET_KEY = 'EjO38wWZbbP7VKBQjEQRtb1tZDv3uWYg'# 要以字符串的形式哦！！！！


def fetch_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + API_KEY + '&client_secret=' + SECRET_KEY
    response = requests.get(host)
    if response:
        result = response.json()
        return result['access_token']


def read_file(image_path):
    f = open(image_path, 'rb')
    return f.read()
    f.close()


def ocr(token, picture_file):
    img = base64.b64encode(picture_file)
    params = {"image": img}
    access_token = token
    request_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()


if __name__ == '__main__':
    with open('static/first/book_ninth.txt',"w+",encoding="gb18030") as fo:
        for i in range(33):
            token = fetch_token()
            picture_file = read_file('output/ninth/page_'+str(i)+".png")
            result_json = ocr(token, picture_file)
            text = ""
            for words_result in result_json["words_result"]:
                text = text + words_result["words"]
    # fo = open('static/book1.txt', 'w+')
            list_passwds = text
            fo.writelines(list_passwds)
    fo.close()
    print(text)

