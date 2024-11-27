import pandas as pd
from rdkit import Chem
import requests
from fake_useragent import UserAgent

# CRAWLING setting
ua = UserAgent()
header = {"User-Agent":ua.random}
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# CAS to CID
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

# PATH setting
input_file = r'C:\Users\user\Desktop\1\Modeling\0. utils\20240923_CAS_list_to_SDF\Mix_1.csv' # file
output_path = r'C:\Users\user\Desktop\1\Modeling\0. utils\20240923_CAS_list_to_SDF\SDF' # folder

# get CAS list
dt = pd.read_csv(input_file)
cas_list = dt['CAS NO']

# get SDF files
total_sdf = []
for cas in cas_list:
    cid = cas_to_cid(cas) # get CID
    # for 2D structure
    url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/sdf'
    # for 3D Structure
    # url= f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/{cid}/record/SDF?record_type=3d&response_type=save&response_basename={cas}'
    r = requests.get(url, verify=False, headers =header, timeout=100)
    open(f"{output_path}/{cas}.sdf", 'wb').write(r.content) # get SDF
    total_sdf.append(r.content.decode('utf-8'))

# LIST to SDF file
with open(f'{output_path}/Total.sdf', 'w') as f:
    f.writelines(total_sdf)