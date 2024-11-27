# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 16:41:38 2024

@author: jspark
"""

import requests
import pandas as pd
from fake_useragent import UserAgent
from tqdm import tqdm

ua = UserAgent(use_cache_server=True)
header = {"User-Agent":ua.random}
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

dt = pd.read_excel(r'C:\Users\user\Desktop\1\Modeling\18. AOP 예측모델\피부과민성\KE1\classification\data\20240801_KE1_classification_new.xlsx')
cid_list = dt['CID']

for cid in tqdm(cid_list):
    url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/sdf'
    r = requests.get(url, verify=False, headers =header, timeout=100)
    open(rf"C:\Users\user\Desktop\1\Modeling\18. AOP 예측모델\피부과민성\KE1\classification\data\sdf\{cid}.sdf", 'wb').write(r.content)    
    
#%%
from rdkit import Chem
import os

def sdf_to_xyz(sdf_file):
    # SDF 파일을 읽어들임
    suppl = Chem.SDMolSupplier(sdf_file)
    
    for mol in suppl:
        if mol is None:
            continue
        
        # 분자 이름
        name = mol.GetProp('_Name') if mol.HasProp('_Name') else 'Molecule'
        
        # XYZ 좌표 출력
        conf = mol.GetConformer()
        print(f"{name} XYZ Coordinates:")
        for atom in mol.GetAtoms():
            pos = conf.GetAtomPosition(atom.GetIdx())
            symbol = atom.GetSymbol()
            print(f"{symbol} {pos.x:.4f} {pos.y:.4f} {pos.z:.4f}")
        print()

# SDF 파일 경로
sdf_path = r'C:\Users\user\Desktop\1\Modeling\18. AOP 예측모델\피부과민성\KE1\classification\data\sdf'
sdf_files = os.listdir(sdf_path)
os.chdir(sdf_path)
for sdf_file in sdf_files:
    # XYZ 좌표 추출 및 출력
    xyz = sdf_to_xyz(sdf_file)
    break