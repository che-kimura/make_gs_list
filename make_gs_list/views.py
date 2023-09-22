import sys
sys.path.append('/usr/local/lib/python3.9/site-packages')

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

import openpyxl
import pathlib

from .forms import InForm
from .models import GoodsService
from .defs import Search, Translate, WriteExcel
#from .platpat import SearchJP
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
        print(params['results'])
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

def nofind(request):
    params = {
        'title':'GOODS & SERVICE',
        'form':InForm(),
        'results':[],
        'cls':'',
        'item':'',
        'eng':'',
        'grpcode':'',
        'dtype':''
    }
    if (request.method == 'POST'):
        #区分と検索する商品役務名を取得
        cls = request.POST.get("cls")
        item = request.POST.get("item")
        params['eng'], params['grpcode'], params['dtype'] = SearchJP(cls,item)
        params['cls'] = cls
        params['jpn'] = item
        #params['item'] = item
        #フォームをそのまま引き継ぐ
        params['form'] = InForm(request.POST)
        #検索済みの商品役務のIDを取得
        # ids = []
        # ids = request.POST.getlist("id")
        # print(ids)
        # results = []
        # condition_we = Q()
        # condition2_we = Q()
        # for id in ids:
        #     condition_we = Q(id__iexact=id)
        #     condition2_we = condition2_we | condition_we
        # #params['results'] = GoodsService.objects.filter(condition2_we)
        # results = GoodsService.objects.filter(condition2_we)
        # #辞書型の配列に変換
        # results_list = list(results.values())
        #検索で取得した商品役務を追加
        # eng = ''
        # grpcode = ''
        # dtype = ''
        # eng, grpcode, dtype = SearchJP(cls,item)
        # results_list.append({'cls':cls, 'eng':eng, 'jpn': item, 'ruijigun':grpcode})
        # params['results'] = results_list
    return render(request, 'make_gs_list/result.html', params)


