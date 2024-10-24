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

with open('dic.txt', 'r', encoding='utf-8') as f:
    dic_content = f.read()

# 軽量なウェブアプリケーションフレームワーク:Flask
app = Flask(__name__)

GEMINI_API_URL = "https://api.gemini.com/v1/chat" 


GEMINI_API_KEY = ("AIzaSyCkOsYaHDXylTcu21dTE9hQZ6AnZ11Lr4A")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')
default_initial_prompt = f"{dic_content}"

if __name__ == "__main__":
    print("起動しました\n")
    while(1):
      message = input()
      if(message == 'q'):
        break
      gemini_reply = model.generate_content(default_initial_prompt + message)
      print(gemini_reply.text.rstrip())
      print("")
    