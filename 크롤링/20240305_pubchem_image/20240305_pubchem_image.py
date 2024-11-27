# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 13:37:37 2024

@author: jspark
"""

import requests
import pandas as pd
from fake_useragent import UserAgent
from tqdm import tqdm
from PIL import Image
import numpy as np

# avoid SSL certification 
ua = UserAgent()
header = {"User-Agent":ua.random}
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

input_path = r'C:\Users\user\Desktop\1\Platform\ToxSquare\온메이커스_전달\2024.10.30_온메이커스_전달\DB\single_compounds.xlsx'
output_path = r'C:\Users\user\Desktop\1\Platform\ToxSquare\온메이커스_전달\2024.10.30_온메이커스_전달\DB\structures'

# data import 
dt = pd.read_excel(input_path)
cid_list = dt['CID']
cas_list = dt['CAS No']
for i, cid in tqdm(enumerate(cid_list)):
    if str(cid) == 'nan':
        continue
    cid = int(cid)
    url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG?image_size=500x500'   #<- define image size
    #url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG?image_size=500x500' # define image size
    
    file_name = rf'{output_path}\{cas_list[i]}.png'

    r = requests.get(url, verify=False, headers =header, timeout=100)
    open(file_name, 'wb').write(r.content)
    
    # background color gray -> white
    im = Image.open(file_name)
    im = im.convert('RGBA')
    
    data =  np.array(im)
    red, green, blue, alpha = data.T
    
    grey_area = (red == 245) & (blue == 245) & (green == 245)
    data[..., :-1][grey_area.T] = (255, 255, 255)

    im2 = Image.fromarray(data)
    im2.save(file_name,'PNG')
    

