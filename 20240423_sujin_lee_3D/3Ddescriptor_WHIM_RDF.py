from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os

smiles = True

# for whim in range(0, 113):
#     WHIM_desc_list.append(f"WHIM{whim +1}")
WHIM_desc_list = [f"WHIM{i + 1}" for i in range(114)]
RDF_desc_list = [f"RDF{i + 1}" for i in range(210)]
total_desc_list = WHIM_desc_list + RDF_desc_list

##파일 경로를 directory로 설정##
input_file = "C:\\Users\\user\\PycharmProjects\\ML_LSJ\\pycharm\\EDC_EDsig_algorithms_data\\20230818_Dataset\\prediction\\input_all\\"
output_file = "C:\\Users\\user\\PycharmProjects\\ML_LSJ\\pycharm\\EDC_EDsig_algorithms_data\\descriptor_result\\output_3D\\"



#batch file list
dir_filename = os.listdir(input_file)
files = [file for file in dir_filename if file.endswith(".xlsx")]
file_list = []

for z in range(0, len(files)):
    file_list.append(input_file + files[z])
print(str(file_list) + "/n")

output_dir = output_file

for i in range(0, len(file_list)):
    input_file = file_list[i]
    output_file_name = files[i][:-5]
    output_file = output_dir + output_file_name + "_3D.xlsx"

    print("file cnt:", i)

    total_result = []
    result = []
    cid_list = []
    smiles_list = []
    mol_list = []

    df = pd.read_excel(input_file)
    cid_list = list(df['CID'])
    label_list = list(df['label'])

    def replace_labels(label):
        if label == "Active":
            return 1
        elif label == "Inactive":
            return 0
        else:
            return label

    label = [replace_labels(label) for label in label_list]

    if smiles:
        smiles_list = list(df['SMILES'])
        for i in range(0, len(smiles_list)):
            mol_list.append(Chem.MolFromSmiles(smiles_list[i]))

    else:
        # get smiles and generate mol file
        for ai in range(0, len(cid_list)):
            print("CID: " + str(cid_list[ai]))

            url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/" + str(
                cid_list[ai]).strip() + "/property/CanonicalSMILES/txt"
            url_info = urlopen(url, None, timeout=100000)

            bsObject = BeautifulSoup(url_info, "html.parser")
            All_txt = bsObject.text
            smiles_list.append(All_txt.strip("\n"))
            mol_list.append(Chem.MolFromSmiles(All_txt.strip("\n")))

    print(len(mol_list))
    for bi in range(0, len(mol_list)):

        result = []

        print("count:", bi)
        print(smiles_list[bi])

        type_check = str(mol_list[bi])
        if(type_check == 'None'):
            for _ in range(324):
                result.append('None')
            total_result.append(result)

        else:
            m = Chem.MolFromSmiles(smiles_list[bi])
            m = Chem.AddHs(m)
            if m is not None:
                desc_whim = []
                desc_rdf = []
                mol_result = AllChem.EmbedMolecule(m, randomSeed=42)  # randomSeed를 지정하여 재현성을 유지
                # AllChem.EmbedMolecule 실행 결과가 -1일 경우, Error 발생
                # if mol_result != 0:
                #     mol_result = AllChem.EmbedMolecule(m, randomSeed=42, maxAttempts=5000)  # 알고리즘이 프로세스를 다시 시도하는 횟수
                if mol_result != 0:
                    mol_result = AllChem.EmbedMolecule(m, randomSeed=42, useRandomCoords=True)  # 랜덤으로 결과값 나오는거

                # mol_result = -1 일 경우 제외
                if mol_result != 0:
                    for _ in range(324):
                        result.append('None')
                    total_result.append(result)

                else:
                    # 분자의 3D 최적화(분자의 에너지 최소화-> 안정된 형태로 조정)
                    AllChem.UFFOptimizeMolecule(m)
                    desc_whim = rdMolDescriptors.CalcWHIM(m)
                    desc_rdf = rdMolDescriptors.CalcRDF(m)
                    result = desc_whim + desc_rdf
                    total_result.append(result)

            else:
                print("Failed to create molecule from SMILES.")

    # 결과를 데이터프레임으로 변환
    # result = np.array(desc)
    # print(result)
    result_df = pd.DataFrame(data=total_result, columns=total_desc_list)
    result_df.insert(loc=0, column="CID", value=cid_list)
    result_df.insert(loc=1, column="label", value=label)

    # 결과를 엑셀 파일로 저장
    result_df.to_excel(output_file, index=False)

    print("Saved WHIM descriptors to:", output_file)