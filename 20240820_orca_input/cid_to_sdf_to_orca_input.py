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

dt = pd.read_excel(r'C:\Users\user\Desktop\1\Modeling\18. AOP 예측모델\피부과민성\KE1\classification\data\20240801_KE1_classification_test.xlsx')
dt = pd.read_excel(r'C:\Users\user\Desktop\1\Modeling\18. AOP 예측모델\피부과민성\KE1\classification\data\20240801_KE1_classification_new.xlsx')
cid_list = dt['CID']

for cid in tqdm(cid_list):
    url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/sdf'
    url= f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/{cid}/record/SDF?record_type=3d&response_type=save&response_basename={cid}'
    r = requests.get(url, verify=False, headers =header, timeout=100)
    open(rf"C:\Users\user\Desktop\1\Modeling\18. AOP 예측모델\피부과민성\KE1\classification\data\3d_sdf\{cid}.sdf", 'wb').write(r.content)    
    
#%%

import os
from rdkit import Chem
from rdkit.Chem import AllChem

def sdf_to_inp(sdf_file):
    cid = int(sdf_file.split('.')[0])
    
    with open(sdf_file, 'r') as f:
        lines = f.readlines()
    
    if len(lines) < 10:
        for i, row in dt.iterrows():
            if row['CID'] == cid:
                smiles = row['isomericSMILES']
                print('train')
        for i, row in test_dt.iterrows():
            if row['CID'] == cid:
                smiles = row['isomericSMILES']
                print('test')
        print(cid, smiles)
        mol = Chem.MolFromSmiles(smiles)
        mol = Chem.AddHs(mol)
        params = AllChem.ETKDGv3()
        params.randomSeed = 0xf00d # optional random seed for reproducibility
        AllChem.EmbedMolecule(mol, params)
    
        lines = Chem.MolToMolBlock(mol)
        lines = lines.split('\n')
    
    lines = lines[4:]
    i = 0
    while True:
        line = lines[i]
        # if float(line.split()[0])%1 == 0:
        if len(line.split()) <= 8:
            break
        i += 1
    
    xyz_list = lines[:i]
    
    with open(fr'C:\Users\user\Desktop\1\Modeling\18. AOP 예측모델\피부과민성\KE1\classification\data\inp\{cid}.inp', 'w') as f:
        f.write('!B3LYP D4 DEF2-SVP OPT\n%maxcore 8000\n%pal\nnprocs 8\nend\n')
        f.write('* xyz 0 1\n')
        for xyz in xyz_list:
            xyz = xyz.split()
            symbol = xyz[3]
            x = xyz[0]
            y = xyz[1]
            z = xyz[2]
            
            line = f'{symbol} {x} {y} {z}\n'
            f.write(line)
        f.write('*')

test_dt = pd.read_excel(r'C:\Users\user\Desktop\1\Modeling\18. AOP 예측모델\피부과민성\KE1\classification\data\20240801_KE1_classification_test.xlsx')
dt = pd.read_excel(r'C:\Users\user\Desktop\1\Modeling\18. AOP 예측모델\피부과민성\KE1\classification\data\20240801_KE1_classification_new.xlsx')

# SDF 파일 경로
sdf_path = r'C:\Users\user\Desktop\1\Modeling\18. AOP 예측모델\피부과민성\KE1\classification\data\3d_sdf'
sdf_files = os.listdir(sdf_path)
os.chdir(sdf_path)
for sdf_file in sdf_files:
    # XYZ 좌표 추출 및 출력
    xyz = sdf_to_inp(sdf_file)
    
        
