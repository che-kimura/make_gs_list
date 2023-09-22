# 2022/11/13
# GSInput.csvに区分と商品役務名（日本語）を入力し、それらをPlatPatから検索して出力する。
import openpyxl
import pprint
import os
from time import sleep

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from selene.api import *
from selene.browsers import BrowserName
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# #出力用商品役務リスト
# items = []
# #入力ファイル
# CSV_IPT_FILE = os.path.dirname(os.path.abspath(__file__)) + '\\'+'GSInput.csv'
# #ヘッダー
# csv_input_header = ['class','description']
# #入力CSVから検索語を読み込む
# with open(CSV_IPT_FILE, encoding='SJIS', newline='') as f:
#     reader = csv.DictReader(f, csv_input_header)

def SearchJP(cls, item):
    #検出件数初期化
    count = 0
    eng = ''
    grpcode = ''
    dtype = ''
    #options = ChromeOptions()
    # Headless Chromeをあらゆる環境で起動させるオプション
    options = Options()
    options.add_argument('--headless')
    #クロムドライバーのパス
    driver_path = os.path.dirname(os.path.abspath(__file__)) + '\\'+'chromedriver.exe'
    print(driver_path)
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
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    #browser.set_driver(driver)

    #driver = Chrome(options=options)
    driver.get("https://www.j-platpat.inpit.go.jp/t1201")
    #要素を取得できるまで2秒待機
    sleep(2)
    i = 0
    # キーを指定して名前だけ出力。
    #for gs in reader:
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