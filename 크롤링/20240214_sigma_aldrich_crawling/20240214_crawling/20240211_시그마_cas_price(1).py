import requests
from bs4 import BeautifulSoup
import json
from urllib.error import HTTPError
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding= 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding= 'utf-8')
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
from tqdm import tqdm
from fake_useragent import UserAgent
ua = UserAgent()
header = {"User-Agent":ua.random}

from selenium import webdriver
from selenium.webdriver.common.by import By

f = open(r"C:\PythonWorkspace\LSJ\datafile\#20240212\20240212_cas.txt", 'r')

CAS = []
key_available_result = []

product_list = []
CASno = []
chemical_name = []
chemical_number = []
attributes_key = []
attributes_values = []
materialId = []
my_prices = []

sigma_url = ['sigma', 'sial', 'sigald', 'mm', 'aldrich']


while True:
    line = f.readline()
    if not line:break
    new_line = line.split("\t")
    CAS.append(new_line[0].strip())


#구동 순서: url 접속(가능여부 체크) > 제품번호 가져오는 특정 key 추출 > cas 별 조회되는 모든 제품번호 추출 > 제품번호를 통해 가장 저렴한 가격 추출
for cas in tqdm(CAS):
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
    if target_key in apolloState:
        key_available_result.append('available')
    else:
        key_available_result.append('unavailable')  # 없으면 break ->> 결과에 None으로 표기.

    product_list = []
    try: # key 사용이 가능한 경우에만
        if 'available' in key_available_result:
            keys_list = list(apolloState.keys())
            index_of_target_key = keys_list.index(target_key)  # 특정 키의 인덱스 찾기

            # 다음 키 가져오기(제품번호 가져올 수 있는 cas 별 특정 key)
            if index_of_target_key < len(keys_list) - 1:
                next_key = keys_list[index_of_target_key + 1]
                print(f"다음 키: {next_key}")

            # CAS 검색시 조회되는 모든 제품번호 수집
            for i in range(len(keys_list)):
                try:
                    key_elements = ['.images.', '.products.']
                    for elements in key_elements:
                        apolloState_key = apolloState[str(next_key) + str(elements) + str(i)]  # dict
                        productKey = apolloState_key['productKey']
                        # print(i, ":", productKey)
                        
                        product_list.append(productKey)

                except KeyError:
                    pass
    except:
        pass
        product_list.append("none")

    for cat_no in tqdm(product_list): #여기서부터 가격 crawling
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
                    IDs = list(set(IDs))  #제품번호 하나에 용량별 materialID를 list로 담기

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

                    driver = webdriver.Chrome('C:\\Users\\user\\Downloads\\chromedriver_win32\\chromedriver.exe',
                                                  options=options)

                    driver.get(url)
                    prices = []
                    for my_id in IDs: #용량별 금액 모두 가져오기
                        try:
                            if '.' in my_id:
                                temp = my_id.split('.')
                                my_id = '\.'.join(temp)
                                # print(my_id)
                            link = driver.find_element(By.CSS_SELECTOR,
                                                        '#P\&A-row-price-' + ai.upper() + '-' + my_id + ' > div > div > div')
                            price = link.text
                            prices.append(price)
                        except:
                                # print('bad!!!!: ', my_id)
                            print('##############################\n', my_id, '###########################\n')
                    driver.close()

                    prices = [float(p[1:].replace(',', '')) for p in prices]
                    prices.sort()
                    if len(prices) == 0:
                        my_price = 'None'
                    else:
                        my_price = round(prices[0])
                    my_prices.append(my_price)
                    print('#P\&A-row-price-' + ai.upper() + '-' + my_id + ' > div > div > div')

                    break

        except KeyError as E:
            my_prices.append('error')
            chemical_number.append('error')
            chemical_name.append('error')
        except HTTPError as e:
            my_prices.append('error')
            chemical_number.append('error')
            chemical_name.append('error')


sigma_cas_price = {'CAS': CAS, 'URLcheck': key_available_result, 'CasNo': CASno, 'chemical_name': chemical_name, 'CATno': chemical_number, 'price': my_prices}
sigma_result = pd.DataFrame(sigma_cas_price)
print(sigma_result)
# sigma_result.to_excel(excel_writer=r"C:\Users\user\PycharmProjects\ML_LSJ\dataset\20240206_연습결과.xlsx", index=None)