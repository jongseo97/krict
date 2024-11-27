# 모델 검증을 위한 R2 계산코드 작성 # - mwseo

# R2 구할 데이터 불러오기
## install.packages("readxl")
library(readxl)
library(writexl)
library(stringr)
library(hydroGOF)
library(mixtox)
#setwd("C:\Users\hkjin\Desktop\R2\input data")
#Data = as.data.frame(read_excel("A001_1.xlsx"))


Dir <- c("C:/Users/hkjin/Desktop/NSE/3pt/")
Output_FileInfo <- c("C:/Users/hkjin/Desktop/NSE/20230417_performance_result_3pt.csv")

#Dir <- c("C:/Users/mwseo/Desktop/R2/")
#Output_FileInfo <- c("C:/Users/mwseo/Desktop/R2/R2_result/20230327_model_R2_result.csv")
FileName <- list.files(Dir)
Dir_fileName <- c()

data.name <- c() #입력데이터 이름 확인을 위해 추가
final.model.nse <- c() #모든 데이터의 nse 결과 통합하기 위해 추가
final.model.rmse <- c() #모든 데이터의 rmse 결과 통합하기 위해 추가
final.model.slope <- c() #모든 데이터의 slope 결과 통합하기 위해 추가
final.model.name <- c()

eqs = c("Hill", "Hill_two", "Hill_three", "Hill_four", "Weibull", "Weibull_three",
        "Weibull_four", "Logit", "Logit_three", "Logit_four", "BCW", "BCL", "GL", 
        "Brain_Consens", "BCV", "Biphasic", "Hill_five")

model.fix = TRUE # slope, RM 고정을 위한 작업

#All file setup (확장자 .xlsx 파일만 필터하여 저장)
for (i in seq(FileName)) {
  if(str_detect(FileName[i], ".xlsx")) {
    Dir_fileName <- c(Dir_fileName, FileName[i])
  }
}
file_list <- paste0(Dir, Dir_fileName)




for (j in seq(file_list)) {
  
  if (str_detect(Dir_fileName[j], ".xlsx")) {
    
    print(file_list[j])
    
    model.data = read_excel(file_list[j])
    model.data <- as.data.frame(model.data) 
    
    model.data[model.data == "NA"] <- as.numeric(0) #NA를 0으로 처리
    #model.data[is.na(model.data)] <- 0 #결측치 0으로 처리

    
    #model.data의 column 순서 변경 시 for문 및 내부 수정 필요
    #1: Effect.Mix, 2:Observed, 3:Deep-TSP, 4:CA, 5:IA, 6:QSAR-TSP
    models.nse <- c()
    models.rmse <- c()
    models.slope <- c()
    models.name <- c()
    
    for (ai in 3:ncol(model.data)) {
      
      #calculate NSE
      nse <- NSE(model.data[, ai], model.data[,2])
      models.nse <- c(models.nse, nse)
      
      #calculate RMSE
      rmse <- rmse(model.data[, ai], model.data[, 2])
      models.rmse <- c(models.rmse, rmse)
      
    }
    
    #Exp 데이터도 추가하기 위해서 for문 분리함
    for (bi in 2:ncol(model.data)) {
      
      #calculate slope factor
      x <- model.data[,bi] #predicted conc of models
      y <- model.data[, 1] #Effect.Mix
      fit_r2 <- c() #최적의 rm 정보 도출을 위해 추가
      fit_param <- c() #최적의 rm 정보 도출을 위해 추가
      
      
      
      if(model.fix == TRUE) { 
        
        #Weibull model 고정
        eq <- "Weibull_three"
        fit <- tuneFit(x, y, eq)
        
        if(fit$sta[4] == 1.000001e+06) {
          fit_r2 <- c(fit_r2, 0) 
        } else {
          fit_r2 <- c(fit_r2, fit$sta[4])
        }
        temp_param <- c(fit$sta[1], fit$sta[2], fit$sta[3], 0, 0)
        
        fit_param <- rbind(fit_param, temp_param) #RM parameter 추가
        
        model <- eq
        param <- fit_param[which.max(fit_r2), ]
        slope <- param[1]
        models.slope <- c(models.slope, slope)
        models.name <-c(models.name, model)
        
        } else {
        
        for (aii in seq(length(eqs))) {
          
          eq <- eqs[aii]
          fit <- tuneFit(x, y, eq)
          
          if(eqs[aii] == "Hill") {
            if(fit$sta[3] == 1.000001e+06) {
              fit_r2 <- c(fit_r2, 0) 
            } else {
              fit_r2 <- c(fit_r2, fit$sta[3])
            }
            temp_param <- c(fit$sta[1], fit$sta[2], 0, 0, 0)
            
          } else if (eqs[aii] == "Hill_two") {
            if(fit$sta[3] == 1.000001e+06) {
              fit_r2 <- c(fit_r2, 0) 
            } else {
              fit_r2 <- c(fit_r2, fit$sta[3])
            }
            temp_param <- c(fit$sta[1], fit$sta[2], 0, 0, 0)
            
          } else if (eqs[aii] == "Hill_three") {
            if(fit$sta[4] == 1.000001e+06) {
              fit_r2 <- c(fit_r2, 0) 
            } else {
              fit_r2 <- c(fit_r2, fit$sta[4])
            }
            temp_param <- c(fit$sta[1], fit$sta[2], fit$sta[3], 0, 0)
            
          } else if (eqs[aii] == "Hill_four") {
            if(fit$sta[5] == 1.000001e+06) {
              fit_r2 <- c(fit_r2, 0) 
            } else {
              fit_r2 <- c(fit_r2, fit$sta[5])
            }
            temp_param <- c(fit$sta[1], fit$sta[2], fit$sta[3], fit$sta[4], 0)
            
          } else if (eqs[aii] == "Weibull") {
            if(fit$sta[3] == 1.000001e+06) {
              fit_r2 <- c(fit_r2, 0) 
            } else {
              fit_r2 <- c(fit_r2, fit$sta[3])
            }
            temp_param <- c(fit$sta[1], fit$sta[2], 0, 0, 0)
            
          } else if (eqs[aii] == "Weibull_three") {
            if(fit$sta[4] == 1.000001e+06) {
              fit_r2 <- c(fit_r2, 0) 
            } else {
              fit_r2 <- c(fit_r2, fit$sta[4])
            }
            temp_param <- c(fit$sta[1], fit$sta[2], fit$sta[3], 0, 0)
            
          } else if (eqs[aii] == "Weibull_four") {
            if(fit$sta[5] == 1.000001e+06) {
              fit_r2 <- c(fit_r2, 0) 
            } else {
              fit_r2 <- c(fit_r2, fit$sta[5])
            }
            temp_param <- c(fit$sta[1], fit$sta[2], fit$sta[3], fit$sta[4], 0)
            
          } else if (eqs[aii] == "Logit") {
            if(fit$sta[3] == 1.000001e+06) {
              fit_r2 <- c(fit_r2, 0) 
            } else {
              fit_r2 <- c(fit_r2, fit$sta[3])
            }
            temp_param <- c(fit$sta[1], fit$sta[2], 0, 0, 0)
            
          } else if (eqs[aii] == "Logit_three") {
            if(fit$sta[4] == 1.000001e+06) {
              fit_r2 <- c(fit_r2, 0) 
            } else {
              fit_r2 <- c(fit_r2, fit$sta[4])
            }
            temp_param <- c(fit$sta[1], fit$sta[2], fit$sta[3], 0, 0)
            
          } else if (eqs[aii] == "Logit_four") {
            if(fit$sta[5] == 1.000001e+06) {
              fit_r2 <- c(fit_r2, 0) 
            } else {
              fit_r2 <- c(fit_r2, fit$sta[5])
            }
            temp_param <- c(fit$sta[1], fit$sta[2], fit$sta[3], fit$sta[4], 0)
            
          } else if (eqs[aii] == "BCW") {
            if(fit$sta[4] == 1.000001e+06) {
              fit_r2 <- c(fit_r2, 0) 
            } else {
              fit_r2 <- c(fit_r2, fit$sta[4])
            }
            temp_param <- c(fit$sta[1], fit$sta[2], fit$sta[3], 0, 0)
            
          } else if (eqs[aii] == "BCL") {
            if(fit$sta[4] == 1.000001e+06) {
              fit_r2 <- c(fit_r2, 0) 
            } else {
              fit_r2 <- c(fit_r2, fit$sta[4])
            }
            temp_param <- c(fit$sta[1], fit$sta[2], fit$sta[3], 0, 0)
            
          } else if (eqs[aii] == "GL") {
            if(fit$sta[4] == 1.000001e+06) {
              fit_r2 <- c(fit_r2, 0) 
            } else {
              fit_r2 - c(fit_r2, fit$sta[4])
            }
            temp_param <- c(fit$sta[1], fit$sta[2], fit$sta[3], 0, 0)
            
          } else if (eqs[aii] == "Brain_Consens") {
            if(fit$sta[4] == 1.000001e+06) {
              fit_r2 <- c(fit_r2, 0) 
            } else {
              fit_r2 <- c(fit_r2, fit$sta[4])
            }
            temp_param <- c(fit$sta[1], fit$sta[2], fit$sta[3], 0, 0)
            
          } else if (eqs[aii] == "BCV") {
            if(fit$sta[5] == 1.000001e+06) {
              fit_r2 <- c(fit_r2, 0) 
            } else {
              fit_r2 <- c(fit_r2, fit$sta[5])
            }
            temp_param <- c(fit$sta[1], fit$sta[2], fit$sta[3], fit$sta[4], 0)
            
          } else if (eqs[aii] == "Biphasic") {
            if(fit$sta[6] == 1.000001e+06) {
              fit_r2 <- c(fit_r2, 0) 
            } else {
              fit_r2 <- c(fit_r2, fit$sta[6])
            }
            temp_param <- c(fit$sta[1], fit$sta[2], fit$sta[3], fit$sta[4], fit$sta[5])
            
          } else {
            if(fit$sta[6] == 1.000001e+06) {
              fit_r2 <- c(fit_r2, 0) 
            } else {
              fit_r2 <- c(fit_r2, fit$sta[6])
            }
            temp_param <- c(fit$sta[1], fit$sta[2], fit$sta[3], fit$sta[4], fit$sta[5])
          }
          
          fit_param <- rbind(fit_param, temp_param) #RM parameter 추가
          
        }
          
          model <- eqs[which.max(fit_r2)]
          param <- fit_param[which.max(fit_r2), ]
          slope <- param[1]
          models.slope <- c(models.slope, slope)
          models.name <-c(models.name, model)
          
      }
      
    }
    
    models.nse <- round(models.nse, 4)
    models.rmse <- round(models.rmse, 4)
    final.model.nse <- rbind(final.model.nse, models.nse)
    final.model.rmse <- rbind(final.model.rmse, models.rmse)
    final.model.slope <- rbind(final.model.slope, models.slope)
    final.model.name <- rbind(final.model.name, models.name)
    data.name <- c(data.name, gsub(".xlsx", "", Dir_fileName[j])) #입력 데이터 확인
    
  }
    
}

colnames(final.model.nse) <- c("Deep-TSP (NSE)", "CA (NSE)", "IA (NSE)", "QSAR-TSP (NSE)") #모델 순서에 따라 이름 변경 필요
colnames(final.model.rmse) <- c("Deep-TSP (RMSE)", "CA (RMSE)", "IA (RMSE)", "QSAR-TSP (RMSE)") #모델 순서에 따라 이름 변경 필요
colnames(final.model.slope) <- c("Exp (slope)" ,"Deep-TSP (slope)", "CA (slope)", "IA (slope)", "QSAR-TSP (slope)") #모델 순서에 따라 이름 변경 필요
colnames(final.model.name) <- c("Exp (RM)", "Deep-TSP (RM)", "CA (RM)", "IA (RM)", "QSAR-TSP (RM)") #모델 순서에 따라 이름 변경 필요


#merge data
#final.model.performance <- cbind(final.model.nse, final.model.rmse, final.model.slope, final.model.name) #-모두출력
final.model.performance <- cbind(final.model.nse, final.model.rmse) #- NSE, RMSE만 출력
rownames(final.model.performance) <- data.name
#write file
final.model.performance <- as.data.frame(final.model.performance)
write.csv(final.model.performance, file=Output_FileInfo)
