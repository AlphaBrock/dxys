# coding:utf-8
import config
import requests
import json
import time
from prettytable import PrettyTable
from tabulate import tabulate

URL = config.DXYS
URL_BK = config.DXYS_BK
payload = {}
headers = {}


# def check_api_status(url):
#     resp = requests.request("GET", url, headers=headers, data=payload)
#     r = resp.status_code
#     print(r)
#     if r == "502" or "403":
#         url = URL_BK
#         return url
#     else:
#         url = URL
#         return url


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def check_value(v):
    area_url = URL + '/nCoV/api/provinceName'
    resp = requests.request("GET", area_url, headers=headers, data=payload)
    text = json.loads(resp.text)
    province = text['results']
    if v in province:
        return True, province
    else:
        return False, province


def overall():
    global msg, img
    over_url = URL + '/nCoV/api/overall'
    resp = requests.request("GET", over_url, headers=headers, data=payload)
    text = json.loads(resp.text)
    if 'results' in text:
        for item in text['results']:
            virus = item.get('virus')
            infectSource = item.get('infectSource')
            passWay = item.get('passWay')
            confirmedCount = item.get('confirmedCount')
            suspectedCount = item.get('suspectedCount')
            curedCount = item.get('curedCount')
            deadCount = item.get('deadCount')
            dailyPic = item.get('dailyPic')
            updateTime = item.get('updateTime')
            format_time = time.localtime(updateTime / 1000)
            _t = time.strftime("%Y-%m-%d %H:%M:%S", format_time)
            msg = '更新时间：' + _t + '\n' + '病毒名称：' + virus + '\n' + "感染源    ：" + infectSource + '\n' + "传播途径：" + passWay + '\n' + '确诊病例：' + str(
                confirmedCount) + '\n' + '疑似病例：' + str(suspectedCount) + '\n' + '治愈人数：' + str(
                curedCount) + '\n' + '死亡人数：' + str(deadCount)
            response = requests.request("GET", dailyPic)
            img = response.content
    return msg, img


def news():
    news_url = URL + '/nCoV/api/news?num=5'
    resp = requests.request("GET", news_url, headers=headers, data=payload)
    text = json.loads(resp.text)
    return text


def rumors(num):
    news_url = URL + '/nCoV/api/rumors?num=%s' % num
    resp = requests.request("GET", news_url, headers=headers, data=payload)
    text = json.loads(resp.text)
    return text


def area(info):
    area_url = URL + '/nCoV/api/area?latest=1'
    resp = requests.request("GET", area_url, headers=headers, data=payload)
    text = json.loads(resp.text)
    _area = PrettyTable(['地区', '确诊', '死亡', '治愈'])
    if '中国' in info:
        if 'results' in text:
            for item in text['results']:
                if item.get('country') == info:
                    provinceShortName = item.get('provinceShortName')
                    confirmedCount = item.get('confirmedCount')
                    deadCount = item.get('deadCount')
                    curedCount = item.get('curedCount')
                    _area.add_row([provinceShortName, confirmedCount, deadCount, curedCount])
    elif '全球' in info:
        if 'results' in text:
            for item in text['results']:
                if item.get('country') != '中国':
                    provinceShortName = item.get('provinceShortName')
                    confirmedCount = item.get('confirmedCount')
                    deadCount = item.get('deadCount')
                    curedCount = item.get('curedCount')
                    _area.add_row([provinceShortName, confirmedCount, deadCount, curedCount])
    else:
        area_url = URL + '/nCoV/api/area?latest=1&province=%s' % info
        resp = requests.request("GET", area_url, headers=headers, data=payload)
        text = json.loads(resp.text)
        if len(text['results'][0]['cities']) < 1:
            pass
        else:
            citys = text['results'][0]['cities']
            for item in range(len(citys)):
                cityName = citys[item].get('cityName')
                confirmedCount = citys[item].get('confirmedCount')
                deadCount = citys[item].get('deadCount')
                curedCount = citys[item].get('curedCount')
                _area.add_row([cityName, confirmedCount, deadCount, curedCount])
    _area.align['地区'] = 'l'
    _area.align['确诊'] = 'r'
    _area.align['死亡'] = 'r'
    _area.align['治愈'] = 'r'
    _area.padding_width = 1
    _area.sortby = '确诊'
    _area.reversesort = True
    print(_area)
    return _area


if __name__ == '__main__':
    text = '广东省'
    area(text)
    # news()
