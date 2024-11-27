import requests
from bs4 import BeautifulSoup
import json
from urllib.error import HTTPError

# sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding= 'utf-8')
# sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding= 'utf-8')
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
from tqdm import tqdm
from fake_useragent import UserAgent
ua = UserAgent()

from lxml import etree

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

f = open(r"C:\Users\user\Desktop\1\Modeling\0. utils\20240214_sigma_aldrich_crawling\20240214_crawling\20240214_금도금_CAS.txt", 'r')

CAS = []

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

sigma_url = ['aldrich', 'sial', 'sigma', 'supelco', 'mm', 'usp', 'sigald']

while True:
    line = f.readline()
    if not line:break
    new_line = line.split("\t")
    CAS.append(new_line[0].strip())

CAS1 = CAS[:1000]
CAS2 = CAS[1000:2000]
CAS3 = CAS[2000:3000]
CAS4 = CAS[3000:4000]
CAS5 = CAS[4000:5000]
CAS6 = CAS[5000:6000]
CAS7 = CAS[6000:]
CAS_zip = [CAS1,CAS2,CAS3,CAS4,CAS5,CAS6,CAS7]
i = 0
#구동 순서: url 접속(가능여부 체크) > 제품번호 가져오는 특정 key 추출 > cas 별 조회되는 모든 제품번호 추출 > 제품번호를 통해 가장 저렴한 가격 추출
CAS_zip = [['6381-92-6']]
for CAS in CAS_zip:
    key_available_result = []

    product_list = []
    CASno = []
    chemical_name = []
    chemical_number = []
    attributes_key = []
    attributes_values = []
    materialId = []
    my_prices = []
    my_sizes = []
    
    for cas in tqdm(CAS):       
        header = {"User-Agent":ua.random}
        url = "https://www.sigmaaldrich.com/KR/ko/search/" + str(cas).strip() + "?focus=products&page=1&perpage=30&sort=relevance&term=" + str(cas).strip() + "&type=product"
        r = requests.get(url, verify=False, headers=header, timeout=1000)
        r.encoding = 'utf-8'
        html = r.text
        bs4 = BeautifulSoup(html, 'html.parser')
        result = bs4.select_one('#__NEXT_DATA__')
        result = result.text
        dict_result = json.loads(result)
        # print(dict_result)
        sigma = dict_result.keys()
        # print(sigma)
        # print(dict_result)
        props = dict_result['props']  # dict
        apolloState = props['apolloState']
    
        target_key = '$ROOT_QUERY.getProductSearchResults({"input":{"facets":[],"group":"substance","pagination":{"page":1},"searchTerm":"' + str(cas).strip() + '","sort":"relevance","type":"PRODUCT"}})'
    
        # CAS 조회 available check
        if apolloState[target_key]['items'] != []:
            key_available_result.append('available')
        else:
            key_available_result.append('unavailable')  # 없으면 break ->> 결과에 None으로 표기.
            chemical_number.append('unavailable')
            my_prices.append('unavailable')
            my_sizes.append('unavailable')
            continue
    
        key_list = list(set([a for a in apolloState.keys() if '.products.' in a]))
        key_list = [key for key in key_list if len(key)==43]
        product_codes = list(set([key.split('.')[0] for key in key_list]))
        available_codes = [code for code in product_codes if apolloState[code]['casNumber'] == cas]
        
        new_key_list = []
        for code in available_codes:
            for key in key_list:
                if code in key:
                    new_key_list.append(key)
    
        IDs = []
        for key in new_key_list:
            #product_id = apolloState[key]['materialIds']['json']
            product_id = apolloState[key]['productKey']
            if product_id != None:
                print('\n', key, product_id)
                IDs.append(product_id)
                
        print(1)
                
        
        options = webdriver.ChromeOptions()
        # options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
        options.add_argument('ignore-certificate-errors')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        options.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        #user_agent = UserAgent().random
        #options.add_argument(f'user-agent={user_agent}')
        options.add_argument('--headless=new')
        options.add_argument("window-size=1920x1080")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("disable-gpu")
        driver = webdriver.Chrome(options=options)
        
        ID_to_price = dict()
        size_to_price = dict()
        for ID in IDs:
            bugs = 0 
            for sigma in sigma_url:
                try:
                    print('\n', ID, sigma, ' start!')
                    url = "https://www.sigmaaldrich.com/KR/ko/product/" + str(sigma) + '/' + str(ID).strip()
                    # r = requests.get(url, verify=False, headers=header, timeout=1000)
                    # r.encoding = 'utf-8'
                    # html = r.text
                    # bs4 = BeautifulSoup(html, 'html.parser')
                    # dom = etree.HTML(str(bs4))
                    # q = dom.xpath('//*[@id="prodductDetailGrid"]')[0].text
                    # if dom.xpath('//*[@id="prodductDetailGrid"]/div[1]/div/div[2]/div/div[3]/div[1]/p[2]') == []:
                    #     continue
                    # assert False

                    driver.get(url)
                    # 잠시대기
                    driver.implicitly_wait(2)
                    
                    # 이싱한 주소면 패스
                    error = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div/div/div[1]')
                    q = error.text
                    if q == '제품을 찾을 수 없음':
                        continue
                    
                    # 맞는 주소면 열릴때까지 존버
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="prodductDetailGrid"]/div[1]/div/div[2]/div/div[5]/div[1]/p[2]'))
                        )
                    time.sleep(0.5)
                    link_size = driver.find_element(By.XPATH, '//*[@id="prodductDetailGrid"]/div[1]/div/div[2]/div/div[5]/div[1]/p[1]/span')
                    size = link_size.text
                    link_price = driver.find_element(By.XPATH, '//*[@id="prodductDetailGrid"]/div[1]/div/div[2]/div/div[5]/div[1]/p[2]')
                                                                
                    price = link_price.text
                    price = round(float(price[1:].replace(',','')))
                    
                    ID_to_price[ID] = price
                    print(ID, price)
                    size_to_price[size] = price
                    break
                except:
                    bugs += 1
            if bugs == len(sigma_url):
                print('\n######',ID,'######\n')
                driver.delete_all_cookies()
        if IDs==[]:
            final_ID = 'None'
            final_price = 'None'
            final_size = 'None'
        
        elif len(ID_to_price) == 0:
            final_ID = ID
            final_price = 'None'
            final_size = 'None'
        else:
            ID_price = sorted(ID_to_price.items(), key = lambda item: item[1])
            size_to_price = sorted(size_to_price.items(), key = lambda item: item[1])
            final_ID = ID_price[0][0]
            final_size = size_to_price[0][0]
            final_price = ID_price[0][1]
        
        chemical_number.append(final_ID)
        my_sizes.append(final_size)
        my_prices.append(final_price)
        
    title = 'results' + str(i) + '.xlsx'
    sigma_cas_price = {'CAS': CAS[:206], 'url_check': key_available_result, 'CATno': chemical_number, 'volume': my_sizes, 'price': my_prices}
    sigma_result = pd.DataFrame(sigma_cas_price)
    print(sigma_result)
    sigma_result.to_excel(excel_writer=title, index=None)
    
    i += 1
