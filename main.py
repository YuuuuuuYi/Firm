import json
import random
import time
from time import localtime

import requests
import schedule as schedule
from requests import get, post
from datetime import datetime, date
from zhdate import ZhDate
import sys
import os
 

corpid = "ww639ead620175218e"
secret = "GxoHCqQZE4Z8diTqWAdWNuIsnweLvgT3EXzuaSLLF48"
agentid = "1000003"
weather_key = "6504d4c67935468398c27b75066f62f8"
love_date = "2023-02-19"

def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)
 
 
def get_access_token():
    # # appId
    # corpid = config["app_id"]
    # # appSecret
    # secret = config["app_secret"]
    post_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={secret}"
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    # print(access_token)
    return access_token
 
 
def get_weather(region):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    key = weather_key
    region_url = "https://geoapi.qweather.com/v2/city/lookup?location={}&key={}".format(region, key)
    response = get(region_url, headers=headers).json()
    if response["code"] == "404":
        print("推送消息失败，请检查地区名是否有误！")
        os.system("pause")
        sys.exit(1)
    elif response["code"] == "401":
        print("推送消息失败，请检查和风天气key是否正确！")
        os.system("pause")
        sys.exit(1)
    else:
        # 获取地区的location--id
        location_id = response["location"][0]["id"]
    weather_url = "https://devapi.qweather.com/v7/weather/now?location={}&key={}".format(location_id, key)
    response = get(weather_url, headers=headers).json()
    # 天气
    weather = response["now"]["text"]
    # 当前温度
    temp = response["now"]["temp"] + u"\N{DEGREE SIGN}" + "C"
    # 风向
    wind_dir = response["now"]["windDir"]
    return weather, temp, wind_dir
 
 
def get_birthday(birthday, year, today):
    birthday_year = birthday.split("-")[0]
    # 判断是否为农历生日
    if birthday_year[0] == "r":
        r_mouth = int(birthday.split("-")[1])
        r_day = int(birthday.split("-")[2])
        # 获取农历生日的今年对应的月和日
        try:
            birthday = ZhDate(year, r_mouth, r_day).to_datetime().date()
        except TypeError:
            print("请检查生日的日子是否在今年存在")
            os.system("pause")
            sys.exit(1)
        birthday_month = birthday.month
        birthday_day = birthday.day
        # 今年生日
        year_date = date(year, birthday_month, birthday_day)
 
    else:
        # 获取国历生日的今年对应月和日
        birthday_month = int(birthday.split("-")[1])
        birthday_day = int(birthday.split("-")[2])
        # 今年生日
        year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        if birthday_year[0] == "r":
            # 获取农历明年生日的月和日
            r_last_birthday = ZhDate((year + 1), r_mouth, r_day).to_datetime().date()
            birth_date = date((year + 1), r_last_birthday.month, r_last_birthday.day)
        else:
            birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day
 
 
def get_ciba():
    url = "http://open.iciba.com/dsapi/"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    r = get(url, headers=headers)
    note_en = r.json()["content"]
    note_ch = r.json()["note"]
    return note_ch, note_en
 
 
def send_message(access_token, region_name, weather, temp, wind_dir, note_ch, note_en, love_date = "2023-02-19"):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    # 获取在一起的日子的日期格式
    love_year = int(love_date.split("-")[0])
    love_month = int(love_date.split("-")[1])
    love_day = int(love_date.split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    # 获取所有生日数据
    birthdays = {}
    birthdays["birthday1"] = {"name": "赵明宇", "birthday": "1999-12-31"}
    birthdays["birthday2"] = {"name": "宝宝", "birthday": "2000-07-04"}

    ##
    files = {"files": open(r"1.jpg", "rb")}

    try:
        ip = requests.get('https://ident.me').text.strip()
        print(ip)
    except :
        print("No ip")

    time.sleep(10)


    response = requests.post(f'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=image',
                             files=files)


    a = json.loads(response.text)
    print(response.text)
    media_id = a["media_id"]

    data = {
        "touser": "@all",
        "msgtype": "mpnews",
        "agentid": "1000003",
        "topcolor": "#FF0000",
        "mpnews": {
            "articles":  [
                {
                    "title":"早安宝宝~",
                    "digest":"{} {}\n\n".format(today, week) + region_name + "\n\n" + weather + "\n\n" + temp + "\n\n" + wind_dir + "\n\n" + love_days + "\n\n" + note_en + "\n\n" + note_ch + "\n\n"
                    ,
                    "date": {
                        "value": "{} {}".format(today, week),
                        "color": get_color()
                    },
                    "region": {
                        "value": region_name,
                        "color": get_color()
                    },
                    "weather": {
                        "value": weather,
                        "color": get_color()
                    },
                    "temp": {
                        "value": temp,
                        "color": get_color()
                    },
                    "wind_dir": {
                        "value": wind_dir,
                        "color": get_color()
                    },
                    "love_day": {
                        "value": love_days,
                        "color": get_color()
                    },
                    "note_en": {
                        "value": note_en,
                        "color": get_color()
                    },
                    "note_ch": {
                        "value": note_ch,
                        "color": get_color()
                    },
                    "thumb_media_id": media_id,
                    "content": 'www.baidu.com'+'\n'+'点击阅读原文查看精彩↓↓↓',
                }
            ]
        },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    for key, value in birthdays.items():
        # 获取距离下次生日的时间
        birth_day = get_birthday(value["birthday"], year, today)
        if birth_day == 0:
            birthday_data = "今天{}生日哦，祝{}生日快乐！".format(value["name"], value["name"])
        else:
            birthday_data = "距离{}的生日还有{}天".format(value["name"], birth_day)
        # 将生日数据插入data
        #data["data"][key] = {"value": birthday_data, "color": get_color()}
        data["mpnews"]["articles"][0][key] = {"value": birthday_data, "color": get_color()}
    HEADERS = {"Content-Type": "application/json ;charset=utf-8"}
    String_textMsg = json.dumps(data)
    response = post(url, headers=HEADERS, data=String_textMsg,).json()
    print(response)
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)
 

    # try:
    #     with open("config.txt", encoding="utf-8") as f:
    #         config = eval(f.read())
    # except FileNotFoundError:
    #     print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
    #     os.system("pause")
    #     sys.exit(1)
    # except SyntaxError:
    #     print("推送消息失败，请检查配置文件格式是否正确")
    #     os.system("pause")
    #     sys.exit(1)
    #
    # 获取accessToken
def main():
    accessToken = get_access_token()
    # 接收的用户
    # users = config["user"]
    # 传入地区获取天气信息
    region = "香港"
    weather, temp, wind_dir = get_weather(region)
    note_ch = ""
    note_en = ""
    if note_ch == "" and note_en == "":
        # 获取词霸每日金句
        note_ch, note_en = get_ciba()
        # 公众号推送消息
        # for user in users:
    send_message(accessToken, region, weather, temp, wind_dir, note_ch, note_en)

if __name__ == '__main__':

    main()
    # schedule.every().day.at('11:35').do(main)
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(30)


