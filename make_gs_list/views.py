from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

import openpyxl
import pathlib

from .forms import InForm
from .models import GoodsService
from .defs import Search, Translate, WriteExcel

def index(request):
    params = {
        'title':'GOODS & SERVICE',
        'form':InForm(),
        'results':[],
        'honyaku':'',
        'nofind':[],
        'ids':''
    }
    if (request.method == 'POST'):
        inp_text = request.POST.get("input")
        #inp_textを関数に渡して、検索結果resultsを取得する
        params['results'], params['ids'] = Search(inp_text)
        #検索に引っかからない商品を取得
        params['honyaku'], params['nofind'] = Translate(inp_text)
        params['form'] = InForm(request.POST)
        #print(params['nofind'])    
    return render(request, 'make_gs_list/index.html', params)
    #results = GoodsService.objects.filter(eng=q_word)

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

def nofind(request):
    params = {
        'title':'GOODS & SERVICE',
        'form':InForm(),
        'results':[],
        'honyaku':'',
        'nofind':''
    }
    if request.method =='POST':
        if "search" in request.POST:
            #PlatPatを検索
            print("search")
        elif "add" in request.POST:
            #そのレコードを一覧に追加する
            print("add")
        return response
    else:
        return render(request, 'make_gs_list/index.html', params)


