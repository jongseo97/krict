# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 16:23:52 2023

@author: user
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
from tqdm import tqdm

ua = UserAgent(use_cache_server=True)
header = {"User-Agent":ua.random}
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

dt = pd.read_excel(r'C:\Users\user\Desktop\1\Modeling\16. THR 단일물질\input data\20240223_THR_PC10_SMILES.xlsx')
cas_list = dt['CAS No']
cas_list = [cas.strip() for cas in cas_list]
cas_list = list(set(cas_list))
print('Unique CAS number : %d'%len(cas_list))

cnt = 0
cid_list = []
i=0
bugs = []
for cas in tqdm(cas_list):
    url = "http://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/" + cas + "/cids/txt"
    r = requests.get(url, verify=False, headers=header, timeout=100)
    r.encoding = 'utf-8'
    html = r.text
    bs4 = BeautifulSoup(html, 'html.parser')
    cids = bs4.text.split()
    
    if 'PUGREST' in bs4.text:
        url = "http://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/name/" + cas + "/cids/txt"
        r = requests.get(url, verify=False, headers=header, timeout=100)
        r.encoding = 'utf-8'
        html = r.text
        bs4 = BeautifulSoup(html, 'html.parser')
        cids = bs4.text.split()
        cnt += 1
        
        if 'PUGREST' in bs4.text:
            print(cas)
            cids = 'None'
            bugs.append(cas)

    cid_list.append(cids)
    i+=1
    if i%10 ==0:
        print(cid_list)
        print(cnt)
    
    #print(cids)
    
#result = bs4.select_one('#__NEXT_DATA__')
#result = result.text

cas_cid = pd.DataFrame({'CAS' :cas_list, 'CID' : cid_list})

drop_list = []
for i, row in cas_cid.iterrows():
    if ',' in row['CAS']:
        drop_list.append(i)
final_dt = cas_cid.drop(drop_list, axis=0)

final_dt.to_csv('20240223_THR_PC10_SMILES_CID.csv')
final_dt.to_excel('20240223_THR_PC10_SMILES_CID.xlsx')

#%%
import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
from tqdm import tqdm

ua = UserAgent(use_cache_server=True)
header = {"User-Agent":ua.random}
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

dt = pd.read_excel(r'C:\Users\user\Desktop\1\Modeling\16. THR 단일물질\input data\20240223_THR_PC10_SMILES.xlsx')
cas_list = dt['CAS No']
cas_list = [cas.strip() for cas in cas_list]

cas_cid = pd.read_excel(r'C:\Users\user\Desktop\1\Modeling\16. THR 단일물질\input data\20240223_THR_PC10_SMILES_CID.xlsx')
cid_list = []

for cas in tqdm(cas_list):
    cids = eval(cas_cid[cas_cid['CAS']==cas]['CID'].iloc[0])
    for cid in cids:
        try:
            print('try ...', cid)
            url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/' + cid + '/sdf'
            r = requests.get(url, verify=False, headers =header, timeout=100)
            open(r"C:\Users\user\Desktop\1\Modeling\16. THR 단일물질\input data\sdf\\" + cas +  '.sdf', 'wb').write(r.content)
            break
        except:
            print('\n\nBUG!!!!!!!!', cid,'\n\n')
        
    
    
    




