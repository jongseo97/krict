import requests
from bs4 import BeautifulSoup
import json
from urllib.error import HTTPError
import sys
import io

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
from tqdm import tqdm
from fake_useragent import UserAgent
ua = UserAgent()
header = {"User-Agent":ua.random}

from selenium import webdriver
from selenium.webdriver.common.by import By

CATno = []
CASno = []
chemical_name = []
chemical_number = []
attributes_key = []
attributes_values = []
materialId = []
my_prices = []

#제품번호 읽을 파일 open
f = open("all_second.txt", 'r')


# 첫 줄부터 한 줄씩 읽고, 다 읽으면 break
while True:
    line = f.readline()
    if not line:break
    new_line = line.split("\t")
    CATno.append(new_line[0].strip())

print("read CAT_no file")

sigma_url = ['sigma', 'sial', 'sigald', 'mm', 'aldrich']

for cat_no in tqdm(CATno):
    print(str("input CAT number: ") + str(cat_no).strip())
    try:
        for ai in sigma_url:
            url = "https://www.sigmaaldrich.com/KR/ko/product/" + str(ai) + '/' + str(cat_no).strip()
            print(url)
            r = requests.get(url, verify=False, headers=header, timeout=1000)
            r.encoding = 'utf-8'
            html = r.text
            bs4 = BeautifulSoup(html, 'html.parser')
            result = bs4.select_one('#__NEXT_DATA__')
            result = result.text
            dict_result = json.loads(result)

            props = dict_result['props']
            pageProps = props['pageProps']
            if 'data' in pageProps:
                data = pageProps['data']
                getProductDetails = data['getProductDetail']
                productname = getProductDetails['name']
                attributes = getProductDetails['attributes']
                materialIds = getProductDetails['materialIds']

                productnumber = getProductDetails['productNumber']
                casnumber = getProductDetails['casNumber']
                attributes_value = []  # list 초기화
                for bi in attributes:
                    attributes_key.append(bi['key'])
                    attributes_values.append(bi['values'])

                dictionary = dict(zip(attributes_key, attributes_values))

                # list에 담자
                chemical_name.append(productname)
                chemical_number.append(productnumber)
                CASno.append(casnumber)

                IDs = materialIds
                IDs = list(set(IDs))

                options = webdriver.ChromeOptions()
                options.add_argument('ignore-certificate-errors')
                options.add_argument(
                    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
                options.add_argument('--headless=new')
                options.add_argument("window-size=1920x1080")
                options.add_argument("disable-infobars")
                options.add_argument("--disable-extensions")
                options.add_argument('--blink-settings=imagesEnabled=false')
                options.add_argument("disable-gpu")

                driver = webdriver.Chrome(options=options)

                driver.get(url)
                prices = []
                for my_id in IDs:
                    try:
                        if '.' in my_id:
                            temp = my_id.split('.')
                            my_id = '\.'.join(temp)
                        #print(my_id)
                        link = driver.find_element(By.CSS_SELECTOR,
                                                   '#P\&A-row-price-' + ai.upper() + '-' + my_id + ' > div > div > div')
                        price = link.text
                        prices.append(price)
                    except:
                        #print('bad!!!!: ', my_id)
                        #print('##############################\n',my_id,'###########################\n')
                        pass
                driver.close()

                prices = [float(p[1:].replace(',', '')) for p in prices]
                prices.sort()
                if len(prices) == 0:
                    my_price = 'None'
                    print('bug: ', cat_no)
                else:
                    my_price = round(prices[0])
                    print('good: ', cat_no, my_price)
                
                my_prices.append(my_price)
                print('#P\&A-row-price-' + ai.upper() + '-' + my_id + ' > div > div > div')

                break

    except KeyError as E:
        chemical_name.append("none")
        chemical_number.append("none")
        CASno.append("none")
    except HTTPError as e:
        chemical_name.append("none")
        chemical_number.append("none")
        CASno.append("none")
    except TimeoutError:
        chemical_name.append("none")
        chemical_number.append("none")
        CASno.append("none")


#엑셀에 저장
print(my_prices)
result_naturalproduct = {'물질명': chemical_name, '제품번호': chemical_number, 'CASno': CASno, '가격': my_prices}
print(result_naturalproduct)
result_naturalproduct = pd.DataFrame(result_naturalproduct)
result_naturalproduct.to_excel(excel_writer="greenprice3.xlsx")


#%%

import pandas as pd

dt = pd.read_excel('greenprice2.xlsx')
dt2 = pd.read_excel('greenprice3.xlsx')

for i, i_row in dt2.iterrows():
    i_price = i_row['가격']
    i_id = i_row['제품번호']
   
    idx = dt.index[dt['제품번호']==i_id][0]
    dt.loc[idx,'가격'] = i_price

dt.to_excel('greenprice_all.xlsx', index=False, na_rep='None')