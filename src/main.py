import requests
import json
import os
import urllib.request

# 天気情報を取得
def weather_get(place):

  url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&lang=ja".format(place,os.environ["WEATHER_APP_ID"])

  res = requests.get(url)
  if res.status_code == requests.codes.ok:

    res_json = res.json()
    data = json.loads(json.dumps(res_json, indent=2))

    msg = ""
    weather = data["weather"][0]["description"]

    if data["weather"][0]["main"] == "Rain":
      msg = "傘がいるよ！"
    elif data["weather"][0]["main"] != "rain":
      msg = "傘はいらないよ！"

    out_msg = "天気:{}\n{}\n{}".format(weather,msg,data["weather"][0]["main"])

    return out_msg

  elif res.status_code != requests.codes.ok:
    return "わかんないな〜"



def lambda_handler(event, context):
    # 送られたメッセージから地点と返信用トークンを取得
    for message_event in json.loads(event['body'])['events']:
        place = message_event['message']['text']
        reply_token = message_event['replyToken']

    message = weather_get(place)

    # チャンネルアクセストークンと返信用トークンを用いてユーザにメッセージを返す
    url = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["ChannelAccessToken"]
    }
    body = {
        'replyToken': reply_token,
        'messages': [
            {
                "type": "text",
                "text": message,
            }
        ]
    }

    req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), method='POST', headers=headers)
    with urllib.request.urlopen(req) as res:
        logger.info(res.read().decode("utf-8"))


    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }
