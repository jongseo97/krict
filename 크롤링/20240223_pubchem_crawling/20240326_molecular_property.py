-# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 16:48:31 2024

@author: jspark
"""

import pandas as pd

from rdkit import Chem
from rdkit.Chem import Descriptors


file_name = r'Z:\모델링팀\과제\환경부(생활화학제품)\2024.04.03.전달용\예시데이터\플랫폼용예시데이터_입력_수정.xlsx'
new_file_name = r'Z:\모델링팀\과제\환경부(생활화학제품)\2024.04.03.전달용\예시데이터\플랫폼용예시데이터_입력_최종.xlsx'

dt = pd.read_excel(file_name)
smiles_list = dt['SMILES']

heavy_atom_list = []
MW_list = []
charge_list = []
logp_list = []
for smiles in smiles_list:
    mol = Chem.MolFromSmiles(smiles)
    numHeavyAtom = Descriptors.HeavyAtomCount(mol)
    MW = Descriptors.MolWt(mol)
    charge = Chem.GetFormalCharge(mol)
    logp = Descriptors.MolLogP(mol)
    
    heavy_atom_list.append(numHeavyAtom)
    MW_list.append(MW)
    charge_list.append(charge)
    logp_list.append(logp)

dt['#_Heavy_Atom'] = heavy_atom_list
dt['Molecular_Weight'] = MW_list
dt['Formal_Charge'] = charge_list
dt['LogP'] = logp_list

dt.to_excel(new_file_name, index=False)