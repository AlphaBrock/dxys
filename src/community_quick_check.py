
# coding:utf-8
from __future__ import unicode_literals

import config
import requests
import json

QQ_URL = config.QQ
MAP_KEY = config.MAP_KEY


def getPosition():
    url = QQ_URL + '/api/getPosition'
    response = requests.request("GET", url)
    text = json.loads(response.text)
    position = text['position']
    return position


def check_param(province, city, district):
    position = str(getPosition())
    if province not in position or city not in position or district not in position:
        return False
    else:
        return True


def get_location(location):
    global coordinate
    url = 'https://restapi.amap.com/v3/geocode/geo?key=%s&address=%s&output=json' % (MAP_KEY, location)
    response = requests.request("GET", url)
    text = json.loads(response.text)
    _t = text['geocodes']
    for i in _t:
        coordinate = i['location']
    return coordinate


def get_distance(origins, destination):
    distance = ''
    url = 'https://restapi.amap.com/v3/distance?key=%s&origins=%s&destination=%s&output=json&type=0' % (MAP_KEY, origins, destination)
    response = requests.request("GET", url)
    text = json.loads(response.text)
    _t = text['results']
    for i in _t:
        distance = str(format(float(i['distance'])/1000, '.2f')) + 'km'
    return distance


def getCommunity(province, city, district):
    info = {}
    url = QQ_URL + '/api/getCommunity?province=%s&city=%s&district=%s' % (province, city, district)
    response = requests.request("GET", url)
    text = json.loads(response.text)
    length = len(text['community'][province])
    if length == 0:
        info = '未查询到相关信息'
    else:
        _i = text['community'][province][city]
        if len(_i) == 0:
            info = '未查询到相关信息'
        elif len(_i) == 1:
            info = text['community'][province][city][district]
        elif len(_i) > 1:
            info = text['community'][province][city]
    return info


if __name__ == '__main__':
    province = '广东省'
    city = '广州市'
    district = '全部'
    location = '南雄市宾阳小区'
    getCommunity(province, city, district)
    # getPosition()
    # check_param(province, city, district)
    # location = '广东省广州市荔湾区中海花湾'
    # get_location(location)
    # origins = "114.318246,25.122732"
    # destination = "113.243599,23.12429"
    # get_distance(origins, destination)