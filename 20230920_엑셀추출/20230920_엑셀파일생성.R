source('ECx_mod.R')
library(writexl)
dt <- read.csv('20230920_Mixture.csv')
dt <- dt[,-1]
head(dt)

mw <- c(1)
#effv <- c(0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9)
effv <- c(10,20,30,40,50,60,70,80,90)
ECx_mod(dt[1,2],as.numeric(as.vector(c(dt[1,3:5]))),effv, effv)

for (i in seq(1:nrow(dt))){
  row <- dt[i,]
  model <- dt[i,2]
  param <- dt[i,3:5]
  param <- as.numeric(as.vector(param))
  results <- ECx_mod(model, param, effv, mw)
  temp <- cbind(effv, as.vector(results))
  temp <- data.frame(temp)
  names(temp) <- c('Effect.Mix', 'Observed')
  name <- paste0('Mix_',i,'_exp.xlsx')
  write_xlsx(temp, name)
}


