from django.conf import settings

import re
import openpyxl
import pathlib

def WriteExcel(items):
    #データをリストにする
    # gslist = []
    # for item in items:
    #     gslist.append([item.cls,item.jpn,item.eng,item.ruijigun,item.nice])

    #結果を出力する
    #ブックを作成
    wb = open.load_workbook()
    #シートを選択
    ws = wb['Sheet']
    #見出しを入力
    #出力ヘッダーを設定
    ws.append(['区分','商品役務（日本語）','商品（英語）','類似群コード','データ種別'])
    #値を入力
    for item in items:
        ws.append([item.cls,item.jpn,item.eng,item.ruijigun,item.nice])
    #所定の場所に保存
    wb.save(str(settings.BASE_DIR) + '/media/Goods_Service_list.xlsx')

    # EXCEL_LST_FILE = os.path.dirnamepython(os.path.abspath(__file__)) + '\\'+'GSList.csv'
    # #出力ヘッダーを設定
    # csv_header = ['区分','商品役務（日本語）','商品（英語）','類似群コード','データ種別']
    
    # with open(CSV_LST_FILE,'w',encoding='SJIS',newline='') as ofile:
    #     writer = csv.writer(ofile, lineterminator='\n')
    #     writer.writerow(csv_header)
    #     writer.writerows(gslist)
