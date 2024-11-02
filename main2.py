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

with open('dic.txt', 'r', encoding='utf-8') as f:
    dic_content = f.read()

# 軽量なウェブアプリケーションフレームワーク:Flask
app = Flask(__name__)

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
default_initial_prompt = f"{dic_content}"

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

hello = "このラインボットでは大阪工業大学情報科学部の授業について知ることができます！履修時期や単位数から検索もできるので試してみてください！"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    print("message",message)
    if(message == "hello"):
        reply_message = TextSendMessage(text=hello)
        line_bot_api.reply_message(event.reply_token, reply_message)
    else:
        gemini_reply = model.generate_content(default_initial_prompt + message)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=gemini_reply.text.rstrip()),
        )

@app.route("/")
def home():
    return "Hello, this is the home page!"

if __name__ == "__main__":
    
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
