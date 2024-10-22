from flask import Flask, request, abort

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

# 軽量なウェブアプリケーションフレームワーク:Flask
app = Flask(__name__)

GEMINI_API_URL = "https://api.gemini.com/v1/chat" 


GEMINI_API_KEY = ("")
genai.configure(api_key="")

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

if __name__ == "__main__":
    print('a')
    gemini_reply = model.generate_content('こんにちは')
    print(gemini_reply.text)
    