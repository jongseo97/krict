# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 15:03:04 2024

@author: jspark
"""

from rdkit.Chem.Draw import IPythonConsole
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors
import pandas as pd
from tqdm import tqdm

dt = pd.read_excel(r'C:\Users\user\Desktop\1\Modeling\17. 대체물질 탐색 알고리즘\FunctionUse\processed data\20240425_cas_data.xlsx')
smiles_list = dt['SMILES']

bugs = []
total_result = []
i=0

legend_bugs = []
for smiles in tqdm(smiles_list):
    
    result = []
    mol = Chem.MolFromSmiles(smiles)
    type_check = str(mol)
    if(type_check == 'None'):
        bugs.append(smiles)
        for _ in range(324):
            result.append('None')
        total_result.append(result)

    else:
        m = Chem.AddHs(mol)
        if m is not None:
            desc_whim = []
            desc_rdf = []
            mol_result = AllChem.EmbedMolecule(m, randomSeed=42)  # randomSeed를 지정하여 재현성을 유지
            # AllChem.EmbedMolecule 실행 결과가 -1일 경우, Error 발생
            # if mol_result != 0:
            #     mol_result = AllChem.EmbedMolecule(m, randomSeed=42, maxAttempts=5000)  # 알고리즘이 프로세스를 다시 시도하는 횟수
            if mol_result != 0:
                print('\n',smiles)
                mol_result = AllChem.EmbedMolecule(m, randomSeed=42, useRandomCoords=True)  # 랜덤으로 결과값 나오는거

            # mol_result = -1 일 경우 제외
            if mol_result != 0:
                for _ in range(324):
                    result.append('None')
                total_result.append(result)

            else:
                # 분자의 3D 최적화(분자의 에너지 최소화-> 안정된 형태로 조정)
                try:
                    AllChem.UFFOptimizeMolecule(m)
                    desc_whim = rdMolDescriptors.CalcWHIM(m)
                    desc_rdf = rdMolDescriptors.CalcRDF(m)
                    result = desc_whim + desc_rdf
                    total_result.append(result)
                except:
                    legend_bugs.append(smiles)

        else:
            print("Failed to create molecule from SMILES.")
    
    # print(smiles, result)