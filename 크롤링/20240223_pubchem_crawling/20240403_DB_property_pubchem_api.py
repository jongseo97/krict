# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 14:50:56 2024

@author: jspark
"""

import pandas as pd
import requests
from fake_useragent import UserAgent


# avoid SSL certification 
ua = UserAgent()
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


# cid number -> properties
def cid_to_properties(cas):
    property_list = ['MolecularFormula','MolecularWeight','CanonicalSMILES','InChI','XLogP','Charge','HBondDonorCount','HBondAcceptorCount','RotatableBondCount','HeavyAtomCount']
    property_url = ''
    for p in property_list:
        property_url += f'{p},'
    property_url = property_url[:-1]
    url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/{property_url}/json'
    header = {"User-Agent":ua.random}
    r = requests.get(url, verify=False, headers = header, timeout=10)
    if r.status_code != 200:
        return None
    r.encoding = 'utf-8'
    result = r.json()
    result = list(list(result.values())[0].values())[0][0]
    
    for p in property_list:
        if p not in result:
            result[p] = 'None'
    
    return result



dt = pd.read_excel(r'C:\Users\user\Desktop\1\Platform\ToxSquare\20240521_전달용\DB\AR\single\#Final_495_cpds.xlsx')
match_id = pd.read_excel(r'C:\Users\user\Desktop\1\Platform\ToxSquare\20240521_전달용\DB\AR\single\AR_cpdID_cas_name.xlsx')



if __name__ == '__main__':
    # data import 
    file_name = r'Z:\모델링팀\과제\환경부(생활화학제품)\2024.04.03.전달용\DB용데이터\단일 데이터 예시\EB\#final_628_cpds(uM)_IC30_50.xlsx'
    new_file_name = r'Z:\모델링팀\과제\환경부(생활화학제품)\2024.04.03.전달용\DB용데이터\단일 데이터 예시\EB\#final_628_cpds(uM)_IC30_50.xlsx'
    dt = pd.read_excel(file_name)
    cas_list = dt['CAS No']
    
    results = dict()
    for cas in cas_list:
        properties = cas_to_properties(cas)
        for keys, values in properties.items():
            if keys in results:
                results[keys].append(values)
            else:
                results[keys] = [values]
    for keys, values in results.items():
        dt[keys] = values
    
    dt.to_excel(new_file_name, index = False)
                
