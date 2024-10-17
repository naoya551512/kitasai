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


GEMINI_API_KEY = ("AIzaSyCkOsYaHDXylTcu21dTE9hQZ6AnZ11Lr4A")
genai.configure(api_key="AIzaSyCkOsYaHDXylTcu21dTE9hQZ6AnZ11Lr4A")

model = genai.GenerativeModel('gemini-1.5-flash')


    



if __name__ == "__main__":
    print('a')
    gemini_reply = model.generate_content('こんにちは')
    print(gemini_reply.text)
    