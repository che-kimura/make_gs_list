from django.shortcuts import render
from django.http import HttpResponse
from .forms import InForm
from .models import GoodsService
from .defs import Search, Translate

def index(request):
    params = {
        'title':'GOODS & SERVICE',
        'form':InForm(),
        'results':[],
        'honyaku':'',
        'nofind':''
    }
    if (request.method == 'POST'):
        inp_text = request.POST.get('input')
        #inp_textを関数に渡して、検索結果resultsを取得する
        params['results'] = Search(inp_text)
        #検索に引っかからない商品を取得
        params['honyaku'], params['nofind'] = Translate(inp_text)
        params['form'] = InForm(request.POST)
    return render(request, 'make_gs_list/index.html', params)
    #results = GoodsService.objects.filter(eng=q_word)
    

