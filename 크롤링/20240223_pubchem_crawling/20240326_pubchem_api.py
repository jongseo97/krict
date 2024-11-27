# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 14:50:56 2024

@author: jspark
"""

import pandas as pd
import requests
from fake_useragent import UserAgent
from tqdm import tqdm

# avoid SSL certification 
ua = UserAgent()
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# 1. Change identifiers to CID
# 2. Get properties with CID

# chemical name -> CID
def name_to_cid(name):
    url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/cids/txt'
    header = {"User-Agent":ua.random}
    r = requests.get(url, verify=False, headers = header, timeout=10)
    if r.status_code != 200:
        return None
    r.encoding = 'utf-8'
    cid = r.text.strip()
    return cid

# cas number -> CID
def cas_to_cid(cas):
    url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{cas}/cids/txt'
    header = {"User-Agent":ua.random}
    r = requests.get(url, verify=False, headers = header, timeout=10)
    if r.status_code != 200:
        return None
    r.encoding = 'utf-8'
    cid = r.text.strip()
    cid = cid.split('\n')[0]
    return cid

# CAS -> SMILES
def cas_to_smiles(cas):
    url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{cas}/property/isomericsmiles/txt'
    header = {"User-Agent":ua.random}
    r = requests.get(url, verify=False, headers = header, timeout=100)
    if r.status_code != 200:
        return None
    r.encoding = 'utf-8'
    smiles = r.text.strip()
    smiles = smiles.split('\n')[0]
    return smiles

# SMILES -> CID 
# only canonical smiles can be used
def smiles_to_cid(smiles):
    url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/cids/txt'
    header = {"User-Agent":ua.random}
    r = requests.get(url, verify=False, headers = header, timeout=10)
    if r.status_code != 200:
        return None
    r.encoding = 'utf-8'
    cid = r.text.strip()
    cid = cid.split('\n')[0]
    return cid

# CID -> SMILES
def cid_to_smiles(cid):
    url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/isomericsmiles/txt'
    header = {"User-Agent":ua.random}
    r = requests.get(url, verify=False, headers = header, timeout=100)
    if r.status_code != 200:
        return None
    r.encoding = 'utf-8'
    smiles = r.text.strip()
    return smiles

# CID -> chemical name
def cid_to_name(cid):
    url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/iupacname/txt'
    header = {"User-Agent":ua.random}
    r = requests.get(url, verify=False, headers = header, timeout=10)
    if r.status_code != 200:
        return None
    r.encoding = 'utf-8'
    name = r.text.strip()
    return name

# CID -> cas number
def cid_to_cas(cid):
    url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON'
    header = {"User-Agent":ua.random}
    r = requests.get(url, verify=False, headers = header, timeout=10)
    if r.status_code != 200:
        return None
    r.encoding = 'utf-8'
    data = r.json()
    while 'Information' not in data:
        for d in data:
            if type(data) == dict:
                d = data[d]
            if 'CAS' in str(d):
                break
        data = d
        if type(data) == str:
            print('CAS number not found.')
            return None
    
    cas = data['Information'][0]['Value']['StringWithMarkup'][0]['String']
    return cas

def cid_to_GHS(cid):    
    final_code_list = []
    final_full_code_list = []
    header = {"User-Agent":ua.random}
    url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON'
    r = requests.get(url, verify=False, headers=header, timeout=100)
    r.encoding = 'utf-8'
    data = r.json()
    
    # GHS 정보가 없거나 위험하지 않은 경우 빈 값 return
    if 'Record' not in data or 'GHS Hazard' not in str(data):
        print(f'{cid} is bug or safe CID ') # 분리해야할수도
        return final_code_list, final_full_code_list
    
    # reference 추출 - ECHA 데이터만 추출하기 위함
    references = data['Record']['Reference']
    # data 추출
    data = data['Record']['Section']
    
    # data 추출
    while 'Information' not in data:
        for d in data:
            if type(data) == dict:
                d = data[d]
            if 'GHS Hazard' in str(d):
                break
        data = d
    data = data['Information']
    for dat in data:
        # PUG View에서 GHS 있는 항목 찾기
        if 'GHS Hazard' in str(dat):
            # 해당 reference name 매칭 위한 reference number 가져옴
            ref_num = dat['ReferenceNumber']
            # reference name 추출
            for ref in references:
                if f"'ReferenceNumber': {ref_num}" in str(ref):
                    ref_name = ref['SourceName']
            
            # 다양한 reference 중 ECHA만 사용하기로 결정
            if 'ECHA' in ref_name:
                # H code list 추출
                H_list = dat['Value']['StringWithMarkup']
                code_list = []
                full_code_list = []            
                for H_string in H_list:
                    # Code 및 Code + 설명 추출
                    H_code = H_string["String"].split(" ")[0].split(":")[0]
                    H_code_full = H_string["String"]
                    
                    # safe chemical
                    if H_code_full == 'Not Classified':
                        code_list.append(H_code_full)
                        full_code_list.append(H_code_full)
                        break
                    
                    # (92.57%) 이런거 괄호 제거
                    if '(' in H_code_full:    
                        H_code_full = H_code_full.split('(')[0].strip() + H_code_full.split(')')[-1]
                    code_list.append(H_code)
                    full_code_list.append(H_code_full)
            
                final_code_list += code_list
                final_full_code_list += full_code_list
    
    # 중복제거 및 오름차순 정리
    final_code_list = list(set(final_code_list))
    final_code_list.sort()
    final_full_code_list = list(set(final_full_code_list))
    final_full_code_list.sort()
    
    # 다른 H code가 존재하는 경우 Not Classified 삭제
    if final_code_list[0] != 'Not Classified':
        index = [i for i, value in enumerate(final_code_list) if value != 'Not Classified']
        final_code_list = [final_code_list[i] for i in index]
        final_full_code_list = [final_full_code_list[i] for i in index]
        
    print('Done')
    # return '; '.join(final_code_list), '; '.join(final_full_code_list) # return string
    return final_code_list, final_full_code_list # return list



if __name__ == '__main__':
    
    # data import 
    out_name = r'C:\Users\user\Desktop\1\Modeling\24. MoA 예측\살생물제\20241121_살생물제_SMILES.xlsx'
    df = pd.read_csv(r'C:\Users\user\Desktop\1\Modeling\24. MoA 예측\살생물제\20240821_살생물제_크롤링.csv')
    cas_list = df['CAS No']
    smiles_list = []
    for cas in tqdm(cas_list):
        smiles = cas_to_smiles(cas)
        smiles_list.append(smiles)
    df = pd.DataFrame()
    df['SMILES'] = smiles_list
    df.to_excel(out_name)
    

            