import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from tqdm import tqdm
import pandas as pd
# user agent setting
ua = UserAgent()
header = {"User-Agent":ua.random}
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
product_info_row = []

for url_id in tqdm(range(1, 194)):
    url = f'https://ecolife.me.go.kr/ecolife/chmstryProduct/chmstryProductIndex?prdCd=01&irdntYn=Y&side=SM020101&page={url_id}'
    response = requests.get(url, verify=False, headers = header, timeout=30)
    response = response.content
    web_page = BeautifulSoup(response, 'html.parser')
    web_table = web_page.select_one('#printArea > table > tbody')
    web_list = web_table.findAll('tr')
    for web in web_list:            
        product = web.find('a').get('onclick').split("'")
        product_simple_id = web.find('td').text.strip()
        product_no = product[1]
        product_tag = product[3]

        product_url = f'https://ecolife.me.go.kr/ecolife/chmstryProduct/chmstryProductShow/{product_no}/{product_tag}'
        if product_no == '15004':
            product_name = '옥시파워'
            product_category = '표백제 / 의류, 섬유용 / 2.5kg'
            names = ['α-헥실시남알데하이드/α-hexylcinnamaldehyde', '3-p-큐메닐-2-메틸프로파이온알데하이드/3-p-cumenyl-2-methylpropionaldehyde', '시트로넬롤/Citronellol', '벤조산 벤질/Benzyl benzoate','핀-2(10)-엔/Pin-2(10)-ene','제올라이트/Zeolites','2,6-다이메틸헵탄-2-올/2,6-dimethylheptan-2-ol',
                     '리날룰옥사이드/', '29H,31H-프탈로시아니네이토(2-)-N29,N30,N31,N32 구리/29H,31H-phthalocyaninato(2-)-N29,N30,N31,N32 copper', '탄산 다이소듐 과산화물/Sodium carbonate peroxide','2,6-다이메틸락트-7-엔-2-올/2,6-dimethyloct-7-en-2-ol','3-옥소-2-펜틸사이클로펜테인아세트산 메틸/Methyl 3-oxo-2-pentylcyclopentaneacetate',
                     '아세트산 4-tert-뷰틸사이클로/4-tert-butylcyclohexyl acetate','탄산 소듐/Sodium carbonate','1-(1,2,3,4,5,6,7,8-옥타하이드로-2,3,8,8-테트라메틸-2-나프틸)에탄-1-온/1-(1,2,3,4,5,6,7,8-octahydro-2,3,8,8-tetramethyl-2-naphthyl)ethan-1-one','(R)-p-멘타-1,8-다이엔/(R)-p-mentha-1,8-diene',
                     '염화 소듐/Sodium chloride','리날로올/Linalool','2-(4-tert-뷰틸벤질)프로파이온알데하이드/2-(4-tert-butylbenzyl)propionaldehyde','홍차 추출물/BLACK TEA EXTRACT','소듐 2-프로펜산, 호모폴리머/2-Propenoic acid, homopolymer, sodium salt','5,12-다이하이드로-2,9-다이메틸퀴노[2,3-b]아크리딘-7,14-다이온/5,12-dihydro-2,9-dimethylquino[2,3-b]acridine-7,14-dione']
            cass = ['101-86-0','103-95-7','106-22-9','','127-91-3','1318-02-1','13254-34-7','1365-19-1','147-14-8','15630-89-4','18479-58-8','24851-98-7','32210-23-4','497-19-8','54464-57-2','5989-27-5','7647-14-5','78-70-6','80-54-6','','9003-04-7','980-26-7']
            uses = ['향료','향료','향료','향료','향료','외관개선','향료','향료','외관개선','산소계표백제','향료','향료','향료','산소계표백제','향료','향료','성능보조','향료','향료','외관개선','외관개선','외관개선']
            for i in range(len(names)):
                product_info_row.append([product_simple_id, product_category, product_name, names[i], cass[i], uses[i]])
            continue
        if product_no == '15007':
            product_name = '스파크 산소표백제'
            product_category = '표백제 / 의류, 섬유용 / 0.25kg, 0.5kg, 1.2kg, 1.4kg, 2kg, 3.5kg'
            names = ['α-헥실시남알데하이드/α-hexylcinnamaldehyde', '3-p-큐메닐-2-메틸프로파이온알데하이드/3-p-cumenyl-2-methylpropionaldehyde', '시트로넬롤/Citronellol', '벤조산 벤질/Benzyl benzoate','핀-2(10)-엔/Pin-2(10)-ene','제올라이트/Zeolites','2,6-다이메틸헵탄-2-올/2,6-dimethylheptan-2-ol',
                     '리날룰옥사이드/', '29H,31H-프탈로시아니네이토(2-)-N29,N30,N31,N32 구리/29H,31H-phthalocyaninato(2-)-N29,N30,N31,N32 copper', '탄산 다이소듐 과산화물/Sodium carbonate peroxide','2,6-다이메틸락트-7-엔-2-올/2,6-dimethyloct-7-en-2-ol','3-옥소-2-펜틸사이클로펜테인아세트산 메틸/Methyl 3-oxo-2-pentylcyclopentaneacetate',
                     '아세트산 4-tert-뷰틸사이클로/4-tert-butylcyclohexyl acetate','탄산 소듐/Sodium carbonate','1-(1,2,3,4,5,6,7,8-옥타하이드로-2,3,8,8-테트라메틸-2-나프틸)에탄-1-온/1-(1,2,3,4,5,6,7,8-octahydro-2,3,8,8-tetramethyl-2-naphthyl)ethan-1-one','(R)-p-멘타-1,8-다이엔/(R)-p-mentha-1,8-diene',
                     '염화 소듐/Sodium chloride','리날로올/Linalool','2-(4-tert-뷰틸벤질)프로파이온알데하이드/2-(4-tert-butylbenzyl)propionaldehyde','홍차 추출물/BLACK TEA EXTRACT','소듐 2-프로펜산, 호모폴리머/2-Propenoic acid, homopolymer, sodium salt','5,12-다이하이드로-2,9-다이메틸퀴노[2,3-b]아크리딘-7,14-다이온/5,12-dihydro-2,9-dimethylquino[2,3-b]acridine-7,14-dione']
            cass = ['101-86-0','103-95-7','106-22-9','','127-91-3','1318-02-1','13254-34-7','1365-19-1','147-14-8','15630-89-4','18479-58-8','24851-98-7','32210-23-4','497-19-8','54464-57-2','5989-27-5','7647-14-5','78-70-6','80-54-6','','9003-04-7','980-26-7']
            uses = ['향료','향료','향료','향료','향료','외관개선','향료','향료','외관개선','산소계표백제','향료','향료','향료','산소계표백제','향료','향료','성능보조','향료','향료','외관개선','외관개선','외관개선']
            for i in range(len(names)):
                product_info_row.append([product_simple_id, product_category, product_name, names[i], cass[i], uses[i]])
            continue
        if product_no == '15013':
            product_name = '스파크 스팀100도씨'
            product_category = '표백제 / 의류, 섬유용 / 0.2kg, 1.4kg'
            names_and_uses = ['α-헥실시남알데하이드/α-hexylcinnamaldehyde', '향료','3-p-큐메닐-2-메틸프로파이온알데하이드/3-p-cumenyl-2-methylpropionaldehyde','향료',"N,N'-에틸렌비스[N-아세틸아세트아마이드]/N,N'-ethylenebis[N-acetylacetamide]",'성능보조','시트로넬롤/Citronellol','향료',
             '벤조산 벤질/Benzyl benzoate','향료','핀-2(10)-엔/Pin-2(10)-ene','향료','제올라이트/Zeolites','외관개선','2,6-다이메틸헵탄-2-올/2,6-dimethylheptan-2-ol','향료','카올린/Kaolin','성능보조','이산화 티타늄/Titanium dioxide','성능보조','리날룰옥사이드/','향료',
             '29H,31H-프탈로시아니네이토(2-)-N29,N30,N31,N32 구리/29H,31H-phthalocyaninato(2-)-N29,N30,N31,N32 copper','외관개선','탄산 다이소듐 과산화물/Sodium carbonate peroxide','산소계표백제','2,6-다이메틸락트-7-엔-2-올/2,6-dimethyloct-7-en-2-ol','향료',
             '3-옥소-2-펜틸사이클로펜테인아세트산 메틸/Methyl 3-oxo-2-pentylcyclopentaneacetate','향료','에톡실화된 폴리(옥시-1,2-에탄다일),α-하이드로-ω-하이드록시- 에탄-1,2-다이올/Poly(oxy-1,2-ethanediyl),α-hydro-ω-hydroxy- Ethane-1,2-diol, ethoxylated','성능보조',
             '아세트산 4-tert-뷰틸사이클로/4-tert-butylcyclohexyl acetate','향료','탄산 소듐/Sodium carbonate','산소계표백제','1-(1,2,3,4,5,6,7,8-옥타하이드로-2,3,8,8-테트라메틸-2-나프틸)에탄-1-온/1-(1,2,3,4,5,6,7,8-octahydro-2,3,8,8-tetramethyl-2-naphthyl)ethan-1-one','향료',
             '(R)-p-멘타-1,8-다이엔/(R)-p-mentha-1,8-diene','향료','염화 소듐/Sodium chloride','성능보조','황산 소듐/Sodium sulphate','성능보조','리날로올/Linalool','향료','2-(4-tert-뷰틸벤질)프로파이온알데하이드/2-(4-tert-butylbenzyl)propionaldehyde','향료',
             '홍차 추출물/BLACK TEA EXTRACT','외관개선','소듐 2-프로펜산, 호모폴리머/2-Propenoic acid, homopolymer, sodium salt','외관개선','카복시메틸 셀룰로스 소듐염/Carboxymethyl cellulose sodium salt','성능보조','덱스트린/','성능보조',
             '2-[4,5-다이에톡시-2-(에톡시메틸)-6-메톡시옥산-3-일]옥시-6-(하이드록시메틸)-5-메톡시옥세인-3,4-다이올/2-[4,5-diethoxy-2-(ethoxymethyl)-6-methoxyoxan-3-yl]oxy-6-(hydroxymethyl)-5-methoxyoxane-3,4-diol','성능보조','서브틸리신/Subtilisin','성능보조',
             '2-(노나노일록시)벤젠설폰산 소듐/sodium 2-(nonanoyloxy)benzenesulfonate','성능보조','5,12-다이하이드로-2,9-다이메틸퀴노[2,3-b]아크리딘-7,14-다이온/5,12-dihydro-2,9-dimethylquino[2,3-b]acridine-7,14-dione','외관개선']
            cass = ['101-86-0','103-95-7','10543-57-4','106-22-9','','127-91-3','1318-02-1','13254-34-7','1332-58-7','13463-67-7','1365-19-1','147-14-8','15630-89-4','18479-58-8','24851-98-7','25322-68-3','32210-23-4','497-19-8','54464-57-2','5989-27-5','7647-14-5',
                    '7757-82-6','78-70-6','80-54-6','','9003-04-7','9004-32-4','9004-53-9','9004-57-3','9014-01-1','91125-43-8','980-26-7']
            for i in range(len(cass)):
                product_info_row.append([product_simple_id, product_category, product_name, names_and_uses[2*i], cass[i], names_and_uses[2*i+1]])
            continue
        if product_no == '15001':
            product_name = '투명한생각 분말세제'
            product_category = '합성세제 / 의류, 섬유용 / 4kg'
            names_and_uses = ['카올린/Kaolin','성능보조','이산화 티타늄/Titanium dioxide','성능보조','탄산수소 소듐/Sodium hydrogencarbonate','성능보조',
                              '도데실 황산 소듐/Sodium dodecyl sulphate','계면활성제','에톡실화된 폴리(옥시-1,2-에탄다일),α-하이드로-ω-하이드록시- 에탄-1,2-다이올/Poly(oxy-1,2-ethanediyl),α-hydro-ω-hydroxy- Ethane-1,2-diol, ethoxylated','성능보조',
                              '탄산 소듐/Sodium carbonate','성능보조','염화 소듐/Sodium chloride','성능보조','황산 소듐/Sodium sulphate','성능보조','셀룰로스/Cellulose','성능보조','덱스트린/','성능보조','서브틸리신/Subtilisin','성능보조']
            cass = ['1332-58-7','13463-67-7','144-55-8','151-21-3','25322-68-3','497-19-8','7647-14-5','7757-82-6','9004-34-6','9004-53-9','9014-01-1']
            for i in range(len(cass)):
                product_info_row.append([product_simple_id, product_category, product_name, names_and_uses[2*i], cass[i], names_and_uses[2*i+1]])
            continue
        if product_no == '14997':
            product_name = '파워산소표백'
            product_category = '표백제 / 의류, 섬유용 / 7kg'
            names_and_uses = ['α-헥실시남알데하이드/α-hexylcinnamaldehyde','향료','3-p-큐메닐-2-메틸프로파이온알데하이드/3-p-cumenyl-2-methylpropionaldehyde','향료','시트로넬롤/Citronellol','향료','벤조산 벤질/Benzyl benzoate','향료',
                              '핀-2(10)-엔/Pin-2(10)-ene','향료','제올라이트/Zeolites','외관개선','2,6-다이메틸헵탄-2-올/2,6-dimethylheptan-2-ol','향료','리날룰옥사이드/','향료',
                              '29H,31H-프탈로시아니네이토(2-)-N29,N30,N31,N32 구리/29H,31H-phthalocyaninato(2-)-N29,N30,N31,N32 copper','외관개선','탄산 다이소듐 과산화물/Sodium carbonate peroxide','산소계표백제','2,6-다이메틸락트-7-엔-2-올/2,6-dimethyloct-7-en-2-ol','향료',
                              '3-옥소-2-펜틸사이클로펜테인아세트산 메틸/Methyl 3-oxo-2-pentylcyclopentaneacetate','향료','아세트산 4-tert-뷰틸사이클로/4-tert-butylcyclohexyl acetate','향료','탄산 소듐/Sodium carbonate','산소계표백제',
                              '1-(1,2,3,4,5,6,7,8-옥타하이드로-2,3,8,8-테트라메틸-2-나프틸)에탄-1-온/1-(1,2,3,4,5,6,7,8-octahydro-2,3,8,8-tetramethyl-2-naphthyl)ethan-1-one','향료','(R)-p-멘타-1,8-다이엔/(R)-p-mentha-1,8-diene','향료','염화 소듐/Sodium chloride','성능보조',
                              '리날로올/Linalool','향료','2-(4-tert-뷰틸벤질)프로파이온알데하이드/2-(4-tert-butylbenzyl)propionaldehyde','향료','홍차 추출물/BLACK TEA EXTRACT','외관개선','소듐 2-프로펜산, 호모폴리머/2-Propenoic acid, homopolymer, sodium salt','외관개선',
                              '5,12-다이하이드로-2,9-다이메틸퀴노[2,3-b]아크리딘-7,14-다이온/5,12-dihydro-2,9-dimethylquino[2,3-b]acridine-7,14-dione','외관개선']
            cass = ['101-86-0','103-95-7','106-22-9','','127-91-3','1318-02-1','13254-34-7','1365-19-1','147-14-8','15630-89-4','18479-58-8','24851-98-7','32210-23-4','497-1-98','54464-57-2','5989-27-5','7647-14-5','78-70-6','80-54-6','','9003-04-7','980-26-7']
            for i in range(len(cass)):
                product_info_row.append([product_simple_id, product_category, product_name, names_and_uses[2*i], cass[i], names_and_uses[2*i+1]])
            continue
        if product_no == '15005':
            product_name = 'O2 산소표백제'
            product_category = '표백제 / 의류, 섬유용 / 1.2kg, 2kg'
            names_and_uses = ['α-헥실시남알데하이드/α-hexylcinnamaldehyde','향료','3-p-큐메닐-2-메틸프로파이온알데하이드/3-p-cumenyl-2-methylpropionaldehyde','향료','시트로넬롤/Citronellol','향료','벤조산 벤질/Benzyl benzoate','향료',
                              '핀-2(10)-엔/Pin-2(10)-ene','향료','제올라이트/Zeolites','외관개선','2,6-다이메틸헵탄-2-올/2,6-dimethylheptan-2-ol','향료','리날룰옥사이드/','향료',
                              '29H,31H-프탈로시아니네이토(2-)-N29,N30,N31,N32 구리/29H,31H-phthalocyaninato(2-)-N29,N30,N31,N32 copper','외관개선','탄산 다이소듐 과산화물/Sodium carbonate peroxide','산소계표백제','2,6-다이메틸락트-7-엔-2-올/2,6-dimethyloct-7-en-2-ol','향료',
                              '3-옥소-2-펜틸사이클로펜테인아세트산 메틸/Methyl 3-oxo-2-pentylcyclopentaneacetate','향료','아세트산 4-tert-뷰틸사이클로/4-tert-butylcyclohexyl acetate','향료','탄산 소듐/Sodium carbonate','산소계표백제',
                              '1-(1,2,3,4,5,6,7,8-옥타하이드로-2,3,8,8-테트라메틸-2-나프틸)에탄-1-온/1-(1,2,3,4,5,6,7,8-octahydro-2,3,8,8-tetramethyl-2-naphthyl)ethan-1-one','향료','(R)-p-멘타-1,8-다이엔/(R)-p-mentha-1,8-diene','향료','염화 소듐/Sodium chloride','성능보조',
                              '리날로올/Linalool','향료','2-(4-tert-뷰틸벤질)프로파이온알데하이드/2-(4-tert-butylbenzyl)propionaldehyde','향료','홍차 추출물/BLACK TEA EXTRACT','외관개선','소듐 2-프로펜산, 호모폴리머/2-Propenoic acid, homopolymer, sodium salt','외관개선',
                              '5,12-다이하이드로-2,9-다이메틸퀴노[2,3-b]아크리딘-7,14-다이온/5,12-dihydro-2,9-dimethylquino[2,3-b]acridine-7,14-dione','외관개선']
            cass = ['101-86-0','103-95-7','106-22-9','','127-91-3','1318-02-1','13254-34-7','1365-19-1','147-14-8','15630-89-4','18479-58-8','24851-98-7','32210-23-4','497-1-98','54464-57-2','5989-27-5','7647-14-5','78-70-6','80-54-6','','9003-04-7','980-26-7']
            for i in range(len(cass)):
                product_info_row.append([product_simple_id, product_category, product_name, names_and_uses[2*i], cass[i], names_and_uses[2*i+1]])
            continue
        if product_no == '15002':
            product_name = '내추럴 온리3'
            product_category = '합성세제 / 의류, 섬유용 / 0.3kg, 3kg'
            names_and_uses = ['탄산수소 소듐/Sodium hydrogencarbonate','성능보조','도데실 황산 소듐/Sodium dodecyl sulphate','계면활성제','염화 소듐/Sodium chloride','성능보조']
            cass = ['144-55-8','151-21-3','7647-14-5']
            for i in range(len(cass)):
                product_info_row.append([product_simple_id, product_category, product_name, names_and_uses[2*i], cass[i], names_and_uses[2*i+1]])
            continue
        response = requests.get(product_url, verify = False, headers = header, timeout = 30)
        response = response.content
        web_page = BeautifulSoup(response, 'html.parser')
        product_name = web_page.select_one('#printArea > div.detail-info > table:nth-child(2) > tbody > tr:nth-child(1) > td')
        if product_name == None:
            print('bug')
            print(product_url)
            product_name = '나중에채우자'
            product_category = '위생용품'
            composition_table = web_page.select_one('#printArea > table > tbody')
            composition_table = composition_table.findAll('tr')
        else:
            product_name = product_name.text.strip()
            product_category = web_page.select_one('#printArea > div.detail-info > table:nth-child(2) > tbody > tr:nth-child(2) > td')
            product_category = product_category.text.strip()

            composition_table = web_page.select_one('#printArea > div.detail-info > table:nth-child(5) > tbody')
            composition_table = composition_table.findAll('tr')
        for i in range(len(composition_table)):
            chemical = composition_table[i]
            chemical = chemical.findAll('td')
            if len(chemical) == 1:
                # 조회된 정보가 없습니다
                temp = [product_simple_id, product_category, product_name, None, None, None]
                product_info_row.append(temp)
                print(product_url)
                break
            name = chemical[0].text
            use = chemical[1].text
            if chemical[2].find('a') == None:
                cas = None
            else:
                cas = chemical[2].find('a').get('href')[1:]
            temp = [product_simple_id, product_category, product_name, name, cas, use]
            product_info_row.append(temp)

    output = pd.DataFrame(product_info_row)
    output.to_excel(r'C:\Users\user\Desktop\1\Modeling\0. utils\크롤링\20241101_초록누리_crawling\output_total.xlsx', index=False)
