# coding:utf-8

import config
import dxys
import telebot
import time
import requests
import threading
from db import Database
from apscheduler.schedulers.background import BackgroundScheduler

TOKEN = config.TOKEN
bot = telebot.TeleBot(TOKEN)


class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, chat_id, city):
        threading.Thread.__init__(self)
        self.city = city
        self.chat_id = chat_id

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print(self.city)
        table = dxys.area(self.city)
        bot.send_message(self.chat_id, '您的订阅城市(%s)统计人数如下：' % self.city)
        bot.send_message(self.chat_id, table)


@bot.message_handler(commands=['start'])
def bot_start(message):
    me = bot.get_me()
    print(message.chat.id)
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, '欢迎使用丁香医生 ~\n要不戳这里试试看 /help')
    bot.send_message(message.chat.id, me)


@bot.message_handler(commands=['help'])
def bot_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,
                     "我能帮你查看新型冠状病毒 2019-nCoV疫情情况\n"
                     "**⚠数据均来源于丁香医生⚠**\n"
                     "/help - 查看帮助\n"
                     "/overall - 查看概览\n"
                     "/news - 查看最近10条新闻\n"
                     "/rumors - 查看发布的辟谣信息，用法：/rumors 不带参数默认最近5条 或者 /rumors 5/all 带参数获取指定条数\n"
                     "/area - 查看区域统计人数，用法：/area 中国或者/area 全球(只支持国内省，直辖市与自治区)\n"
                     "/sub - 订阅城市/省份统计人数，用法：/sub 广东省或者/sub 广州市(只支持国内省，直辖市与自治区)\n"
                     "/unsub - 取消订阅", parse_mode='Markdown')


@bot.message_handler(commands=['overall'])
def bot_overall(message):
    msg, dailyPics = dxys.overall()
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, msg)
    for item in range(len(dailyPics.split(','))):
        response = requests.request("GET", dailyPics.split(',')[item])
        img = response.content
        bot.send_photo(message.chat.id, img)


@bot.message_handler(commands=['news'])
def bot_news(message):
    bot.send_chat_action(message.chat.id, 'typing')
    text = dxys.news()
    if 'results' in text:
        for item in text['results']:
            title = item.get('title')
            summary = item.get('summary')
            infoSource = item.get('infoSource')
            sourceUrl = item.get('sourceUrl')
            pubDate = item.get('pubDate')
            format_time = time.localtime(pubDate / 1000)
            _t = time.strftime("%Y-%m-%d %H:%M:%S", format_time)
            news = '发布日期：' + _t + '\n' + '标题：' + title + '\n' + '内容：' + summary + '\n' + '信息来源：' + infoSource + '\n\n' + '来源链接：' + sourceUrl
            bot.send_message(message.chat.id, news)


@bot.message_handler(commands=['rumors'])
def bot_rumors(message):
    num = '5'
    length = len(message.text.split(' '))
    bot.send_chat_action(message.chat.id, 'typing')
    if length == 1:
        if message.text == "/rumors":
            num = '5'
    elif length > 1:
        if dxys.is_number(message.text.split(' ')[1]) is False:
            bot.send_message(message.chat.id, '输入格式有误，例：`/rumors 20`', parse_mode='Markdown')
            return
        elif dxys.is_number(message.text.split(' ')[1]) is True:
            num = message.text.split(' ')[1]
    text = dxys.rumors(num)
    bot.send_chat_action(message.chat.id, 'typing')
    if 'results' in text:
        for item in text['results']:
            rumors = '标题：' + item.get('title') + '\n' + '概要：' + item.get(
                'mainSummary') + '\n' + '详情：' + item.get(
                'body')
            bot.send_message(message.chat.id, rumors)


@bot.message_handler(commands=['area'])
def bot_area(message):
    length = len(message.text.split(' '))
    bot.send_chat_action(message.chat.id, 'typing')
    if length == 1:
        bot.send_message(message.chat.id, '输入格式有误，例：`/area 中国 或者/area 全球 或者 /area 广东省`', parse_mode='Markdown')
    else:
        text = message.text.split(' ')[1]
        status, provinceName = dxys.check_value(text)
        if status is True or '中国' in text or '全球' in text:
            table = dxys.area(text)
            bot.send_message(message.chat.id, table, parse_mode='markdown')
        elif status is False:
            bot.send_message(message.chat.id, '输入省份有误，参考如下：\n', parse_mode='Markdown')
            bot.send_message(message.chat.id, '%s' % provinceName, parse_mode='Markdown')


@bot.message_handler(commands='sub')
def region_sub(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if len(message.text.split(' ')) == 1:
        bot.send_message(message.chat.id, '输入省市格式，例：`/sub 广东省或者/sub 广州市或者/sub 中国 或者/sub 全球`', parse_mode='Markdown')
    else:
        text = message.text.split(' ')[1]
        data = Database().query_chat_id()
        region = []
        for i in range(len(data)):
            region.append(data[i][2])
        if text in region:
            bot.send_message(message.chat.id, '你已订阅过%s' % text)
        else:
            status, provinceName = dxys.check_value(text)
            if status is True or '中国' in text or '全球' in text or '市' in text:
                data = (message.chat.id, text)
                Database().create_chat_id(data)
                bot.send_message(message.chat.id, '订阅成功', parse_mode='Markdown')
                table = dxys.area(text)
                bot.send_message(message.chat.id, '你订阅的省份/城市为：%s' % text, parse_mode='Markdown')
                bot.send_message(message.chat.id, table, parse_mode='markdown')
            elif status is False:
                bot.send_message(message.chat.id, '输入省份/城市有误，参考如下：\n', parse_mode='Markdown')
                bot.send_message(message.chat.id, '%s' % provinceName, parse_mode='Markdown')


@bot.message_handler(commands='unsub')
def region_unsub(message):
    bot.send_chat_action(message.chat.id, 'typing')
    status = (Database().delete_chat_id(message.chat.id))
    if len(status) == 0:
        bot.send_message(message.chat.id, '取消订阅成功')
    else:
        bot.send_message(message.chat.id, '未查询到当前用户的订阅')


def sub_schedule():
    regions = []
    threads = []
    data = Database().query_chat_id()
    try:
        for i in range(len(data)):
            region = [data[i][1], data[i][2]]
            regions.append(region)
        print(regions, type(regions))
        for j in range(len(regions)):
            city = regions[j][0]
            chat_id = regions[j][1]
            thread = myThread(city, chat_id)
            thread.start()
            threads.append(thread)
            for t in threads:
                t.join()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    try:
        sched = BackgroundScheduler(daemon=True)
        sched.add_job(lambda: sub_schedule(), 'cron', hour=8, minute=30)
        sched.start()
    except Exception as e:
        print(e)
    bot.polling(none_stop=True)
