# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 15:37:18 2024

@author: jspark
"""

import requests
from fake_useragent import UserAgent
import pandas as pd

# user agent setting
ua = UserAgent()
header = {"User-Agent":ua.random}
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# cas number -> CID
def cas_to_cid(cas):
    url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{cas}/cids/txt'
    header = {"User-Agent":ua.random}
    r = requests.get(url, verify=False, headers = header, timeout=30)
    # time.sleep(1)
    if r.status_code != 200:
        return None
    r.encoding = 'utf-8'
    cid = r.text.strip()
    cid = cid.split('\n')[0]
    return cid

def cas_to_GHS(cas):
    
    # cid = cas_to_cid(cas)
    # print(f'{cas} --> {cid}')
    # if input is cid
    cid = cas
    
    
    final_code_list = []
    final_full_code_list = []
    
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
    while 'Information' not in data or 'Section' in data:
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
                if ref['ReferenceNumber'] == ref_num:
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
    if len(final_code_list) ==0:
        return final_code_list, final_full_code_list
    if final_code_list[0] != 'Not Classified':
        index = [i for i, value in enumerate(final_code_list) if value != 'Not Classified']
        final_code_list = [final_code_list[i] for i in index]
        final_full_code_list = [final_full_code_list[i] for i in index]
        
    # print('Done')
    # return '; '.join(final_code_list), '; '.join(final_full_code_list) # return string
    return final_code_list, final_full_code_list # return list


from tqdm import tqdm
dt = pd.read_excel(r'C:\Users\user\Desktop\1\DB\20241029_대체물질_수요조사서식_파일\20241029_F_Use.xlsx')
for i, row in dt.iterrows():
    if pd.isna(row['GHS']):
        cids = str(row['CID'])
        cids = cids.split(', ')
        for cid in cids:
            GHS, GHS_full = cas_to_GHS(cid)
            GHS = '; '.join(GHS)
            GHS_full = '; '.join(GHS_full)
            if GHS != '':
                break
        print(i, cids, GHS, GHS_full, '\n')

if __name__ == '__main__':
    dt = pd.read_excel(r'C:\Users\user\Desktop\1\DB\20241029_어린이제품_저작권_DB\과정 파일\어린이제품_CAS_CID_SMILES_list.xlsx')
    output_path = r'C:\Users\user\Desktop\1\DB\20241029_어린이제품_저작권_DB\과정 파일\어린이제품_GHS.xlsx'
    cas_list = dt['CAS']
    cid_list = dt['CID']
    GHS_list = []
    GHS_full_list = []
    for cid in tqdm(cid_list):
        if pd.isna(cid):
            GHS_list.append(None)
            GHS_full_list.append(None)
            continue
        cid = str(int(cid))
        cids = cid.split(', ')
        for cid in cids:
            GHS, GHS_full = cas_to_GHS(cid)
            GHS = '; '.join(GHS)
            GHS_full = '; '.join(GHS_full)
            if GHS != '':
                break
        GHS_list.append(GHS)
        GHS_full_list.append(GHS_full)
    
    # GHS_list = []
    # GHS_full_list = []
    # for cas in tqdm(cas_list):
    #     GHS, GHS_full = cas_to_GHS(cas)
    #     GHS = '; '.join(GHS)
    #     GHS_full = '; '.join(GHS_full)
        
    #     GHS_list.append(GHS)
    #     GHS_full_list.append(GHS_full)
        
    dt['GHS'] = GHS_list
    dt['GHS_full'] = GHS_full_list
    
    dt.to_excel(output_path, index=False)


