import pandas as pd
from rdkit import Chem

file_smiles = pd.read_csv(r"C:\Users\user\Desktop\[금도금 smiles 관련]\금도금_smiles\20240209_금도금_smiles.csv")
smiles_list = file_smiles['SMILES']
smiles_list = list(smiles_list)
smiles_Result = []

my_smiles = 0
for smiles in smiles_list:
    try:
        temp = 0
        split_result = smiles.split('.') #(.) 쪼개기
        if len(split_result) == 1: #(.)이 없는 경우
            smiles_Result.append(smiles)
            continue
        for smi in split_result:
            mol = Chem.MolFromSmiles(smi)
            atoms = mol.GetNumAtoms()  #원자수 count
            if atoms > temp: #쪼갠 문자열의 원자수 비교(가장 큰놈을 가져오기)
                my_smiles = smi
                my_atoms = atoms
                temp = my_atoms
        if my_atoms == 1: #쪼갠것들 중에서 원자수가 가장 큰게 1일 경우,
            smiles_Result.append("None")

        else:
            smiles_Result.append(my_smiles)

    except AttributeError: #에러 발생할 경우 check >> (예시) "Explicit valence for atom # 1 Si, 8, is greater than permitted"
        smiles_Result.append("Check")

# print(smiles_Result)

# new_smiles = {'before': smiles_list, 'after': smiles_Result}
# new_smiles = pd.DataFrame(new_smiles)
# new_smiles.to_excel(excel_writer= r"C:\Users\user\Desktop\[금도금 smiles 관련]\금도금_smiles\20240220_result.xlsx", index=None)