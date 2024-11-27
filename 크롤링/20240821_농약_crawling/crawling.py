import json
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from tqdm import tqdm
import pandas as pd
# user agent setting
ua = UserAgent()
header = {"User-Agent":ua.random}
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

url = 'https://psis.rda.go.kr/psis/saf/evl/chmstry/chmstryChartrLst.ps'
elem_url = 'https://psis.rda.go.kr/psis/saf/evl/chmstry/chmstryChartrDtl.ps'

keys = ['용도', '일반명(한글)', '일반명(영문)', 'CAS No', '화학명', '구조식', '용해도', '분자식', '비점', '분자량', '증기압', '외관', 'KowLogP', '융점', '밀도', '코드명', '코드설명', '계통명']
my_dict = {key:[] for key in keys}

for i in tqdm(range(1,61)):
    data = {'pageIndex':i, 'pageSize':10, 'sTchprductIrdntSn': None, 'sGnrINm': None, 'sCasrn:': None, 'pageUnit': 20, 'menuId':'PS00376'}
    response = requests.post(url, verify=False, data=data).content
    web_page = BeautifulSoup(response, 'html.parser')
    counts = len(web_page.select('#chmstryChartrVO > div.gridScroll > table > tbody > tr'))
    for count in tqdm(range(1, counts+1)):
        element = web_page.select_one(f'#chmstryChartrVO > div.gridScroll > table > tbody > tr:nth-child({count}) > td:nth-child(3) > a')
        onclick = element['onclick']
        element_id = int(onclick.split("'")[1])
        element_use = web_page.select_one(f'#chmstryChartrVO > div.gridScroll > table > tbody > tr:nth-child({count}) > td:nth-child(2)').text.strip()
        element_kor_name = web_page.select_one(f'#chmstryChartrVO > div.gridScroll > table > tbody > tr:nth-child({count}) > td:nth-child(3)').text.strip()
        element_eng_name = web_page.select_one(f'#chmstryChartrVO > div.gridScroll > table > tbody > tr:nth-child({count}) > td:nth-child(4)').text.strip()
        my_dict['용도'].append(element_use)
        my_dict['일반명(한글)'].append(element_kor_name)
        my_dict['일반명(영문)'].append(element_eng_name)
        elem_data = {'pageIndex':i, 'pageSize':10, 'sTchprductIrdntSn': element_id, 'sGnrINm': None, 'sCasrn:': None, 'pageUnit': 20, 'menuId':'PS00376'}
        elem_response = requests.post(elem_url, verify=False, data=elem_data).content
        elem_page = BeautifulSoup(elem_response, 'html.parser')
        chemical_info = elem_page.select('#innerCont > div')[0].find_all('div')  
        code_info = elem_page.select('#innerCont > div')[1].find_all('div')  
        info = chemical_info + code_info
        
        for j in range(0, len(info), 2):
            col = info[j].text.strip()
            val = info[j+1].text.strip().replace('\n', ' ').replace('\r', '')
            my_dict[col].append(val)
    print(i, len(my_dict['용도']), len(my_dict['계통명']))
    
    pd.DataFrame(my_dict).to_csv(r'C:\Users\user\Desktop\1\Modeling\0. utils\크롤링\20240821_농약_crawling\output2.csv', encoding = 'utf-8-sig', index= False)