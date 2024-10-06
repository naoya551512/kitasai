from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)


# 環境変数からLINEのアクセストークンとシークレットを取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/debug")
def debug():
    access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'Not Found')
    secret = os.getenv('LINE_CHANNEL_SECRET', 'Not Found')
    return f"Access Token: {access_token}, Secret: {secret}"

@app.route("/callback", methods=['POST'])
def callback():
    # X-Line-Signature ヘッダーから署名を取得
    signature = request.headers['X-Line-Signature']

    # リクエストボディの内容を取得
    body = request.get_data(as_text=True)

    # 署名を検証し、問題があればエラーを返す
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# メッセージが送信された時の処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 受け取ったメッセージをそのまま返す
    reply_text = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run()
