from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings

from .forms import InForm
from .models import EstimateInfo
from .models import Country
from django.conf import settings

def index(request):
    params = {
        'title':'MAKE ESTIMATE',
        'form':InForm(),
        #'results':'',
        'mode': 'ini',
        'countries_asia':[],
        'countries_namerica':[],
        'countries_samerica':[],
        'countries_oceania':[],
        'countries_europe':[],
        'countries_africa':[],
    }
    if (request.method == 'POST'):
        params['form'] = InForm(request.POST)
        #押下されたボタンで入力画面を変える（モードを変える）
        if 'btn_mp' in request.POST:
            params['mode'] = 'mp'
            #加盟国リストを取得
            params['countries_asia'] = Country.objects.filter(area='1').order_by('code')
            params['countries_namerica'] = Country.objects.filter(area='2').order_by('code')
            params['countries_samerica'] = Country.objects.filter(area='3').order_by('code')
            params['countries_oceania'] = Country.objects.filter(area='4').order_by('code')
            params['countries_europe'] = Country.objects.filter(area='5').order_by('code')
            params['countries_me'] = Country.objects.filter(area='6').order_by('code')
            params['countries_africa'] = Country.objects.filter(area='7').order_by('code')
        if 'btn_ind' in request.POST:
            params['mode'] = 'ind'
    return render(request, 'make_estimate/index.html', params)

#MP見積作成を押されたときの処理
def estimate_mp(request):
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