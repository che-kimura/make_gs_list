from .models import GoodsService
from django.db.models import Q
from django.conf import settings

import re
import openpyxl
import pathlib

def Search(inp_text):
    results = []
    ids = []
    sorted_results = []
    condition = Q()
    condition2 = Q()
    #頭文字から英語か日本語か判断する
    #英語→日本語
    if re.fullmatch('[a-zA-Z]+',inp_text[0:1]):
        l_gs = inp_text.split('; ')
        #検索する
        #1アイテムずつ検索する条件をOrでつなげる
        for gs in l_gs:
            condition = Q(eng__iexact=gs)
            #検索条件をORでつなげる
            condition2 = condition2 | condition
        #results = GoodsService.objects.filter(condition2).order_by('cls','ruijigun')
        results = GoodsService.objects.filter(condition2)
        #入力順にする
        for gs2 in l_gs:
            for item in results:
                if item.eng == gs2:
                    sorted_results.append(item)
                    ids.append(item.id)
                    continue
    #日本語→英語
    else:
        l_gs = inp_text.split('，')
        print(l_gs)
        #検索する
        #1アイテムずつ検索する条件をOrでつなげる
        for gs in l_gs:
            condition = Q(jpn__iexact=gs)
            condition2 = condition2 | condition
        #results = GoodsService.objects.filter(condition2).order_by('cls','ruijigun')
        results = GoodsService.objects.filter(condition2)
        #入力順にする
        for gs2 in l_gs:
            for item in results:
                if item.jpn == gs2:
                    sorted_results.append(item)
                    ids.append(item.id)
                    continue
    # for item in results:
    #     ids.append(item.id)
    #     sorted_results.append(item) 
    #return results, ids
    return sorted_results,ids

#商品役務をそのまま翻訳する
def Translate(inp_text):
    #見つからない商品役務
    nofind = []
    #翻訳
    honyaku = ''
    #英日フラグ
    lang = ''
    #頭文字から英語か日本語か判断する
    if re.fullmatch('[a-zA-Z]+',inp_text[0:1]):
        #英語→日本語の場合、セミコロンを区切り文字としてリスト化
        l_gs = inp_text.split('; ')
        #出力言語を日本語にする
        lang = 'EN'
        #検索する
        for gs in l_gs:
            if GoodsService.objects.filter(eng__iexact=gs).count() == 1:
                for gs2 in GoodsService.objects.filter(eng__iexact=gs):
                    honyaku += gs2.jpn + '，'
            elif GoodsService.objects.filter(eng__iexact=gs).count() > 1:
                honyaku += '<font class="text-danger">［複数候補：' + gs + '］'
                for gs2 in GoodsService.objects.filter(eng__iexact=gs):
                    honyaku += gs2.jpn + '/'
                honyaku = honyaku[:-1] + '</font>， '
            elif GoodsService.objects.filter(eng__iexact=gs).count() == 0:
                honyaku += '<font class="text-danger">［不明：' + gs + ']</font>' + '，'
                nofind.append(gs)
        #末尾のコンマ、コロンとる
        honyaku = honyaku[0:-1]
    else:
        #日本語→英語の場合
        #出力言語を英語にする
        lang = 'JP'
        l_gs = inp_text.split('，')
        #検索する
        for gs in l_gs:
            if GoodsService.objects.filter(jpn__iexact=gs).count() == 1:
                for gs2 in GoodsService.objects.filter(jpn__iexact=gs):
                    honyaku += gs2.eng + '; '
            elif GoodsService.objects.filter(jpn__iexact=gs).count() > 1:
                honyaku += '<font class="text-danger">［複数候補：' + gs + '］'
                for gs2 in GoodsService.objects.filter(jpn__iexact=gs):
                    honyaku += gs2.eng + '/'
                honyaku = honyaku[:-1] + '</font>; '
            elif GoodsService.objects.filter(jpn__iexact=gs).count() == 0:
                honyaku += '<font class="text-danger">［不明：' + gs + '］</font>' + '; '
                nofind.append(gs)
        #末尾のコンマ、コロンとる
        honyaku = honyaku[0:-2]
        #print(nofind)
    return honyaku, nofind, lang

#商品役務のIDを取得してExcelに出力する
def WriteExcel(id_list):
    results = []
    condition_we = Q()
    condition2_we = Q()
    for id in id_list:
        condition_we = Q(id__iexact=id)
        condition2_we = condition2_we | condition_we
    results = GoodsService.objects.filter(condition2_we).order_by('cls','ruijigun')
    
    #結果を出力する
    #ブックを作成
    wb = openpyxl.Workbook()
    #シートを選択
    ws = wb['Sheet']
    #見出しを入力
    #出力ヘッダーを設定
    ws.append(['区分','商品役務（日本語）','商品（英語）','類似群コード','データ種別'])
    # # #値を入力
    for item in results:
        ws.append([item.cls,item.jpn,item.eng,item.ruijigun,item.nice])
    #所定の場所に保存
    wb.save(str(settings.BASE_DIR) + '/media/Goods_Service_list.xlsx')

""" #検索に引っかからない商品役務を文字列で返す
def CheckNoFind(inp_text):
    results = ''
    #頭文字から英語か日本語か判断する
    if re.fullmatch('[a-zA-Z]+',inp_text[0:1]):
        l_gs = inp_text.split('; ')
        #検索する
        for gs in l_gs:
            if GoodsService.objects.filter(eng=gs).exists() == 0:
                results += gs + '; '
    else:
        l_gs = inp_text.split('，')
        #検索する
        for gs in l_gs:
            if GoodsService.objects.filter(jpn=gs).exists() == 0:
                results += gs + '，'
    results = results[0:-1]
    return results """