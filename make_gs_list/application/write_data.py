# coding:utf-8
import os
import csv
from django.conf import settings

# htmlからのデータをcsvファイルに記録
def write_csv(data):
    datas = [data]
    with open(str(settings.BASE_DIR) + '/media/'+'data.csv','a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(datas)