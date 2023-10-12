import sys
sys.path.append('/usr/local/lib/python3.9/site-packages')
import os

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings

import openpyxl
import pathlib

from .forms import InForm
from .models import GoodsService
from .defs import Search, Translate, WriteExcel
from .platpat import SearchGS
from django.db.models import Q

def index(request):
    params = {
        'title':'GOODS & SERVICE',
        'form':InForm(),
        'results':[],
        'honyaku':'',
        'nofind':[],
        'lang':'',
        'ids':''
    }
    if (request.method == 'POST'):
        inp_text = request.POST.get("input")
        #inp_textを関数に渡して、検索結果resultsを取得する
        params['results'], params['ids'] = Search(inp_text)
        #print(params['results'])
        #検索に引っかからない商品を取得
        params['honyaku'], params['nofind'], params['lang'] = Translate(inp_text)
        params['form'] = InForm(request.POST)
    return render(request, 'make_gs_list/index.html', params)

def download(request):
    params = {
        'title':'GOODS & SERVICE',
        'form':InForm(),
        'results':[],
        'honyaku':'',
        'nofind':''
    }
    if request.method =='POST':
        #隠しデータ（商品役務のIDリスト）を取得して、EXCELファイルを作成
        WriteExcel(request.POST.getlist("id"))
        #作成したExcelにアクセス
        wb = openpyxl.load_workbook(str(settings.BASE_DIR) + '/media/Goods_Service_list.xlsx')
        ws = wb.active
        #responseにExcelファイルを含ませる
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s' % 'Goods_Service_list.xlsx'
        wb.save(response)
        return response
    else:
        return render(request, 'make_gs_list/index.html', params)

#J-PlatPatで検索して情報を取得
def nofind(request):
    #Dictionary型
    elements = {
        'title':'SEARCH RESULT',
        'gs':[]
        }
    gs_tmp = []
    key_item = []
    if (request.method == 'POST'):
        #区分と検索する商品役務名を取得
        key_cls = request.POST.get("cls")
        key_item = request.POST.get("item")
        #検索で取得した商品役務を追加
        gs_tmp = SearchGS(key_cls,key_item)
        elements['gs'] = gs_tmp
    return render(request, 'make_gs_list/gslist.html', elements)
# ajaxでurl指定したメソッド
def call_write_data(request):
    if request.method == 'GET':
        # write_data.pyのwrite_csv()メソッドを呼び出す。
        # ajaxで送信したデータのうち"input_data"を指定して取得する。
        write_data.write_csv(request.GET.get("input_data"))
        return HttpResponse()

def test_page(request):
    return render(request, 'make_gs_list/test.html')

def test(request):
    if request.method == 'GET':
        # write_data.pyのwrite_csv()メソッドを呼び出す。
        # ajaxで送信したデータのうち"input_data"を指定して取得する。
        platpat.test(request.GET.get("input_data"))
        return HttpResponse()


