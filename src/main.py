# coding:utf-8

import config
import dxys
import telebot
import time

TOKEN = config.TOKEN
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def bot_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, '欢迎使用丁香医生 ~\n要不戳这里试试看 /help')


@bot.message_handler(commands=['help'])
def bot_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,
                     "我能帮你查看此时疫情情况\n"
                     "**⚠数据均来源于丁香医生⚠**\n"
                     "help - 查看帮助\n"
                     "overall - 查看概览\n"
                     "news - 查看最近10条新闻\n"
                     "rumors - 查看发布的辟谣信息，用法：/rumors 不带参数默认最近5条 或者 /rumors 5/all 带参数获取指定条数\n"
                     "area - 查看区域统计人数，用法：/area 中国或者/area 全球\n", parse_mode='Markdown')


@bot.message_handler(commands=['overall'])
def bot_overall(message):
    msg = dxys.overall().encode('utf-8')
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, msg)


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
    elif length > 1:
        text = message.text.split(' ')[1]
        status, provinceName = dxys.check_value(text)
        if status is False:
            bot.send_message(message.chat.id, '输入省份有误，参考如下：\n', parse_mode='Markdown')
            bot.send_message(message.chat.id, '%s' % provinceName, parse_mode='Markdown')
        else:
            table = dxys.area(text)
            bot.send_message(message.chat.id, table, parse_mode='markdown')


if __name__ == '__main__':
    bot.polling(none_stop=True)
