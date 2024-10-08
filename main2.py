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

course_info = {
    "微積分学": {"担当教授": "A教授", "単位取得率": "85%", "定期テスト": "あり", "出席確認": "あり", "履修時期": "１年前期"},
    "C言語": {"担当教授": "B教授", "単位取得率": "80%", "定期テスト": "なし", "出席確認": "あり", "履修時期": "１年後期"},
    "生物": {"担当教授": "C教授", "単位取得率": "98%", "定期テスト": "なし", "出席確認": "なし", "履修時期": "２年前期"},
    "化学": {"担当教授": "D教授", "単位取得率": "90%", "定期テスト": "あり", "出席確認": "あり", "履修時期": "３年前期"}
}

# 軽量なウェブアプリケーションフレームワーク:Flask
app = Flask(__name__)


#環境変数からLINE Access Tokenを設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
#環境変数からLINE Channel Secretを設定
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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

# MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text  # ユーザーのメッセージ
    response = ""
    a = 0

    # 一年生で履修できる講義を知りたい場合
    if re.search(r"(１年|一年|1年)", message):
        if re.search(r"(前期)", message):
            response += "１年前期で履修できる授業\n"
            for course, info in course_info.items():
                if re.search(r"１年前期", info['履修時期']):
                    response += f"・{course}\n"
        elif re.search(r"(後期)", message):
            response += "１年後期で履修できる授業\n"
            for course, info in course_info.items():
                if re.search(r"１年後期", info['履修時期']):
                    response += f"・{course}\n"
        else:
            response += "１年で履修できる授業\n"
            for course, info in course_info.items():
                if re.search(r"１年", info['履修時期']):
                    response += f"・{course}\n"

    # 二年生で履修できる講義を知りたい場合
    elif re.search(r"(２年|二年|2年)", message):
        if re.search(r"(前期)", message):
            response += "２年前期で履修できる授業\n"
            for course, info in course_info.items():
                if re.search(r"２年前期", info['履修時期']):
                    response += f"・{course}\n"
        elif re.search(r"(後期)", message):
            response += "２年後期で履修できる授業\n"
            for course, info in course_info.items():
                if re.search(r"２年後期", info['履修時期']):
                    response += f"・{course}\n"
        else:
            response += "２年で履修できる授業\n"
            for course, info in course_info.items():
                if re.search(r"２年", info['履修時期']):
                    response += f"・{course}\n"

    # 三年生で履修できる講義を知りたい場合
    elif re.search(r"(３年|三年|3年)", message):
        if re.search(r"(前期)", message):
            response += "３年前期で履修できる授業\n"
            for course, info in course_info.items():
                if re.search(r"３年前期", info['履修時期']):
                    response += f"・{course}\n"
        elif re.search(r"(後期)", message):
            response += "３年後期で履修できる授業\n"
            for course, info in course_info.items():
                if re.search(r"３年後期", info['履修時期']):
                    response += f"・{course}\n"
        else:
            response += "３年で履修できる授業\n"
            for course, info in course_info.items():
                if re.search(r"３年", info['履修時期']):
                    response += f"・{course}\n"

    # 授業の一覧を見たい場合
    elif re.search(r"(はい|みたい|見たい|みせて|見せて|表示|一覧)", message):
        for course, info in course_info.items():
            response += f"{course}\n"

    # すべての講義情報を求めている場合
    elif re.search(r"すべて|詳しく|全部|全て", message):
        for course, info in course_info.items():
            response += (f"講義名: {course}\n担当教授: {info['担当教授']}\n単位取得率: {info['単位取得率']}\n"
                         f"定期テスト: {info['定期テスト']}\n出席確認: {info['出席確認']}\n"
                         f"履修時期: {info['履修時期']}\n\n")

    # 入力から授業名を抽出して詳細情報を表示
    else:
        for course in course_info.keys():
            if re.search(course, message):
                info = course_info[course]
                # 質問がどの情報を求めているかを判定
                if re.search(r"(?=.*(履修|受|？))(?=.*(いつ|後期|前期)|履修時期)", message):
                    a = 1
                    response += f"{course}は{info['履修時期']}に履修できます。\n"
                if re.search(r"教授|先生|担当", message):
                    a = 1
                    response += f"{course}の担当教授は{info['担当教授']}です。\n"
                if re.search(r"単位取得率", message):
                    a = 1
                    response += f"{course}の単位取得率は{info['単位取得率']}です。\n"
                if re.search(r"定期テスト", message):
                    a = 1
                    response += f"{course}は定期テストが{info['定期テスト']}ます。\n"
                if re.search(r"出席確認", message):
                    a = 1
                    response += f"{course}は出席確認が{info['出席確認']}ます。\n"
                if a == 0:
                    response = (f"講義名: {course}\n担当教授: {info['担当教授']}\n単位取得率: {info['単位取得率']}\n"
                                f"定期テスト: {info['定期テスト']}\n出席確認: {info['出席確認']}\n履修時期: {info['履修時期']}\n")
                break

    # メッセージが設定されていない場合のデフォルト応答
    if not response:
        response = "その講義についての情報はありません。講義一覧を見ますか？"

    # 返信を送信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response)
    )


@app.route("/")
def home():
    return "Hello, this is the home page!"

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)