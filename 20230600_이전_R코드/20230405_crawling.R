library(RCurl)
library(xml2)
library(utils)

CAS_to_CID <- function(cas){
  xml.path <- paste0("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/",cas,"/property/MolecularFormula/XML")
  xml.text <- tryCatch({
    xml.raw <- read_xml(xml.path)
    xml.node <- xml_children(xml.raw)
    xml.vector <- xml_find_all(xml.node,'./*')
    xml.text <- xml_text(xml.vector)[1]
    }, 
           error  = function(e) {
             print(cas)
             xml.path <- paste0('https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/name/',cas,'/cids/XML')
             xml.raw <- read_xml(xml.path)
             xml.node <- xml_children(xml.raw)
             xml.vector <- xml_find_all(xml.node,'./*')
             xml.text <- xml_text(xml.vector)[2]
             return(xml.text)
             },
           warning = function(e) {
             print('Holy')
             return(xml.path)
             })
  return(xml.text)
}

CAS_to_CID2 <- function(cas){
  xml.path <- paste0("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/",cas,"/cids/XML")
  cids <- tryCatch({
    xml.raw <- read_xml(xml.path)
    xml.node <- xml_children(xml.raw)
    cids <- xml_text(xml.node)
    names(cids) <- xml_name(xml.node)
    cids <- as.data.frame(cids)[1,1]
  }, 
  error  = function(e) {
    print(cas)
    xml.path <- paste0('https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/name/',cas,'/cids/XML')
    xml.raw <- read_xml(xml.path)
    xml.node <- xml_children(xml.raw)
    xml.node <- xml_children(xml.node)
    tmp <- as.list(xml_text(xml.node))
    names(tmp) <- xml_name(xml.node)
    for(i in seq(length(tmp))){
      if (names(tmp)[i]=='CID'){
        cids <- tmp[[i]]
        break
      }
    }
    return(cids)
  },
  warning = function(e) {
    print('Holy')
    return(xml.path)
  })
  return(cids)
}


CAS_to_SMILES <- function(cas){              # 이제 얻은 cid,cid,cid,cid,...를 url에 넣고 SMILES로 가져오는 작업
  xml.path <- paste0("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/",cas,"/property/CanonicalSMILES/XML")
  xml.raw <- read_xml(xml.path)                # url을 xml로 가져와서 node에 담고
  xml.node <- xml_children(xml.raw)
  xml.vector <- xml_find_all(xml.node, './*')  # 이렇게 하면 각 노드에 있는 line by line 값들을 가져올 수 있다.
  xml.text <- xml_text(xml.vector)
  return (xml.text[2])
}

CAS_to_iso_SMILES <- function(cas){              # 이제 얻은 cid,cid,cid,cid,...를 url에 넣고 SMILES로 가져오는 작업
  xml.path <- paste0("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/",cas,"/property/IsomericSMILES/XML")
  xml.raw <- read_xml(xml.path)                # url을 xml로 가져와서 node에 담고
  xml.node <- xml_children(xml.raw)
  xml.vector <- xml_find_all(xml.node, './*')  # 이렇게 하면 각 노드에 있는 line by line 값들을 가져올 수 있다.
  xml.text <- xml_text(xml.vector)
  return (xml.text[2])
}
SMILES_to_CID <- function(smiles){   # 염 제거한 SMILES -> CID 로 변환하는 작업이 필요하다. 이거는 한개 by 한개만 가능 
  xml.text <- tryCatch({
    xml.path <- paste0("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/",smiles,"/property/MolecularFormula/XML")
    xml.raw <- read_xml(xml.path)                # url을 xml로 가져와서 node에 담고
    xml.node <- xml_children(xml.raw)
    xml.vector <- xml_find_all(xml.node, './*')  # 이렇게 하면 각 노드에 있는 line by line 값들을 가져올 수 있다.
    xml.text <- xml_text(xml.vector)
  }, 
  error = function(e) { # 만약에 #이 있으면 에러가 나오게 되고, #은 url에서 인식못해서 특수문자 url encoding 해줘야한다.
    print(smiles)
    smiles <- URLencode(smiles, reserved = T)
    xml.path <- paste0("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/",smiles,"/property/MolecularFormula/XML")
    xml.raw <- read_xml(xml.path)                
    xml.node <- xml_children(xml.raw)
    xml.vector <- xml_find_all(xml.node, './*')  
    xml.text <- xml_text(xml.vector)
    return(xml.text)
  },
  warning = function(e) {
    print('holy')
  }
    )
  

  return (xml.text[1])
}

CID_to_TEXTS <- function(cid.list, cutoff){   # CID들을 하나의 url로 SMILES 묶어서 들고오기 위해서 'cid,cid,cid,cid' 꼴로 바꾸는 작업.
  if (cutoff>2000){                           # max url이 2000글자라서 그거 이내로 묶어와야한다
    print('MAX cutoff EXCEED!!')
    return ('None')
  }
  output <- c()
  cids <- ''
  for (i.cid in cid.list){
    if(i.cid != 'None' & length(i.cid) != 0){   # 문제없으면 cid를 ,로 분리해서 담는다
      cids <- paste0(cids,i.cid,',')
    }
    
    if (nchar(cids) > cutoff){
      cids <- gsub('.$','',cids)               # cutoff 넘으면 분리해서 list에 담는데, 마지막에 붙은 ',' 를 제거해주는 작업 ('.$' 이게 마지막을 뜻하는거임)
      output <- c(output,cids)
      cids <- ''                               # 담고나면 초기화
    }
  }
  output <- c(output,cids)                     # 마지막 남은 cid들을 담는다. 여기에도 ,(쉼표) 붙어있는지 한번 확인해보자
  return(output)
}

CID_to_SMILES <- function(cid.text){              # 이제 얻은 cid,cid,cid,cid,...를 url에 넣고 SMILES로 가져오는 작업
  xml.path <- paste0("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/",cid.text,"/property/CanonicalSMILES/XML")
  xml.raw <- read_xml(xml.path)                # url을 xml로 가져와서 node에 담고
  xml.node <- xml_children(xml.raw)
  dt.SMILES <- data.frame()
  for (i in seq(length(xml.node))){
    xml.vector <- xml_find_all(xml.node[i], './*')  # 이렇게 하면 각 노드에 있는 line by line 값들을 가져올 수 있다.
    xml.text <- xml_text(xml.vector)
    dt.SMILES <- rbind(dt.SMILES, xml.text)         # 한줄씩 data에 추가. (CID, SMILES) 이게 한줄
  }
  names(dt.SMILES) <- xml_name(xml.vector)
  return (dt.SMILES)
}

CID_to_iso_SMILES <- function(cid.text){              # 이제 얻은 cid,cid,cid,cid,...를 url에 넣고 SMILES로 가져오는 작업
  xml.path <- paste0("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/",cid.text,"/property/IsomericSMILES/XML")
  xml.raw <- read_xml(xml.path)                # url을 xml로 가져와서 node에 담고
  xml.node <- xml_children(xml.raw)
  dt.SMILES <- data.frame()
  for (i in seq(length(xml.node))){
    xml.vector <- xml_find_all(xml.node[i], './*')  # 이렇게 하면 각 노드에 있는 line by line 값들을 가져올 수 있다.
    xml.text <- xml_text(xml.vector)
    dt.SMILES <- rbind(dt.SMILES, xml.text)         # 한줄씩 data에 추가. (CID, SMILES) 이게 한줄
  }
  names(dt.SMILES) <- xml_name(xml.vector)
  return (dt.SMILES)
}

CID_to_MW <- function(cid.text){              # 이제 얻은 cid,cid,cid,cid,...를 url에 넣고 SMILES로 가져오는 작업
  xml.path <- paste0("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/",cid.text,"/property/MolecularWeight/XML")
  xml.raw <- read_xml(xml.path)                # url을 xml로 가져와서 node에 담고
  xml.node <- xml_children(xml.raw)
  dt.MW <- data.frame()
  for (i in seq(length(xml.node))){
    xml.vector <- xml_find_all(xml.node[i], './*')  # 이렇게 하면 각 노드에 있는 line by line 값들을 가져올 수 있다.
    xml.text <- xml_text(xml.vector)
    dt.MW <- rbind(dt.MW, xml.text)         # 한줄씩 data에 추가. (CID, SMILES) 이게 한줄
  }
  names(dt.MW) <- xml_name(xml.vector)
  return (dt.MW)
}


SMILES_to_SDF <- function(smiles,name){
  source.url <- paste0("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/",smiles,"/sdf")
  download.file(url = source.url, destfile = paste0(name,'.sdf'))
}

CAS_to_SDF <- function(cas,smiles,path){
  source.url <- paste0("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/",cas,"/sdf")
  download.file(url = source.url, destfile = paste0(path, i.cas,'.sdf'))
  return(c(cas,smiles))
}

CID_TEXT_to_SDF <- function(cid.text,name, path){
  source.url <- paste0("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/",cid.text,"/sdf")
  download.file(url = source.url, destfile = paste0(path, name,'.sdf'))
  return(NULL)
}



CID_to_LOGP <- function(cid.text){              # 이제 얻은 cid,cid,cid,cid,...를 url에 넣고 SMILES로 가져오는 작업
  xml.path <- paste0("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/",cid.text,"/property/XLogP/XML")
  xml.raw <- read_xml(xml.path)                # url을 xml로 가져와서 node에 담고
  xml.node <- xml_children(xml.raw)
  dt.logp <- data.frame()
  for (i in seq(length(xml.node))){
    xml.vector <- xml_find_all(xml.node[i], './*')  # 이렇게 하면 각 노드에 있는 line by line 값들을 가져올 수 있다.
    xml.text <- xml_text(xml.vector)
    dt.logp <- rbind(dt.logp, xml.text)         # 한줄씩 data에 추가. (CID, SMILES) 이게 한줄
  }
  names(dt.logp) <- xml_name(xml.vector)
  return (dt.logp)
}

properties <- c('MolecularWeight','CanonicalSMILES','IsomericSMILES','InChI','InChIKey',
                'IUPACName','Title','XLogP','ExactMass','MonoisotopicMass','TPSA','Complexity',
                'Charge','HBondDonorCount','HBondAcceptorCount','RotatableBondCount','HeavyAtomCount',
                'IsotopeAtomCount','AtomStereoCount','DefinedAtomStereoCount','UndefinedAtomStereoCount',
                'BondStereoCount','DefinedBondStereoCount','UndefinedBondStereoCount','CovalentUnitCount',
                'Volume3D','XStericQuadrupole3D','YStericQuadrupole3D','ZStericQuadrupole3D','FeatureCount3D',
                'FeatureAcceptorCount3D','FeatureDonorCount3D','FeatureAnionCount3D','FeatureCationCount3D',
                'FeatureRingCount3D','FeatureHydrophobeCount3D','ConformerModelRMSD3D','EffectiveRotorCount3D',
                'ConformerCount3D','Fingerprint2D')




