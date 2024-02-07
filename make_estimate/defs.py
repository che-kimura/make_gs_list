from .models import GoodsService
from django.db.models import Q
from django.conf import settings

import re
import openpyxl
import pathlib

"""
yahooファイナンスから為替レートを取得する。1通貨単位の円換算を返す
"""
import requests
from bs4 import BeautifulSoup
import datetime

def cal_exchange_rate(code):
    #code = 'USD'
    #スクレイピング対象とするサイトのURL
    url ='https://www.google.com/finance/quote/'+code+'-JPY'

    #レスポンス情報をrequestsモジュールのgetメソッドで取得
    res = requests.get(url)

    #BeautifulSoupに引数として、レスポンス情報のテキストを渡す
    #第2引数には解析のためのhtml.parserをセット
    soup = BeautifulSoup(res.text,'html.parser')

    print(soup.find('title').text)
    now = datetime.datetime.now()
    now_19 = "{0.year}年{0.month}月{0.day}日{0.hour}時{0.minute}分".format(now)

    #サイトからhtmlを取得
    soup = BeautifulSoup(res.text, 'html.parser')
    #為替レートを取得
    yen = soup.find('div', class_='YMlKec fxKbKc').text
    #print(yen)

    return yen

#見積り（Excel）をテンプレートから作成する
def MakeEstimate():
    #必要な値を取得する
    #テンプレートを開く
    #シートを選択
    ws = wb['Sheet']
    #値を入力する
    #別名で保存する
    #所定の場所に保存
    wb.save(str(settings.BASE_DIR) + '/media/' + fname + '.xlsx')