# coding:utf-8
import config
import requests
import json
import time
from prettytable import PrettyTable

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
    area_url = URL_BK + '/nCoV/api/provinceName'
    resp = requests.request("GET", area_url, headers=headers, data=payload)
    text = json.loads(resp.text)
    province = text['results']
    if v in province:
        return True, province
    else:
        return False, province


def overall():
    global msg, dailyPics
    over_url = URL + '/nCoV/api/overall'
    resp = requests.request("GET", over_url, headers=headers, data=payload)
    text = json.loads(resp.text)
    if 'results' in text:
        for item in text['results']:
            note1 = item.get('note1')
            note2 = item.get('note2')
            note3 = item.get('note3')
            confirmedCount = item.get('confirmedCount')
            confirmedIncr = item.get('confirmedIncr')
            suspectedCount = item.get('suspectedCount')
            suspectedIncr = item.get('suspectedIncr')
            seriousCount = item.get('seriousCount')
            seriousIncr = item.get('seriousIncr')
            curedCount = item.get('curedCount')
            curedIncr = item.get('curedIncr')
            deadCount = item.get('deadCount')
            deadIncr = item.get('deadIncr')
            dailyPics = item.get('dailyPic')
            remark3 = item.get('remark3')
            updateTime = item.get('updateTime')
            format_time = time.localtime(updateTime / 1000)
            _t = time.strftime("%Y-%m-%d %H:%M:%S", format_time)
            msg = '更新时间：' + _t + '\n' + note1 + '\n' + note2 + '\n' + note3 + '\n' + remark3 + '\n' + '确诊病例：' + str(confirmedCount) + '   较昨日+' + str(confirmedIncr) + '\n' + '疑似病例：' + str(suspectedCount) + '   较昨日+' + str(suspectedIncr) + '\n' + '重症病例：' + str(seriousCount) + '   较昨日+' + str(seriousIncr) + '\n' + '治愈人数：' + str(curedCount) + '   较昨日+' + str(curedIncr) + '\n' + '死亡人数：' + str(deadCount) + '   较昨日+' + str(deadIncr)
    return msg, dailyPics


def news():
    news_url = URL_BK + '/nCoV/api/news?num=5'
    resp = requests.request("GET", news_url, headers=headers, data=payload)
    text = json.loads(resp.text)
    return text


def rumors(num):
    news_url = URL_BK + '/nCoV/api/rumors?num=%s' % num
    resp = requests.request("GET", news_url, headers=headers, data=payload)
    text = json.loads(resp.text)
    return text


def area(info):
    area_url = URL_BK + '/nCoV/api/area?latest=1'
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
    elif '市' in info:
        region = info.split('市')[0]
        try:
            for item in text['results']:
                for i in range(len(item['cities'])):
                    if item['cities'][i].get('cityName') == region:
                        confirmedCount = item['cities'][i].get('confirmedCount')
                        deadCount = item['cities'][i].get('deadCount')
                        curedCount = item['cities'][i].get('curedCount')
                        _area.add_row([region, confirmedCount, deadCount, curedCount])
                    else:
                        pass
        except Exception as e:
            pass
    else:
        area_url = URL_BK + '/nCoV/api/area?latest=1&province=%s' % info
        resp = requests.request("GET", area_url, headers=headers, data=payload)
        text = json.loads(resp.text)
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
    text = '广州市'
    area(text)
