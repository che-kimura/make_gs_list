# 2022/11/13
# GSInput.csvに区分と商品役務名（日本語）を入力し、それらをPlatPatから検索して出力する。
import openpyxl
import pprint
import os
from time import sleep
import csv

from django.conf import settings

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#from selene.api import *
#from selene.browsers import BrowserName

#ChromeDriverの自動バージョン適用
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#サーバ用にコメントアウト%%テストでは戻す%%
#import chromedriver_binary

def SearchGS(key_cls,key_item):
    count = ''
    results = []
    dtype_tmp = ''
    options = Options()
    options.add_argument('--headless')

    #[pythonanywereサーバ用]
    driver = webdriver.Chrome(options=options)
    #[テスト環境用]テスト環境だとchromeのバージョンが合わないので
    #クロムドライバーのパス
    #driver_path = os.path.dirname(os.path.abspath(__file__)) + '\\'+'chromedriver.exe'

    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    #PlatPatにアクセス
    driver.get("https://www.j-platpat.inpit.go.jp/t1201")
    i = 0
    #商品・役務名入力
    gs_textarea = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="t12_searchKeyword0"]'))
    )
    gs_textarea.clear()
    gs_textarea.send_keys(key_item)
    #区分
    gs_textarea2 = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="t12_searchCode0"]'))
    )
    gs_textarea2.clear()
    gs_textarea2.send_keys(key_cls)
    gs_textarea2.send_keys(Keys.RETURN)
    #検索結果が0件か否か
    try:
        errormsg = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="InputErrorMsg"]'))
            )
    except:
        count = driver.find_element(By.XPATH, '//*[@id="t1203_resultExpnlTrademarkServiceName_lblSearchHitCnt"]').text
    #最後までスクロールする
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
    try:
        #件数分要素を取得
        for num in range(int(count[1:-1])):
            #データ種別
            if len(driver.find_elements(
                By.XPATH, '//*[@id="t1203_resultExpnlTrademarkServiceName_basicMk_' + str(num) +'"]/span[1]')) > 0:
                dtype_tmp = '基'
            if len(driver.find_elements(
                By.XPATH, '//*[@id="t1203_resultExpnlTrademarkServiceName_nMk_' + str(num) +'"]/span[1]')) > 0:
                dtype_tmp = 'N'
            if len(driver.find_elements(
                By.XPATH, '//*[@id="t1203_resultExpnlTrademarkServiceName_tMk_' + str(num) +'"]/span[1]')) > 0:
                dtype_tmp = 'T'
            if len(driver.find_elements(
                By.XPATH, '//*[@id="t1203_resultExpnlTrademarkServiceName_appealMk_' + str(num) +'"]/span[1]')) > 0:
                dtype_tmp = '審'
            if len(driver.find_elements(
                By.XPATH, '//*[@id="t1203_resultExpnlTrademarkServiceName_mMk_' + str(num) +'"]/span[1]')) > 0:
                dtype_tmp = 'M'
            results.append({
                'cls':key_cls,
                'item':driver.find_element(
                    By.XPATH, '//*[@id="t1203_resultExpnlTrademarkServiceName_jpnGoodsServiceName_' + str(num) +'"]').text,
                'eng':driver.find_element(
                    By.XPATH, '//*[@id="t1203_resultExpnlTrademarkServiceName_engGoodsServiceName_' + str(num) +'"]').text,
                'grpcode':driver.find_element(
                    By.XPATH, '//*[@id="t1203_resultExpnlTrademarkServiceName_smlrGrpCd_' + str(num) +'"]').text,
                'dtype':dtype_tmp
            })
    except:
        print("エラーです。")
    #ブラウザ操作終了
    driver.close()
    #検索結果を含む辞書型の配列を返す
    return results

#PlatPatを開いて検索語を自動入力する
def SearchJP(cls, item):
    #検出件数初期化
    count = 0
    eng = ''
    grpcode = ''
    dtype = ''
    #[pythonanywereサーバ用]
    #options = Options()
    #options.add_argument('--headless')
    #driver = webdriver.Chrome(options=options)
    #[テスト環境]テスト環境だとchromeのバージョンが合わないので
    chrome_options = webdriver.ChromeOptions()
    chrome_options.set_capability("browserVersion", "109")
    chrome_options.set_capability("platformName", "Windows 10")
    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:8000/make_gs_list',
        options=chrome_options
    )
    
    driver.get("https://www.j-platpat.inpit.go.jp/t1201")
    print(driver.title)
    driver.quit()

    #クロムドライバーのパス
    #driver_path = os.path.dirname(os.path.abspath(__file__)) + '\\'+'chromedriver.exe'
    #print(driver_path)
    #driver = webdriver.Chrome(executable_path=driver_path, options=options)

    # options.add_argument('--disable-gpu')
    # options.add_argument('--disable-extensions')
    # options.add_argument('--proxy-server="direct://"')
    # options.add_argument('--proxy-bypass-list=*')
    # options.add_argument('--start-maximized')
    #ブラウザ操作
    # config.browser_name = BrowserName.CHROME
    # chrome_option = webdriver.ChromeOptions()
    #chrome_option.add_argument('--disable-gpu')
    #driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    #browser.set_driver(driver)

    #driver = Chrome(options=options)
    #eng = driver.title
    #grpcode = driver.title
    #dtype = driver.title
    #一次的にコメントアウト
    #要素を取得できるまで2秒待機
    sleep(2)
    i = 0
    # キーを指定して名前だけ出力。
    print('検索区分:' + cls)
    print('検索商品:' + item)
    #商品・役務名入力
    gs_textarea = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="t12_searchKeyword0"]'))
    )
    gs_textarea.clear()
    gs_textarea.send_keys(item)
    #区分
    gs_textarea2 = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="t12_searchCode0"]'))
    )
    gs_textarea2.clear()
    gs_textarea2.send_keys(cls)
    gs_textarea2.send_keys(Keys.RETURN)
    sleep(5)
    #検索結果が0件か否か
    try:
        errormsg = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="InputErrorMsg"]'))
            )
        #未検出レコード作成
        #items.append([gs['class'],gs['description'],'','',''])
    except:
        count = driver.find_element(By.XPATH, '//*[@id="t1203_resultExpnlTrademarkServiceName_lblSearchHitCnt"]').text
    #最後までスクロールする
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
    print("検索件数："+count)
    try:
        #件数分要素を取得
        for num in range(int(count[1:-1])):
            print('商品役務名：' + driver.find_element(
                By.XPATH, '//*[@id="t1203_resultExpnlTrademarkServiceName_jpnGoodsServiceName_' + str(num) +'"]').text)
            gs_jpn = driver.find_element(
                By.XPATH, '//*[@id="t1203_resultExpnlTrademarkServiceName_jpnGoodsServiceName_' + str(num) +'"]').text
            #商品役務が一致したら
            if gs_jpn == item:
                #商品役務(1件）
                # item.append(gs['class'])
                # item.append(gs['description'])
                eng = driver.find_element(
                    By.XPATH, '//*[@id="t1203_resultExpnlTrademarkServiceName_engGoodsServiceName_' + str(num) +'"]').text
                grpcode = driver.find_element(
                    By.XPATH, '//*[@id="t1203_resultExpnlTrademarkServiceName_smlrGrpCd_' + str(num) +'"]').text
                #データ種別
                if len(driver.find_elements(
                    By.XPATH, '//*[@id="t1203_resultExpnlTrademarkServiceName_basicMk_' + str(num) +'"]/span[1]')) > 0:
                    dtype = '基'
                if len(driver.find_elements(
                    By.XPATH, '//*[@id="t1203_resultExpnlTrademarkServiceName_nMk_' + str(num) +'"]/span[1]')) > 0:
                    dtype += 'N'
                if len(driver.find_elements(
                    By.XPATH, '//*[@id="t1203_resultExpnlTrademarkServiceName_tMk_' + str(num) +'"]/span[1]')) > 0:
                    dtype += 'T'
                if len(driver.find_elements(
                    By.XPATH, '//*[@id="t1203_resultExpnlTrademarkServiceName_appealMk_' + str(num) +'"]/span[1]')) > 0:
                    dtype += '審'
                if len(driver.find_elements(
                    By.XPATH, '//*[@id="t1203_resultExpnlTrademarkServiceName_mMk_' + str(num) +'"]/span[1]')) > 0:
                    dtype += 'M'
                # item.append(dtype)
                # items.append(item)
    except:
        print("エラーです。")
    print(eng)
    print(grpcode)
    print(dtype)
    #sleep(5)
    #ブラウザ操作終了
    driver.close()
    return eng, grpcode, dtype
    #ブラウザ操作終了
    #driver.close()


# #結果を出力する
# #出力一覧ファイル
# CSV_LST_FILE = os.path.dirname(os.path.abspath(__file__)) + '\\'+'GSList.csv'
# #出力ヘッダーを設定
# csv_header = ['区分','商品役務（日本語）','商品（英語）','類似群コード','データ種別']
# #出力
# with open(CSV_LST_FILE,'w',encoding='SJIS',newline='') as ofile:
#     writer = csv.writer(ofile, lineterminator='\n')
#     writer.writerow(csv_header)
#     writer.writerows(items)