library(readxl)
source('ECx_mod.R')

dt <- read_excel('20230914_EC10 mixture 실험정보 for Deep-TSP_2023.xlsx',sheet='2023 complex mixture')

dt <- data.frame(dt)

myrow = data.frame()
index = 5
for (i in 1:nrow(dt)){
  if (is.na(dt[i,1])){
    next
  } else{
    name <- paste0('Mix ', index)
    row <- dt[i+1,5:8]
    row <- c(name, row)
    names(row) <- names(myrow)
    myrow <- rbind(myrow, row)
    names(myrow) <- c('Mixture', 'RM', 'a','b','r')
    index = index + 1
  }
}
head(myrow)

newdt <- read_excel('20230920_Mixture.xlsx')
names(myrow) <- names(newdt)
newdt <- rbind(newdt, myrow)
write.csv(newdt, '20230920_Mixture.csv')
