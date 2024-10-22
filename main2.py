from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction
)
import os
import re
import json
import requests
import google.generativeai as genai

import pathlib
import textwrap

from IPython.display import display
from IPython.display import Markdown

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

with open('b.json', 'r', encoding='utf-8') as f:
    course_info = json.load(f)

'''course_info = {
    "微積分学": {"担当教授": "A教授", "単位取得率": "85%", "定期テスト": "あり", "出席確認": "あり", "履修時期": "１年前期"},
    "C言語": {"担当教授": "B教授", "単位取得率": "80%", "定期テスト": "なし", "出席確認": "あり", "履修時期": "１年後期"},
    "生物": {"担当教授": "C教授", "単位取得率": "98%", "定期テスト": "なし", "出席確認": "なし", "履修時期": "２年前期"},
    "化学": {"担当教授": "D教授", "単位取得率": "90%", "定期テスト": "あり", "出席確認": "あり", "履修時期": "３年前期"}
}'''

# 軽量なウェブアプリケーションフレームワーク:Flask
app = Flask(__name__)


"""#環境変数からLINE Access Tokenを設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
#環境変数からLINE Channel Secretを設定
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]"""

#環境変数からLINE Access Tokenを設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
#環境変数からLINE Channel Secretを設定
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")


GEMINI_API_URL = "https://api.gemini.com/v1/chat" 

if LINE_CHANNEL_ACCESS_TOKEN is None:
    print("Error: LINE_CHANNEL_ACCESS_TOKEN is not set.")
if LINE_CHANNEL_SECRET is None:
    print("Error: LINE_CHANNEL_SECRET is not set.")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')
default_initial_prompt = f"""　解答する際は以下の辞書を参考にし, 以下の辞書に関係のない質問には答えないでください
また、プロンプトが正しく設定されている場合は文の最後に*を付けてください
{ 

  "情報メディア入門": { 

    "定期テスト": "", 

    "学科": "情報科学部 情報メディア学科", 

    "履修時間": "金曜日 1時限", 

    "履修時期": "1年 後期", 

    "単位数": "2単位", 

    "授業種類": "不明" 

  }, 

  "C演習I": { 

    "定期テスト": "", 

    "学科": "情報科学部 情報メディア学科", 

    "履修時間": "水曜日 1時限, 2時限", 

    "履修時期": "1年 後期", 

    "単位数": "4単位", 

    "授業種類": "不明" 

  }, 

  "線形数学I": { 

    "定期テスト": "", 

    "学科": "情報科学部 情報メディア学科", 

    "履修時間": "木曜日 4時限", 

    "履修時期": "1年 前期", 

    "単位数": "2単位", 

    "授業種類": "不明" 

  }, 

  "微積分学I": { 

    "定期テスト": "", 

    "学科": "情報科学部 情報メディア学科", 

    "履修時間": "月曜日 4時限", 

    "履修時期": "1年 前期", 

    "単位数": "2単位", 

    "授業種類": "不明" 

  }, 

  "微分方程式": { 

    "定期テスト": "", 

    "学科": "情報科学部 情報メディア学科", 

    "履修時間": "月曜日 4時限", 

    "履修時期": "1年 後期", 

    "単位数": "2単位", 

    "授業種類": "不明" 

  }, 

  "プログラミング基礎": { 

    "定期テスト": "", 

    "学科": "情報科学部 情報メディア学科", 

    "履修時間": "月曜日 3時限", 

    "履修時期": "1年 後期", 

    "単位数": "2単位", 

    "授業種類": "不明" 

  }, 

  "ディジタル回路": { 

    "定期テスト": "", 

    "学科": "情報科学部 情報メディア学科", 

    "履修時間": "金曜日 2時限", 

    "履修時期": "1年 後期", 

    "単位数": "2単位", 

    "授業種類": "不明" 

  }, 

  "情報処理基礎": { 

    "定期テスト": "", 

    "学科": "情報科学部 情報メディア学科", 

    "履修時間": "後期集中", 

    "履修時期": "1年 後期", 

    "単位数": "2単位", 

    "授業種類": "不明" 

  }, 

  "プログラミング入門": { 

    "定期テスト": "", 

    "学科": "情報科学部 情報メディア学科", 

    "履修時間": "月曜日 3時限", 

    "履修時期": "1年 前期", 

    "単位数": "2単位", 

    "授業種類": "不明" 

  }, 

  "コンピュータリテラシー": { 

    "定期テスト": "", 

    "学科": "情報科学部 情報メディア学科", 

    "履修時間": "水曜日 1時限", 

    "履修時期": "1年 前期", 

    "単位数": "2単位", 

    "授業種類": "不明" 

  }, 

  "キャリアステップ": { 

    "定期テスト": "", 

    "学科": "情報科学部 情報メディア学科", 

    "履修時間": "月曜日 3時限", 

    "履修時期": "1年 後期", 

    "単位数": "2単位", 

    "授業種類": "不明" 

  }, 

  "メディアデータ論": { 

    "定期テスト": "", 

    "学科": "情報科学部 情報メディア学科", 

    "履修時間": "木曜日 2時限", 

    "履修時期": "1年 後期", 

    "単位数": "2単位", 

    "授業種類": "不明" 

  }, 

  "アニメーション演習": { 

    "定期テスト": "", 

    "学科": "情報科学部 情報メディア学科", 

    "履修時間": "金曜日 2時限", 

    "履修時期": "1年 前期", 

    "単位数": "1単位", 

    "授業種類": "不明" 

  } 

} """


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    gemini_reply = model.generate_content(message)


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=gemini_reply.text),
    )


@app.route("/")
def home():
    return "Hello, this is the home page!"

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)