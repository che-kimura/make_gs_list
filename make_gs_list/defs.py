from .models import GoodsService
from django.db.models import Q
import re

def Search(inp_text):
    results = []
    condition = Q()
    condition2 = Q()
    #頭文字から英語か日本語か判断する
    #sql = 'select * from make_gs_list_goodsservice where '
    #英語→日本語
    if re.fullmatch('[a-zA-Z]+',inp_text[0:1]):
        l_gs = inp_text.split('; ')
        #検索する
        #1アイテムずつ検索する条件をOrでつなげる
        for gs in l_gs:
            condition = Q(eng__iexact=gs)
            condition2 = condition2 | condition
        results = GoodsService.objects.filter(condition2).order_by('cls','ruijigun')
    #日本語→英語
    else:
        l_gs = inp_text.split('，')
        #検索する
        #1アイテムずつ検索する条件をOrでつなげる
        for gs in l_gs:
            condition = Q(jpn__iexact=gs)
            condition2 = condition2 | condition
        results = GoodsService.objects.filter(condition2).order_by('cls','ruijigun')
    return results

#検索に引っかからない商品役務を文字列で返す
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
    return results

#商品役務をそのまま翻訳する
def Translate(inp_text):
    #見つからない商品役務
    nofind = ''
    #翻訳
    honyaku = ''
     #頭文字から英語か日本語か判断する
    if re.fullmatch('[a-zA-Z]+',inp_text[0:1]):
        #英語→日本語の場合
        l_gs = inp_text.split('; ')
        #検索する
        for gs in l_gs:
            if GoodsService.objects.filter(eng__iexact=gs).count() == 1:
                for gs2 in GoodsService.objects.filter(eng__iexact=gs):
                    honyaku += gs2.jpn + '，'
            elif GoodsService.objects.filter(eng__iexact=gs).count() > 1:
                for gs2 in GoodsService.objects.filter(eng__iexact=gs):
                    honyaku += '!!候補が複数あります!!（' + gs2.jpn + '），'
            elif GoodsService.objects.filter(eng__iexact=gs).count() == 0:
                honyaku += '!!見つかりません!!（' + gs + '）' + '，'
                nofind += gs + '，'
        #末尾のコンマ、コロンとる
        honyaku = honyaku[0:-1]
    else:
        #日本語→英語の場合
        l_gs = inp_text.split('，')
        #検索する
        for gs in l_gs:
            if GoodsService.objects.filter(jpn__iexact=gs).count() == 1:
                for gs2 in GoodsService.objects.filter(jpn__iexact=gs):
                    honyaku += gs2.eng + '; '
            elif GoodsService.objects.filter(jpn__iexact=gs).count() > 1:
                for gs2 in GoodsService.objects.filter(jpn__iexact=gs):
                    honyaku += '!!候補が複数あります!!（' + gs2.eng + '）; '
            elif GoodsService.objects.filter(jpn__iexact=gs).count() == 0:
                honyaku += '!!見つかりません!!（' + gs + '）' + '; '
                nofind += gs + '，'
        #末尾のコンマ、コロンとる
        honyaku = honyaku[0:-2]
    nofind = nofind[0:-1]
    return honyaku, nofind
