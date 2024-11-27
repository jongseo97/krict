ECx_mod <- function(model, param, effv, MW){
  #calculate effect concentrations using associated inverse function
  if (missing(model) || missing (param) || missing (MW)) stop('argument missing')
  #if (missing(effv)) effv = 0.5
  #effv = 0.5
  if (is.vector(param)) param <- t(param)
  
  #effv <- sort(effv)
  #print(effv)
  
  
  ecx <- matrix(0, length(model), length(effv), length(MW))
  
  for (i in seq(model)){
    fun <- model[i]
    p <- param[i, ]
    #M <- MW[i, ] - MRA v1
    M <- MW[i]
    
    # DRC package 5개 RM 정보수식 // DRC-ftting을 위해 사용 - mwseo
    if(fun == 'Weibull_four')
      ec <- exp(log(-log(-(((effv-p[2])/(p[3]-p[2]))-1))) / p[1]) * p[4] 
    else if(fun == 'Asymptotic_three')
      ec <- -p[3]*log(1-((effv-p[1])/(p[2]-p[1])))
    else if(fun == 'Michaelis-Menten_three')
      ec <- -((p[3]*effv-p[1]*p[3]) / (effv-p[2]))
    else if(fun == 'Gompertz_four')
      ec <- (log(-log((effv-p[2])/(p[3]-p[2]))) / p[1]) + p[4]
    else if(fun == 'Logistic_five')
      ec <- (log((((p[3]-p[2])/(effv-p[2]))^(1/p[5]))-1)/p[1]) + p[4]
    
    
    #Hill three - sigmaplot 계산결과를 위해 수식 추가
    else if(fun == 'Hill') 
      ec <- p[1] / ((p[3] / effv - 1)^(1 / p[2]))
    #else if(fun == 'Chapman')
    #  ec <- p[3] - p[2] * log(-log(effv / p[1]))

    #else if (fun == "Hill")
    #  ec <- p[1] / ((1 / effv - 1)^(1 / p[2]))
    else if (fun == "Hill_two")
      ec <- p[1] * effv / (p[2] - effv)
    # <REVISED> # p[1] / (( ffv - 1)^(1 / p[2])) => p[3] / ((p[1] / effv - 1)^(1 / p[2]))
    else if (fun == "Hill_three")
      #ec <- ((-(p[3]^p[2]*effv)/(effv-p[1]))^(1/p[2]))
      ec <- p[3] / ((p[1] / effv - 1)^(1 / p[2]))    #original
    else if(fun == "Hill_four")
      ec <- p[1] / (((p[3] - p[4]) / (effv - p[4]) - 1)^(1 / p[2]))
    else if(fun == "Weibull")
      ec <- 10^((log(-log(1 - effv)) - p[1])/p[2]) # modified
      #ec <- exp(-(-log(log(-1 / (-1 + effv))) + p[1]) * log(10) / p[2]) #mixtox origin
    else if(fun == "Weibull_three")
      ec <- exp(-(-log(log(p[3] / (p[3] - effv))) + p[1]) * log(10) / p[2])
    #else if(fun == "Weibull_four")
    #  ec <- exp((log(log((-p[4] + p[3]) / (p[3] - effv))) - p[1]) * log(10) / p[2]) #mixtox origin
    else if (fun == "Logit")
      ec <- 10^((log(effv/(1-effv))-p[1])/p[2]) # modified
    #ec <- exp(-log(10) * (p[1] + log(-(-1 + effv) / (effv))) / p[2]) #mixtox origin
    else if(fun == "Logit_three")
      ec <- exp(-log(10) * (p[1] + log((p[3] - effv) / effv)) / p[2])
    else if(fun == "Logit_four")
      ec <- exp(-log(10) * (p[1] + log(-(p[3] - effv) / (p[4] - effv))) / p[2])
    else if (fun == "BCW")

      ec <- exp(log(-(p[1] * p[3] - p[2] - log(-log(1 - effv)) * p[3])/p[2])/p[3]) #mixtox origin
      #ec <- (p[3]/p[2]*(log(-log(1-effv))-p[1])+1)^(1/p[3]) #modified
    
    else if (fun == "BCL")
      ec <- exp(log(-(p[1] * p[3] - p[2] + log(-(-1 + effv)/effv) * p[3])/p[2])/p[3])
    
    else if (fun == "GL")
      ec <- exp(-log(10) * (p[1] + log(exp(-log(effv)/p[3]) - 1))/p[2]) #mixtox origin
      #ec <- 10^(-(log((1/effv)^(1/p[3])-1)+p[1])/p[2]) # modified
    
    
    
    
    
    
    
    
    # <ADDED> # J. Kim et al., 2014. Development of a Partial Least Squares-Based Integrated Addition Model for Predicting Mixture Toxicity. Human and Ecological Risk Assessment, 20: 174-200.
    else if (fun == "Probit")
      ec <- 10^((qnorm(effv, mean=0, sd=1) - p[1]) / p[2])
    else if (fun == "BCP")
      ec <- (p[3] / p[2] * (qnorm(effv, mean=0, sd=1) - p[1]) + 1)^(1 / p[3])
    else if (fun == "Sigmoid")
      ec <- p[3] - p[2] * log((p[1] - effv) / effv)
    else if (fun == "Logistic")
      ec <- p[3] *((p[1] - effv) / effv)^(1 / p[2])
    else if (fun == "Chapman")
      ec <- -(log(1 - (effv / p[1])^(1 / p[3])) / p[2])
    else if (fun == "Gompertz")
      ec <- p[3] - p[2] * log(-log(effv / p[1]))
    # <ADDED> #Weibull (2 parameters) equation described in drc package (refer to 'weibull2.R')
    else if (fun == "Weibull_drc")
      ec <- exp(((log(-log(1 - effv))) / p[1]) + log(p[2]))
    
    #1. Unit conversion from "mg/L" to "ug/L" (_mg/L_ug/L)#
    else if (fun == "Hill_three_mg/L_ug/L")
      ec <- (p[3] / (((p[1] / effv - 1)^(1 / p[2])))) * 1000
    else if (fun == "Weibull_mg/L_ug/L")
      ec <- (10^((log(-log(1 - effv)) - p[1])/p[2])) * 1000
    #ec <- (exp(-(-log(log(-1 / (-1 + effv))) + p[1]) * log(10) / p[2])) * 1000
    else if (fun == "Logit_mg/L_ug/L")
      ec <- (10^((log(effv/(1-effv))-p[1])/p[2])) * 1000
    #ec <- (exp(-log(10) * (p[1] + log(-(-1 + effv) / (effv))) / p[2])) * 1000
    else if (fun == "BCW_mg/L_ug/L")
      ec <- ((p[3]/p[2]*(log(-log(1-effv))-p[1])+1)^(1/p[3])) * 1000
    #ec <- (exp(log(-(p[1] * p[3] - p[2] - log(-log(1 - effv)) * p[3]) / p[2]) / p[3])) * 1000
    else if (fun == "BCL_mg/L_ug/L")
      ec <- (exp(log(-(p[1] * p[3] - p[2] + log(-(-1 + effv) / effv) * p[3]) / p[2]) / p[3])) * 1000
    else if (fun == "GL_mg/L_ug/L")
      ec <- (10^(-(log((1/effv)^(1/p[3])-1)+p[1])/p[2])) * 1000
    #ec <- (exp(-log(10) * (p[1] + log(exp(-log(effv) / p[3]) - 1)) / p[2])) * 1000
    else if (fun == "Probit_mg/L_ug/L")
      ec <- (10^((qnorm(effv, mean=0, sd=1) - p[1]) / p[2])) * 1000
    else if (fun == "BCP_mg/L_ug/L")
      ec <- ((p[3] / p[2] * (qnorm(effv, mean=0, sd=1) - p[1]) + 1)^(1 / p[3])) * 1000
    else if (fun == "Sigmoid_mg/L_ug/L")
      ec <- (p[3] - p[2] * log((p[1] - effv) / effv)) * 1000
    else if (fun == "Logistic_mg/L_ug/L")
      ec <- (p[3] *((p[1] - effv) / effv)^(1 / p[2])) * 1000
    else if (fun == "Chapman_mg/L_ug/L")
      ec <- (-(log(1 - (effv / p[1])^(1 / p[3])) / p[2])) * 1000
    else if (fun == "Gompertz_mg/L_ug/L")
      ec <- (p[3] - p[2] * log(-log(effv / p[1]))) * 1000
    
    #2. Unit conversion from "mg/L" to "mM" (_mg/L_mM)#
    else if (fun == "Hill_three_mg/L_mM")
      ec <- ((p[3] / (((p[1] / effv - 1)^(1 / p[2]))))) / M[1]
    else if (fun == "Weibull_mg/L_mM")
      ec <- (10^((log(-log(1 - effv)) - p[1])/p[2])) / M[1]
    #ec <- ((exp(-(-log(log(-1 / (-1 + effv))) + p[1]) * log(10) / p[2]))) / M[1]
    else if (fun == "Logit_mg/L_mM")
      ec <- (10^((log(effv/(1-effv))-p[1])/p[2])) / M[1]
    #ec <- ((exp(-log(10) * (p[1] + log(-(-1 + effv) / (effv))) / p[2]))) / M[1]
    else if (fun == "BCW_mg/L_mM")
      ec <- ((p[3]/p[2]*(log(-log(1-effv))-p[1])+1)^(1/p[3])) / M[1]
    #ec <- ((exp(log(-(p[1] * p[3] - p[2] - log(-log(1 - effv)) * p[3]) / p[2]) / p[3]))) / M[1]
    else if (fun == "BCL_mg/L_mM")
      ec <- ((exp(log(-(p[1] * p[3] - p[2] + log(-(-1 + effv) / effv) * p[3]) / p[2]) / p[3]))) / M[1]
    else if (fun == "GL_mg/L_mM")
      ec <- (10^(-(log((1/effv)^(1/p[3])-1)+p[1])/p[2])) / M[1]
    #ec <- ((exp(-log(10) * (p[1] + log(exp(-log(effv) / p[3]) - 1)) / p[2]))) / M[1]
    else if (fun == "Probit_mg/L_mM")
      ec <- ((10^((qnorm(effv, mean=0, sd=1) - p[1]) / p[2]))) / M[1]
    else if (fun == "BCP_mg/L_mM")
      ec <- (((p[3] / p[2] * (qnorm(effv, mean=0, sd=1) - p[1]) + 1)^(1 / p[3]))) / M[1]
    else if (fun == "Sigmoid_mg/L_mM")
      ec <- ((p[3] - p[2] * log((p[1] - effv) / effv))) / M[1]
    else if (fun == "Logistic_mg/L_mM")
      ec <- ((p[3] *((p[1] - effv) / effv)^(1 / p[2]))) / M[1]
    else if (fun == "Chapman_mg/L_mM")
      ec <- ((-(log(1 - (effv / p[1])^(1 / p[3])) / p[2]))) / M[1]
    else if (fun == "Gompertz_mg/L_mM")
      ec <- ((p[3] - p[2] * log(-log(effv / p[1])))) / M[1]
    
    #3. Unit conversion from "mg/L" to "uM" (_mg/L_uM)#
    else if (fun == "Hill_three_mg/L_uM")
      ec <- ((p[3] / (((p[1] / effv - 1)^(1 / p[2]))))) / M[1] * 1000
    else if (fun == "Weibull_mg/L_uM")
      ec <- (10^((log(-log(1 - effv)) - p[1])/p[2])) / M[1] * 1000
    #ec <- ((exp(-(-log(log(-1 / (-1 + effv))) + p[1]) * log(10) / p[2]))) / M[1] * 1000
    else if (fun == "Logit_mg/L_uM")
      ec <- (10^((log(effv/(1-effv))-p[1])/p[2])) / M[1] * 1000
    #ec <- ((exp(-log(10) * (p[1] + log(-(-1 + effv) / (effv))) / p[2]))) / M[1] * 1000
    else if (fun == "BCW_mg/L_uM")
      ec <- ((p[3]/p[2]*(log(-log(1-effv))-p[1])+1)^(1/p[3])) / M[1] * 1000
    #ec <- ((exp(log(-(p[1] * p[3] - p[2] - log(-log(1 - effv)) * p[3]) / p[2]) / p[3]))) / M[1] * 1000
    else if (fun == "BCL_mg/L_uM")
      ec <- ((exp(log(-(p[1] * p[3] - p[2] + log(-(-1 + effv) / effv) * p[3]) / p[2]) / p[3]))) / M[1] * 1000
    else if (fun == "GL_mg/L_uM")
      ec <- (10^(-(log((1/effv)^(1/p[3])-1)+p[1])/p[2])) / M[1] * 1000
    #ec <- ((exp(-log(10) * (p[1] + log(exp(-log(effv) / p[3]) - 1)) / p[2]))) / M[1] * 1000
    else if (fun == "Probit_mg/L_uM")
      ec <- ((10^((qnorm(effv, mean=0, sd=1) - p[1]) / p[2]))) / M[1] * 1000
    else if (fun == "BCP_mg/L_uM")
      ec <- (((p[3] / p[2] * (qnorm(effv, mean=0, sd=1) - p[1]) + 1)^(1 / p[3]))) / M[1] * 1000
    else if (fun == "Sigmoid_mg/L_uM")
      ec <- ((p[3] - p[2] * log((p[1] - effv) / effv))) / M[1] * 1000
    else if (fun == "Logistic_mg/L_uM")
      ec <- ((p[3] *((p[1] - effv) / effv)^(1 / p[2]))) / M[1] * 1000
    else if (fun == "Chapman_mg/L_uM")
      ec <- ((-(log(1 - (effv / p[1])^(1 / p[3])) / p[2]))) / M[1] * 1000
    else if (fun == "Gompertz_mg/L_uM")
      ec <- ((p[3] - p[2] * log(-log(effv / p[1])))) / M[1] * 1000
    
    #4. Unit conversion from "mg/L" to "nM" (_mg/L_nM)#
    else if (fun == "Hill_three_mg/L_nM")
      ec <- ((p[3] / (((p[1] / effv - 1)^(1 / p[2]))))) / M[1] * 1000000
    else if (fun == "Weibull_mg/L_nM")
      ec <- (10^((log(-log(1 - effv)) - p[1])/p[2])) / M[1] * 1000000
    #ec <- ((exp(-(-log(log(-1 / (-1 + effv))) + p[1]) * log(10) / p[2]))) / M[1] * 1000000
    else if (fun == "Logit_mg/L_nM")
      ec <- (10^((log(effv/(1-effv))-p[1])/p[2]) / M[1]) * 1000000
    #ec <- ((exp(-log(10) * (p[1] + log(-(-1 + effv) / (effv))) / p[2]))) / M[1] * 1000000
    else if (fun == "BCW_mg/L_nM")
      ec <- ((p[3]/p[2]*(log(-log(1-effv))-p[1])+1)^(1/p[3])) / M[1] * 1000000
    #ec <- ((exp(log(-(p[1] * p[3] - p[2] - log(-log(1 - effv)) * p[3]) / p[2]) / p[3]))) / M[1] * 1000000
    else if (fun == "BCL_mg/L_nM")
      ec <- ((exp(log(-(p[1] * p[3] - p[2] + log(-(-1 + effv) / effv) * p[3]) / p[2]) / p[3]))) / M[1] * 1000000
    else if (fun == "GL_mg/L_nM")
      ec <- (10^(-(log((1/effv)^(1/p[3])-1)+p[1])/p[2])) / M[1] * 1000000
    #ec <- ((exp(-log(10) * (p[1] + log(exp(-log(effv) / p[3]) - 1)) / p[2]))) / M[1] * 1000000
    else if (fun == "Probit_mg/L_nM")
      ec <- ((10^((qnorm(effv, mean=0, sd=1) - p[1]) / p[2]))) / M[1] * 1000000
    else if (fun == "BCP_mg/L_nM")
      ec <- (((p[3] / p[2] * (qnorm(effv, mean=0, sd=1) - p[1]) + 1)^(1 / p[3]))) / M[1] * 1000000
    else if (fun == "Sigmoid_mg/L_nM")
      ec <- ((p[3] - p[2] * log((p[1] - effv) / effv))) / M[1] * 1000000
    else if (fun == "Logistic_mg/L_nM")
      ec <- ((p[3] *((p[1] - effv) / effv)^(1 / p[2]))) / M[1] * 1000000
    else if (fun == "Chapman_mg/L_nM")
      ec <- ((-(log(1 - (effv / p[1])^(1 / p[3])) / p[2]))) / M[1] * 1000000
    else if (fun == "Gompertz_mg/L_nM")
      ec <- ((p[3] - p[2] * log(-log(effv / p[1])))) / M[1] * 1000000
    
    #5. Unit conversion from "ug/L" to "mg/L" (_ug/L_mg/L)#
    else if (fun == "Hill_three_ug/L_mg/L")
      ec <- ((p[3] / (((p[1] / effv - 1)^(1 / p[2]))))) / 1000
    else if (fun == "Weibull_ug/L_mg/L")
      ec <- (10^((log(-log(1 - effv)) - p[1])/p[2])) / 1000
    #ec <- ((exp(-(-log(log(-1 / (-1 + effv))) + p[1]) * log(10) / p[2]))) / 1000
    else if (fun == "Logit_ug/L_mg/L")
      ec <- (10^((log(effv/(1-effv))-p[1])/p[2])) / 1000
    #ec <- ((exp(-log(10) * (p[1] + log(-(-1 + effv) / (effv))) / p[2]))) / 1000
    else if (fun == "BCW_ug/L_mg/L")
      ec <- ((p[3]/p[2]*(log(-log(1-effv))-p[1])+1)^(1/p[3])) / 1000
    #ec <- ((exp(log(-(p[1] * p[3] - p[2] - log(-log(1 - effv)) * p[3]) / p[2]) / p[3]))) / 1000
    else if (fun == "BCL_ug/L_mg/L")
      ec <- ((exp(log(-(p[1] * p[3] - p[2] + log(-(-1 + effv) / effv) * p[3]) / p[2]) / p[3]))) / 1000
    else if (fun == "GL_ug/L_mg/L")
      ec <- (10^(-(log((1/effv)^(1/p[3])-1)+p[1])/p[2])) / 1000
    #ec <- ((exp(-log(10) * (p[1] + log(exp(-log(effv) / p[3]) - 1)) / p[2]))) / 1000
    else if (fun == "Probit_ug/L_mg/L")
      ec <- ((10^((qnorm(effv, mean=0, sd=1) - p[1]) / p[2]))) / 1000
    else if (fun == "BCP_ug/L_mg/L")
      ec <- (((p[3] / p[2] * (qnorm(effv, mean=0, sd=1) - p[1]) + 1)^(1 / p[3]))) / 1000
    else if (fun == "Sigmoid_ug/L_mg/L")
      ec <- ((p[3] - p[2] * log((p[1] - effv) / effv))) / 1000
    else if (fun == "Logistic_ug/L_mg/L")
      ec <- ((p[3] *((p[1] - effv) / effv)^(1 / p[2]))) / 1000
    else if (fun == "Chapman_ug/L_mg/L")
      ec <- ((-(log(1 - (effv / p[1])^(1 / p[3])) / p[2]))) / 1000
    else if (fun == "Gompertz_ug/L_mg/L")
      ec <- ((p[3] - p[2] * log(-log(effv / p[1])))) / 1000
    
    #6. Unit conversion from "ug/L" to "mM" (_ug/L_mM)#
    else if (fun == "Hill_three_ug/L_mM")
      ec <- ((p[3] / (((p[1] / effv - 1)^(1 / p[2]))))) / M[1] / 1000
    else if (fun == "Weibull_ug/L_mM")
      ec <- (10^((log(-log(1 - effv)) - p[1])/p[2])) / M[1] / 1000
    #ec <- ((exp(-(-log(log(-1 / (-1 + effv))) + p[1]) * log(10) / p[2]))) / M[1] / 1000
    else if (fun == "Logit_ug/L_mM")
      ec <- (10^((log(effv/(1-effv))-p[1])/p[2])) / M[1] / 1000
    #ec <- ((exp(-log(10) * (p[1] + log(-(-1 + effv) / (effv))) / p[2]))) / M[1] / 1000
    else if (fun == "BCW_ug/L_mM")
      ec <- ((p[3]/p[2]*(log(-log(1-effv))-p[1])+1)^(1/p[3])) / M[1] / 1000
    #ec <- ((exp(log(-(p[1] * p[3] - p[2] - log(-log(1 - effv)) * p[3]) / p[2]) / p[3]))) / M[1] / 1000
    else if (fun == "BCL_ug/L_mM")
      ec <- ((exp(log(-(p[1] * p[3] - p[2] + log(-(-1 + effv) / effv) * p[3]) / p[2]) / p[3]))) / M[1] / 1000
    else if (fun == "GL_ug/L_mM")
      ec <- (10^(-(log((1/effv)^(1/p[3])-1)+p[1])/p[2])) / M[1] / 1000
    #ec <- ((exp(-log(10) * (p[1] + log(exp(-log(effv) / p[3]) - 1)) / p[2]))) / M[1] / 1000
    else if (fun == "Probit_ug/L_mM")
      ec <- ((10^((qnorm(effv, mean=0, sd=1) - p[1]) / p[2]))) / M[1] / 1000
    else if (fun == "BCP_ug/L_mM")
      ec <- (((p[3] / p[2] * (qnorm(effv, mean=0, sd=1) - p[1]) + 1)^(1 / p[3]))) / M[1] / 1000
    else if (fun == "Sigmoid_ug/L_mM")
      ec <- ((p[3] - p[2] * log((p[1] - effv) / effv))) / M[1] / 1000
    else if (fun == "Logistic_ug/L_mM")
      ec <- ((p[3] *((p[1] - effv) / effv)^(1 / p[2]))) / M[1] / 1000
    else if (fun == "Chapman_ug/L_mM")
      ec <- ((-(log(1 - (effv / p[1])^(1 / p[3])) / p[2]))) / M[1] / 1000
    else if (fun == "Gompertz_ug/L_mM")
      ec <- ((p[3] - p[2] * log(-log(effv / p[1])))) / M[1] / 1000
    
    #7. Unit conversion from "ug/L" to "uM" (_ug/L_uM)#
    else if (fun == "Hill_three_ug/L_uM")
      ec <- ((p[3] / (((p[1] / effv - 1)^(1 / p[2]))))) / M[1]
    else if (fun == "Weibull_ug/L_uM")
      ec <- (10^((log(-log(1 - effv)) - p[1])/p[2])) / M[1]
    #ec <- ((exp(-(-log(log(-1 / (-1 + effv))) + p[1]) * log(10) / p[2]))) / M[1]
    else if (fun == "Logit_ug/L_uM")
      ec <- (10^((log(effv/(1-effv))-p[1])/p[2])) / M[1]
    #ec <- ((exp(-log(10) * (p[1] + log(-(-1 + effv) / (effv))) / p[2]))) / M[1]
    else if (fun == "BCW_ug/L_uM")
      ec <- ((p[3]/p[2]*(log(-log(1-effv))-p[1])+1)^(1/p[3])) / M[1]
    #ec <- ((exp(log(-(p[1] * p[3] - p[2] - log(-log(1 - effv)) * p[3]) / p[2]) / p[3]))) / M[1]
    else if (fun == "BCL_ug/L_uM")
      ec <- ((exp(log(-(p[1] * p[3] - p[2] + log(-(-1 + effv) / effv) * p[3]) / p[2]) / p[3]))) / M[1]
    else if (fun == "GL_ug/L_uM")
      ec <- (10^(-(log((1/effv)^(1/p[3])-1)+p[1])/p[2])) / M[1]
    #ec <- ((exp(-log(10) * (p[1] + log(exp(-log(effv) / p[3]) - 1)) / p[2]))) / M[1]
    else if (fun == "Probit_ug/L_uM")
      ec <- ((10^((qnorm(effv, mean=0, sd=1) - p[1]) / p[2]))) / M[1]
    else if (fun == "BCP_ug/L_uM")
      ec <- (((p[3] / p[2] * (qnorm(effv, mean=0, sd=1) - p[1]) + 1)^(1 / p[3]))) / M[1]
    else if (fun == "Sigmoid_ug/L_uM")
      ec <- ((p[3] - p[2] * log((p[1] - effv) / effv))) / M[1]
    else if (fun == "Logistic_ug/L_uM")
      ec <- ((p[3] *((p[1] - effv) / effv)^(1 / p[2]))) / M[1]
    else if (fun == "Chapman_ug/L_uM")
      ec <- ((-(log(1 - (effv / p[1])^(1 / p[3])) / p[2]))) / M[1]
    else if (fun == "Gompertz_ug/L_uM")
      ec <- ((p[3] - p[2] * log(-log(effv / p[1])))) / M[1]
    
    #8. Unit conversion from "ug/L" to "nM" (_ug/L_nM)#
    else if (fun == "Hill_three_ug/L_nM")
      ec <- ((p[3] / (((p[1] / effv - 1)^(1 / p[2]))))) / M[1] * 1000
    else if (fun == "Weibull_ug/L_nM")
      ec <- (10^((log(-log(1 - effv)) - p[1])/p[2])) / M[1] * 1000
    #ec <- ((exp(-(-log(log(-1 / (-1 + effv))) + p[1]) * log(10) / p[2]))) / M[1] * 1000
    else if (fun == "Logit_ug/L_nM")
      ec <- (10^((log(effv/(1-effv))-p[1])/p[2])) / M[1] * 1000
    #ec <- ((exp(-log(10) * (p[1] + log(-(-1 + effv) / (effv))) / p[2]))) / M[1] * 1000
    else if (fun == "BCW_ug/L_nM")
      ec <- ((p[3]/p[2]*(log(-log(1-effv))-p[1])+1)^(1/p[3])) / M[1] * 1000
    #ec <- ((exp(log(-(p[1] * p[3] - p[2] - log(-log(1 - effv)) * p[3]) / p[2]) / p[3]))) / M[1] * 1000
    else if (fun == "BCL_ug/L_nM")
      ec <- ((exp(log(-(p[1] * p[3] - p[2] + log(-(-1 + effv) / effv) * p[3]) / p[2]) / p[3]))) / M[1] * 1000
    else if (fun == "GL_ug/L_nM")
      ec <- (10^(-(log((1/effv)^(1/p[3])-1)+p[1])/p[2])) / M[1] * 1000
    #ec <- ((exp(-log(10) * (p[1] + log(exp(-log(effv) / p[3]) - 1)) / p[2]))) / M[1] * 1000
    else if (fun == "Probit_ug/L_nM")
      ec <- ((10^((qnorm(effv, mean=0, sd=1) - p[1]) / p[2]))) / M[1] * 1000
    else if (fun == "BCP_ug/L_nM")
      ec <- (((p[3] / p[2] * (qnorm(effv, mean=0, sd=1) - p[1]) + 1)^(1 / p[3]))) / M[1] * 1000
    else if (fun == "Sigmoid_ug/L_nM")
      ec <- ((p[3] - p[2] * log((p[1] - effv) / effv))) / M[1] * 1000
    else if (fun == "Logistic_ug/L_nM")
      ec <- ((p[3] *((p[1] - effv) / effv)^(1 / p[2]))) / M[1] * 1000
    else if (fun == "Chapman_ug/L_nM")
      ec <- ((-(log(1 - (effv / p[1])^(1 / p[3])) / p[2]))) / M[1] * 1000
    else if (fun == "Gompertz_ug/L_nM")
      ec <- ((p[3] - p[2] * log(-log(effv / p[1])))) / M[1] * 1000
    
    #9. Unit conversion from "mM" to "mg/L" (_mM_mg/L)#
    else if (fun == "Hill_three_mM_mg/L")
      ec <- ((p[3] / (((p[1] / effv - 1)^(1 / p[2]))))) * M[1]
    else if (fun == "Weibull_mM_mg/L")
      ec <- (10^((log(-log(1 - effv)) - p[1])/p[2])) * M[1]
    #ec <- ((exp(-(-log(log(-1 / (-1 + effv))) + p[1]) * log(10) / p[2]))) * M[1]
    else if (fun == "Logit_mM_mg/L")
      ec <- (10^((log(effv/(1-effv))-p[1])/p[2])) * M[1]
    #ec <- ((exp(-log(10) * (p[1] + log(-(-1 + effv) / (effv))) / p[2]))) * M[1]
    else if (fun == "BCW_mM_mg/L")
      ec <- ((p[3]/p[2]*(log(-log(1-effv))-p[1])+1)^(1/p[3])) * M[1]
    #ec <- ((exp(log(-(p[1] * p[3] - p[2] - log(-log(1 - effv)) * p[3]) / p[2]) / p[3]))) * M[1]
    else if (fun == "BCL_mM_mg/L")
      ec <- ((exp(log(-(p[1] * p[3] - p[2] + log(-(-1 + effv) / effv) * p[3]) / p[2]) / p[3]))) * M[1]
    else if (fun == "GL_mM_mg/L")
      ec <- (10^(-(log((1/effv)^(1/p[3])-1)+p[1])/p[2])) * M[1]
    #ec <- ((exp(-log(10) * (p[1] + log(exp(-log(effv) / p[3]) - 1)) / p[2]))) * M[1]
    else if (fun == "Probit_mM_mg/L")
      ec <- ((10^((qnorm(effv, mean=0, sd=1) - p[1]) / p[2]))) * M[1]
    else if (fun == "BCP_mM_mg/L")
      ec <- (((p[3] / p[2] * (qnorm(effv, mean=0, sd=1) - p[1]) + 1)^(1 / p[3]))) * M[1]
    else if (fun == "Sigmoid_mM_mg/L")
      ec <- ((p[3] - p[2] * log((p[1] - effv) / effv))) * M[1]
    else if (fun == "Logistic_mM_mg/L")
      ec <- ((p[3] *((p[1] - effv) / effv)^(1 / p[2]))) * M[1]
    else if (fun == "Chapman_mM_mg/L")
      ec <- ((-(log(1 - (effv / p[1])^(1 / p[3])) / p[2]))) * M[1]
    else if (fun == "Gompertz_mM_mg/L")
      ec <- ((p[3] - p[2] * log(-log(effv / p[1])))) * M[1]
    
    #10. Unit conversion from "mM" to "ug/L" (_mM_ug/L)#
    else if (fun == "Hill_three_mM_ug/L")
      ec <- ((p[3] / (((p[1] / effv - 1)^(1 / p[2]))))) * M[1] * 1000
    else if (fun == "Weibull_mM_ug/L")
      ec <- (10^((log(-log(1 - effv)) - p[1])/p[2])) * M[1] * 1000
    #ec <- ((exp(-(-log(log(-1 / (-1 + effv))) + p[1]) * log(10) / p[2]))) * M[1] * 1000
    else if (fun == "Logit_mM_ug/L")
      ec <- (10^((log(effv/(1-effv))-p[1])/p[2])) * M[1] * 1000
    #ec <- ((exp(-log(10) * (p[1] + log(-(-1 + effv) / (effv))) / p[2]))) * M[1] * 1000
    else if (fun == "BCW_mM_ug/L")
      ec <- ((p[3]/p[2]*(log(-log(1-effv))-p[1])+1)^(1/p[3])) * M[1] * 1000
    #ec <- ((exp(log(-(p[1] * p[3] - p[2] - log(-log(1 - effv)) * p[3]) / p[2]) / p[3]))) * M[1] * 1000
    else if (fun == "BCL_mM_ug/L")
      ec <- ((exp(log(-(p[1] * p[3] - p[2] + log(-(-1 + effv) / effv) * p[3]) / p[2]) / p[3]))) * M[1] * 1000
    else if (fun == "GL_mM_ug/L")
      ec <- (10^(-(log((1/effv)^(1/p[3])-1)+p[1])/p[2])) * M[1] * 1000
    #ec <- ((exp(-log(10) * (p[1] + log(exp(-log(effv) / p[3]) - 1)) / p[2]))) * M[1] * 1000
    else if (fun == "Probit_mM_ug/L")
      ec <- ((10^((qnorm(effv, mean=0, sd=1) - p[1]) / p[2]))) * M[1] * 1000
    else if (fun == "BCP_mM_ug/L")
      ec <- (((p[3] / p[2] * (qnorm(effv, mean=0, sd=1) - p[1]) + 1)^(1 / p[3]))) * M[1] * 1000
    else if (fun == "Sigmoid_mM_ug/L")
      ec <- ((p[3] - p[2] * log((p[1] - effv) / effv))) * M[1] * 1000
    else if (fun == "Logistic_mM_ug/L")
      ec <- ((p[3] *((p[1] - effv) / effv)^(1 / p[2]))) * M[1] * 1000
    else if (fun == "Chapman_mM_ug/L")
      ec <- ((-(log(1 - (effv / p[1])^(1 / p[3])) / p[2]))) * M[1] * 1000
    else if (fun == "Gompertz_mM_ug/L")
      ec <- ((p[3] - p[2] * log(-log(effv / p[1])))) * M[1] * 1000
    
    #11. Unit conversion from "mM" to "uM" (_mM_uM)#
    else if (fun == "Hill_three_mM_uM")
      ec <- (p[3] / (((p[1] / effv - 1)^(1 / p[2])))) * 1000
    else if (fun == "Weibull_mM_uM")
      ec <- (10^((log(-log(1 - effv)) - p[1])/p[2])) * 1000
    #ec <- (exp(-(-log(log(-1 / (-1 + effv))) + p[1]) * log(10) / p[2])) * 1000
    else if (fun == "Logit_mM_uM")
      ec <- (10^((log(effv/(1-effv))-p[1])/p[2])) * 1000
    #ec <- (exp(-log(10) * (p[1] + log(-(-1 + effv) / (effv))) / p[2])) * 1000
    else if (fun == "BCW_mM_uM")
      ec <- ((p[3]/p[2]*(log(-log(1-effv))-p[1])+1)^(1/p[3])) * 1000
    #ec <- (exp(log(-(p[1] * p[3] - p[2] - log(-log(1 - effv)) * p[3]) / p[2]) / p[3])) * 1000
    else if (fun == "BCL_mM_uM")
      ec <- (exp(log(-(p[1] * p[3] - p[2] + log(-(-1 + effv) / effv) * p[3]) / p[2]) / p[3])) * 1000
    else if (fun == "GL_mM_uM")
      ec <- (10^(-(log((1/effv)^(1/p[3])-1)+p[1])/p[2])) * 1000
    #ec <- (exp(-log(10) * (p[1] + log(exp(-log(effv) / p[3]) - 1)) / p[2])) * 1000
    else if (fun == "Probit_mM_uM")
      ec <- (10^((qnorm(effv, mean=0, sd=1) - p[1]) / p[2])) * 1000
    else if (fun == "BCP_mM_uM")
      ec <- ((p[3] / p[2] * (qnorm(effv, mean=0, sd=1) - p[1]) + 1)^(1 / p[3])) * 1000
    else if (fun == "Sigmoid_mM_uM")
      ec <- (p[3] - p[2] * log((p[1] - effv) / effv)) * 1000
    else if (fun == "Logistic_mM_uM")
      ec <- (p[3] *((p[1] - effv) / effv)^(1 / p[2])) * 1000
    else if (fun == "Chapman_mM_uM")
      ec <- (-(log(1 - (effv / p[1])^(1 / p[3])) / p[2])) * 1000
    else if (fun == "Gompertz_mM_uM")
      ec <- (p[3] - p[2] * log(-log(effv / p[1]))) * 1000
    
    
    #12. Unit conversion from "mM" to "nM" (_mM_nM)# - 수정 mwseo
    else if (fun == "Hill_three_mM_nM")
      ec <- (p[3] / (((p[1] / effv - 1)^(1 / p[2])))) * 1000000
    else if (fun == "Weibull_mM_nM")
      ec <- (10^((log(-log(1 - effv)) - p[1])/p[2])) * 1000000
    #ec <- (exp(-(-log(log(-1 / (-1 + effv))) + p[1]) * log(10) / p[2])) * 1000000
    else if (fun == "Logit_mM_nM")
      ec <- (10^((log(effv/(1-effv))-p[1])/p[2])) * 1000000
    #ec <- (exp(-log(10) * (p[1] + log(-(-1 + effv) / (effv))) / p[2])) * 1000000
    else if (fun == "BCW_mM_nM")
      ec <- ((p[3]/p[2]*(log(-log(1-effv))-p[1])+1)^(1/p[3])) * 1000000
    #ec <- (exp(log(-(p[1] * p[3] - p[2] - log(-log(1 - effv)) * p[3]) / p[2]) / p[3])) * 1000000
    else if (fun == "BCL_mM_nM")
      ec <- (exp(log(-(p[1] * p[3] - p[2] + log(-(-1 + effv) / effv) * p[3]) / p[2]) / p[3])) * 1000000
    else if (fun == "GL_mM_nM")
      ec <- (10^(-(log((1/effv)^(1/p[3])-1)+p[1])/p[2])) * 1000000
    #ec <- (exp(-log(10) * (p[1] + log(exp(-log(effv) / p[3]) - 1)) / p[2])) * 1000000
    else if (fun == "Probit_mM_nM")
      ec <- (10^((qnorm(effv, mean=0, sd=1) - p[1]) / p[2])) * 1000000
    else if (fun == "BCP_mM_nM")
      ec <- ((p[3] / p[2] * (qnorm(effv, mean=0, sd=1) - p[1]) + 1)^(1 / p[3])) * 1000000
    else if (fun == "Sigmoid_mM_nM")
      ec <- (p[3] - p[2] * log((p[1] - effv) / effv)) * 1000000
    else if (fun == "Logistic_mM_nM")
      ec <- (p[3] *((p[1] - effv) / effv)^(1 / p[2])) * 1000000
    else if (fun == "Chapman_mM_nM")
      ec <- (-(log(1 - (effv / p[1])^(1 / p[3])) / p[2])) * 1000000
    else if (fun == "Gompertz_mM_nM")
      ec <- (p[3] - p[2] * log(-log(effv / p[1]))) * 1000000
    
    
    #13. Unit conversion from "uM" to "mg/L" (_uM_mg/L)#
    else if (fun == "Hill_three_uM_mg/L")
      ec <- (((p[3] / (((p[1] / effv - 1)^(1 / p[2]))))) * M[1] ) / 1000
    else if (fun == "Weibull_uM_mg/L")
      ec <- ((10^((log(-log(1 - effv)) - p[1])/p[2])) * M[1]) / 1000
    #ec <- (((exp(-(-log(log(-1 / (-1 + effv))) + p[1]) * log(10) / p[2]))) * M[1] ) / 1000
    else if (fun == "Logit_uM_mg/L")
      ec <- ((10^((log(effv/(1-effv))-p[1])/p[2])) * M[1]) / 1000
    #ec <- (((exp(-log(10) * (p[1] + log(-(-1 + effv) / (effv))) / p[2]))) * M[1] ) / 1000
    else if (fun == "BCW_uM_mg/L")
      ec <- (((p[3]/p[2]*(log(-log(1-effv))-p[1])+1)^(1/p[3])) * M[1]) / 1000
    #ec <- (((exp(log(-(p[1] * p[3] - p[2] - log(-log(1 - effv)) * p[3]) / p[2]) / p[3]))) * M[1] ) / 1000
    else if (fun == "BCL_uM_mg/L")
      ec <- (((exp(log(-(p[1] * p[3] - p[2] + log(-(-1 + effv) / effv) * p[3]) / p[2]) / p[3]))) * M[1] ) / 1000
    else if (fun == "GL_uM_mg/L")
      ec <- ((10^(-(log((1/effv)^(1/p[3])-1)+p[1])/p[2])) * M[1]) / 1000
    #ec <- (((exp(-log(10) * (p[1] + log(exp(-log(effv) / p[3]) - 1)) / p[2]))) * M[1] ) / 1000
    else if (fun == "Probit_uM_mg/L")
      ec <- (((10^((qnorm(effv, mean=0, sd=1) - p[1]) / p[2]))) * M[1] ) / 1000
    else if (fun == "BCP_uM_mg/L")
      ec <- ((((p[3] / p[2] * (qnorm(effv, mean=0, sd=1) - p[1]) + 1)^(1 / p[3]))) * M[1] ) / 1000
    else if (fun == "Sigmoid_uM_mg/L")
      ec <- (((p[3] - p[2] * log((p[1] - effv) / effv))) * M[1] ) / 1000
    else if (fun == "Logistic_uM_mg/L")
      ec <- (((p[3] *((p[1] - effv) / effv)^(1 / p[2]))) * M[1] ) / 1000
    else if (fun == "Chapman_uM_mg/L")
      ec <- (((-(log(1 - (effv / p[1])^(1 / p[3])) / p[2]))) * M[1] ) / 1000
    else if (fun == "Gompertz_uM_mg/L")
      ec <- (((p[3] - p[2] * log(-log(effv / p[1])))) * M[1] ) / 1000
    
    #14. Unit conversion from "uM" to "ug/L" (_uM_ug/L)#
    else if (fun == "Hill_three_uM_ug/L")
      ec <- ((p[3] / (((p[1] / effv - 1)^(1 / p[2]))))) * M[1]
    else if (fun == "Weibull_uM_ug/L")
      ec <- (10^((log(-log(1 - effv)) - p[1])/p[2])) * M[1]
    #ec <- ((exp(-(-log(log(-1 / (-1 + effv))) + p[1]) * log(10) / p[2]))) * M[1]
    else if (fun == "Logit_uM_ug/L")
      ec <- (10^((log(effv/(1-effv))-p[1])/p[2])) * M[1]
    #ec <- ((exp(-log(10) * (p[1] + log(-(-1 + effv) / (effv))) / p[2]))) * M[1]
    else if (fun == "BCW_uM_ug/L")
      ec <- ((p[3]/p[2]*(log(-log(1-effv))-p[1])+1)^(1/p[3])) * M[1]
    #ec <- ((exp(log(-(p[1] * p[3] - p[2] - log(-log(1 - effv)) * p[3]) / p[2]) / p[3]))) * M[1]
    else if (fun == "BCL_uM_ug/L")
      ec <- ((exp(log(-(p[1] * p[3] - p[2] + log(-(-1 + effv) / effv) * p[3]) / p[2]) / p[3]))) * M[1]
    else if (fun == "GL_uM_ug/L")
      ec <- (10^(-(log((1/effv)^(1/p[3])-1)+p[1])/p[2])) * M[1]
    #ec <- ((exp(-log(10) * (p[1] + log(exp(-log(effv) / p[3]) - 1)) / p[2]))) * M[1]
    else if (fun == "Probit_uM_ug/L")
      ec <- ((10^((qnorm(effv, mean=0, sd=1) - p[1]) / p[2]))) * M[1]
    else if (fun == "BCP_uM_ug/L")
      ec <- (((p[3] / p[2] * (qnorm(effv, mean=0, sd=1) - p[1]) + 1)^(1 / p[3]))) * M[1]
    else if (fun == "Sigmoid_uM_ug/L")
      ec <- ((p[3] - p[2] * log((p[1] - effv) / effv))) * M[1]
    else if (fun == "Logistic_uM_ug/L")
      ec <- ((p[3] *((p[1] - effv) / effv)^(1 / p[2]))) * M[1]
    else if (fun == "Chapman_uM_ug/L")
      ec <- ((-(log(1 - (effv / p[1])^(1 / p[3])) / p[2]))) * M[1]
    else if (fun == "Gompertz_uM_ug/L")
      ec <- ((p[3] - p[2] * log(-log(effv / p[1])))) * M[1]
    
    #15. Unit conversion from "uM" to "mM" (_uM_mM)#
    else if (fun == "Hill_three_uM_mM")
      ec <- ((p[3] / (((p[1] / effv - 1)^(1 / p[2]))))) / 1000
    else if (fun == "Weibull_uM_mM")
      ec <- (10^((log(-log(1 - effv)) - p[1])/p[2])) / 1000
    #ec <- ((exp(-(-log(log(-1 / (-1 + effv))) + p[1]) * log(10) / p[2]))) / 1000
    else if (fun == "Logit_uM_mM")
      ec <- (10^((log(effv/(1-effv))-p[1])/p[2])) / 1000
    #ec <- ((exp(-log(10) * (p[1] + log(-(-1 + effv) / (effv))) / p[2]))) / 1000
    else if (fun == "BCW_uM_mM")
      ec <- ((p[3]/p[2]*(log(-log(1-effv))-p[1])+1)^(1/p[3])) / 1000
    #ec <- ((exp(log(-(p[1] * p[3] - p[2] - log(-log(1 - effv)) * p[3]) / p[2]) / p[3]))) / 1000
    else if (fun == "BCL_uM_mM")
      ec <- ((exp(log(-(p[1] * p[3] - p[2] + log(-(-1 + effv) / effv) * p[3]) / p[2]) / p[3]))) / 1000
    else if (fun == "GL_uM_mM")
      ec <- (10^(-(log((1/effv)^(1/p[3])-1)+p[1])/p[2])) / 1000
    #ec <- ((exp(-log(10) * (p[1] + log(exp(-log(effv) / p[3]) - 1)) / p[2]))) / 1000
    else if (fun == "Probit_uM_mM")
      ec <- ((10^((qnorm(effv, mean=0, sd=1) - p[1]) / p[2]))) / 1000
    else if (fun == "BCP_uM_mM")
      ec <- (((p[3] / p[2] * (qnorm(effv, mean=0, sd=1) - p[1]) + 1)^(1 / p[3]))) / 1000
    else if (fun == "Sigmoid_uM_mM")
      ec <- ((p[3] - p[2] * log((p[1] - effv) / effv))) / 1000
    else if (fun == "Logistic_uM_mM")
      ec <- ((p[3] *((p[1] - effv) / effv)^(1 / p[2]))) / 1000
    else if (fun == "Chapman_uM_mM")
      ec <- ((-(log(1 - (effv / p[1])^(1 / p[3])) / p[2]))) / 1000
    else if (fun == "Gompertz_uM_mM")
      ec <- ((p[3] - p[2] * log(-log(effv / p[1])))) / 1000
    
    #16. Unit conversion from "uM" to "nM" (_uM_nM)#
    else if (fun == "Hill_three_uM_nM")
      ec <- ((p[3] / (((p[1] / effv - 1)^(1 / p[2]))))) * 1000
    else if (fun == "Weibull_uM_nM")
      ec <- (10^((log(-log(1 - effv)) - p[1])/p[2])) * 1000
    #ec <- ((exp(-(-log(log(-1 / (-1 + effv))) + p[1]) * log(10) / p[2]))) * 1000
    else if (fun == "Logit_uM_nM")
      ec <- (10^((log(effv/(1-effv))-p[1])/p[2])) * 1000
    #ec <- ((exp(-log(10) * (p[1] + log(-(-1 + effv) / (effv))) / p[2]))) * 1000
    else if (fun == "BCW_uM_nM")
      ec <- ((p[3]/p[2]*(log(-log(1-effv))-p[1])+1)^(1/p[3])) * 1000
    #ec <- ((exp(log(-(p[1] * p[3] - p[2] - log(-log(1 - effv)) * p[3]) / p[2]) / p[3]))) * 1000
    else if (fun == "BCL_uM_nM")
      ec <- ((exp(log(-(p[1] * p[3] - p[2] + log(-(-1 + effv) / effv) * p[3]) / p[2]) / p[3]))) * 1000
    else if (fun == "GL_uM_nM")
      ec <- (10^(-(log((1/effv)^(1/p[3])-1)+p[1])/p[2])) * 1000
    #ec <- ((exp(-log(10) * (p[1] + log(exp(-log(effv) / p[3]) - 1)) / p[2]))) * 1000
    else if (fun == "Probit_uM_nM")
      ec <- ((10^((qnorm(effv, mean=0, sd=1) - p[1]) / p[2]))) * 1000
    else if (fun == "BCP_uM_nM")
      ec <- (((p[3] / p[2] * (qnorm(effv, mean=0, sd=1) - p[1]) + 1)^(1 / p[3]))) * 1000
    else if (fun == "Sigmoid_uM_nM")
      ec <- ((p[3] - p[2] * log((p[1] - effv) / effv))) * 1000
    else if (fun == "Logistic_uM_nM")
      ec <- ((p[3] *((p[1] - effv) / effv)^(1 / p[2]))) * 1000
    else if (fun == "Chapman_uM_nM")
      ec <- ((-(log(1 - (effv / p[1])^(1 / p[3])) / p[2]))) * 1000
    else if (fun == "Gompertz_uM_nM")
      ec <- ((p[3] - p[2] * log(-log(effv / p[1])))) * 1000
    
    #17. Unit conversion from "nM" to "mg/L" (_nM_mg/L)#
    else if (fun == "Hill_three_nM_mg/L")
      ec <- (((p[3] / (((p[1] / effv - 1)^(1 / p[2]))))) * M[1] ) / 1000000
    else if (fun == "Weibull_nM_mg/L")
      ec <- (10^((log(-log(1 - effv)) - p[1])/p[2])) / 1000000
    #ec <- (((exp(-(-log(log(-1 / (-1 + effv))) + p[1]) * log(10) / p[2]))) * M[1] ) / 1000000
    else if (fun == "Logit_nM_mg/L")
      ec <- (10^((log(effv/(1-effv))-p[1])/p[2])) / 1000000
    #ec <- (((exp(-log(10) * (p[1] + log(-(-1 + effv) / (effv))) / p[2]))) * M[1] ) / 1000000
    else if (fun == "BCW_nM_mg/L")
      ec <- ((p[3]/p[2]*(log(-log(1-effv))-p[1])+1)^(1/p[3])) / 1000000
    #ec <- (((exp(log(-(p[1] * p[3] - p[2] - log(-log(1 - effv)) * p[3]) / p[2]) / p[3]))) * M[1] ) / 1000000
    else if (fun == "BCL_nM_mg/L")
      ec <- (((exp(log(-(p[1] * p[3] - p[2] + log(-(-1 + effv) / effv) * p[3]) / p[2]) / p[3]))) * M[1] ) / 1000000
    else if (fun == "GL_nM_mg/L")
      ec <- (10^(-(log((1/effv)^(1/p[3])-1)+p[1])/p[2])) / 1000000
    #ec <- (((exp(-log(10) * (p[1] + log(exp(-log(effv) / p[3]) - 1)) / p[2]))) * M[1] ) / 1000000
    else if (fun == "Probit_nM_mg/L")
      ec <- (((10^((qnorm(effv, mean=0, sd=1) - p[1]) / p[2]))) * M[1] ) / 1000000
    else if (fun == "BCP_nM_mg/L")
      ec <- ((((p[3] / p[2] * (qnorm(effv, mean=0, sd=1) - p[1]) + 1)^(1 / p[3]))) * M[1] ) / 1000000
    else if (fun == "Sigmoid_nM_mg/L")
      ec <- (((p[3] - p[2] * log((p[1] - effv) / effv))) * M[1] ) / 1000000
    else if (fun == "Logistic_nM_mg/L")
      ec <- (((p[3] *((p[1] - effv) / effv)^(1 / p[2]))) * M[1] ) / 1000000
    else if (fun == "Chapman_nM_mg/L")
      ec <- (((-(log(1 - (effv / p[1])^(1 / p[3])) / p[2]))) * M[1] ) / 1000000
    else if (fun == "Gompertz_nM_mg/L")
      ec <- (((p[3] - p[2] * log(-log(effv / p[1])))) * M[1] ) / 1000000
    
    #18. Unit conversion from "nM" to "ug/L" (_nM_ug/L)#
    else if (fun == "Hill_three_nM_ug/L")
      ec <- (((p[3] / (((p[1] / effv - 1)^(1 / p[2]))))) * M[1] ) / 1000
    else if (fun == "Weibull_nM_ug/L")
      ec <- (10^((log(-log(1 - effv)) - p[1])/p[2])) / 1000
    #ec <- (((exp(-(-log(log(-1 / (-1 + effv))) + p[1]) * log(10) / p[2]))) * M[1] ) / 1000
    else if (fun == "Logit_nM_ug/L")
      ec <- (10^((log(effv/(1-effv))-p[1])/p[2])) / 1000
    #ec <- (((exp(-log(10) * (p[1] + log(-(-1 + effv) / (effv))) / p[2]))) * M[1] ) / 1000
    else if (fun == "BCW_nM_ug/L")
      ec <- ((p[3]/p[2]*(log(-log(1-effv))-p[1])+1)^(1/p[3])) / 1000
    #ec <- (((exp(log(-(p[1] * p[3] - p[2] - log(-log(1 - effv)) * p[3]) / p[2]) / p[3]))) * M[1] ) / 1000
    else if (fun == "BCL_nM_ug/L")
      ec <- (((exp(log(-(p[1] * p[3] - p[2] + log(-(-1 + effv) / effv) * p[3]) / p[2]) / p[3]))) * M[1] ) / 1000
    else if (fun == "GL_nM_ug/L")
      ec <- (10^(-(log((1/effv)^(1/p[3])-1)+p[1])/p[2])) / 1000
    #ec <- (((exp(-log(10) * (p[1] + log(exp(-log(effv) / p[3]) - 1)) / p[2]))) * M[1] ) / 1000
    else if (fun == "Probit_nM_ug/L")
      ec <- (((10^((qnorm(effv, mean=0, sd=1) - p[1]) / p[2]))) * M[1] ) / 1000
    else if (fun == "BCP_nM_ug/L")
      ec <- ((((p[3] / p[2] * (qnorm(effv, mean=0, sd=1) - p[1]) + 1)^(1 / p[3]))) * M[1] ) / 1000
    else if (fun == "Sigmoid_nM_ug/L")
      ec <- (((p[3] - p[2] * log((p[1] - effv) / effv))) * M[1] ) / 1000
    else if (fun == "Logistic_nM_ug/L")
      ec <- (((p[3] *((p[1] - effv) / effv)^(1 / p[2]))) * M[1] ) / 1000
    else if (fun == "Chapman_nM_ug/L")
      ec <- (((-(log(1 - (effv / p[1])^(1 / p[3])) / p[2]))) * M[1] ) / 1000
    else if (fun == "Gompertz_nM_ug/L")
      ec <- (((p[3] - p[2] * log(-log(effv / p[1])))) * M[1] ) / 1000
    
    #19. Unit conversion from "nM" to "mM" (_nM_mM)#
    else if (fun == "Hill_three_nM_mM")
      ec <- ((p[3] / (((p[1] / effv - 1)^(1 / p[2])))))/ 1000000
    else if (fun == "Weibull_nM_mM")
      ec <- (10^((log(-log(1 - effv)) - p[1])/p[2])) / 1000000
    #ec <- ((exp(-(-log(log(-1 / (-1 + effv))) + p[1]) * log(10) / p[2])))/ 1000000
    else if (fun == "Logit_nM_mM")
      ec <- (10^((log(effv/(1-effv))-p[1])/p[2])) / 1000000
    #ec <- ((exp(-log(10) * (p[1] + log(-(-1 + effv) / (effv))) / p[2])))/ 1000000
    else if (fun == "BCW_nM_mM")
      ec <- ((p[3]/p[2]*(log(-log(1-effv))-p[1])+1)^(1/p[3])) / 1000000
    #ec <- ((exp(log(-(p[1] * p[3] - p[2] - log(-log(1 - effv)) * p[3]) / p[2]) / p[3])))/ 1000000
    else if (fun == "BCL_nM_mM")
      ec <- ((exp(log(-(p[1] * p[3] - p[2] + log(-(-1 + effv) / effv) * p[3]) / p[2]) / p[3])))/ 1000000
    else if (fun == "GL_nM_mM")
      ec <- (10^(-(log((1/effv)^(1/p[3])-1)+p[1])/p[2])) / 1000000
    #ec <- ((exp(-log(10) * (p[1] + log(exp(-log(effv) / p[3]) - 1)) / p[2])))/ 1000000
    else if (fun == "Probit_nM_mM")
      ec <- ((10^((qnorm(effv, mean=0, sd=1) - p[1]) / p[2])))/ 1000000
    else if (fun == "BCP_nM_mM")
      ec <- (((p[3] / p[2] * (qnorm(effv, mean=0, sd=1) - p[1]) + 1)^(1 / p[3])))/ 1000000
    else if (fun == "Sigmoid_nM_mM")
      ec <- ((p[3] - p[2] * log((p[1] - effv) / effv)))/ 1000000
    else if (fun == "Logistic_nM_mM")
      ec <- ((p[3] *((p[1] - effv) / effv)^(1 / p[2])))/ 1000000
    else if (fun == "Chapman_nM_mM")
      ec <- ((-(log(1 - (effv / p[1])^(1 / p[3])) / p[2])))/ 1000000
    else if (fun == "Gompertz_nM_mM")
      ec <- ((p[3] - p[2] * log(-log(effv / p[1]))))/ 1000000
    
    #20. Unit conversion from "nM" to "uM" (_nM_uM)#
    else if (fun == "Hill_three_nM_uM")
      ec <- ((p[3] / (((p[1] / effv - 1)^(1 / p[2]))))) / 1000
    else if (fun == "Weibull_nM_uM")
      ec <- (10^((log(-log(1 - effv)) - p[1])/p[2])) / 1000
    #ec <- ((exp(-(-log(log(-1 / (-1 + effv))) + p[1]) * log(10) / p[2]))) / 1000
    else if (fun == "Logit_nM_uM")
      ec <- (10^((log(effv/(1-effv))-p[1])/p[2])) / 1000
    #ec <- ((exp(-log(10) * (p[1] + log(-(-1 + effv) / (effv))) / p[2]))) / 1000
    else if (fun == "BCW_nM_uM")
      ec <- ((p[3]/p[2]*(log(-log(1-effv))-p[1])+1)^(1/p[3])) / 1000
    #ec <- ((exp(log(-(p[1] * p[3] - p[2] - log(-log(1 - effv)) * p[3]) / p[2]) / p[3]))) / 1000
    else if (fun == "BCL_nM_uM")
      ec <- ((exp(log(-(p[1] * p[3] - p[2] + log(-(-1 + effv) / effv) * p[3]) / p[2]) / p[3]))) / 1000
    else if (fun == "GL_nM_uM")
      ec <- (10^(-(log((1/effv)^(1/p[3])-1)+p[1])/p[2])) / 1000
    #ec <- ((exp(-log(10) * (p[1] + log(exp(-log(effv) / p[3]) - 1)) / p[2]))) / 1000
    else if (fun == "Probit_nM_uM")
      ec <- ((10^((qnorm(effv, mean=0, sd=1) - p[1]) / p[2]))) / 1000
    else if (fun == "BCP_nM_uM")
      ec <- (((p[3] / p[2] * (qnorm(effv, mean=0, sd=1) - p[1]) + 1)^(1 / p[3]))) / 1000
    else if (fun == "Sigmoid_nM_uM")
      ec <- ((p[3] - p[2] * log((p[1] - effv) / effv))) / 1000
    else if (fun == "Logistic_nM_uM")
      ec <- ((p[3] *((p[1] - effv) / effv)^(1 / p[2]))) / 1000
    else if (fun == "Chapman_nM_uM")
      ec <- ((-(log(1 - (effv / p[1])^(1 / p[3])) / p[2]))) / 1000
    else if (fun == "Gompertz_nM_uM")
      ec <- ((p[3] - p[2] * log(-log(effv / p[1])))) / 1000
    
    ecx[i, ] <- ec
    
  }
  
  ## Chemical의 EC 전 구간의 데이터가 NaN 또는 Inf 값이 나오는 경우 chemical을 mixture에서 제외하는 코드 - mwseo
  ## 필요 시 사용
  
  # remove <- 0
  # 
  # for (ai in seq(nrow(ecx))) {
  #   temp <- ecx[ai,]
  #   
  #   if ((is.infinite(temp[1]) & is.infinite(temp[length(temp)])) | (is.na(temp[1] & is.na(temp[length(temp)])))) {
  #     remove <- c(remove, ai)
  # 
  #   }
  # }
  # 
  # remove <- remove[2:length(remove)]
  # 
  # ecx <- ecx[-c(remove), ]
  # param <- param[-c(remove), ]
  # model <- model[-c(remove)]
  # 
  
  #print(ecx)
  #print(param)
  #print(model)
  effects <- c(0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90)
  colName <- effects*100
  colnames(ecx) <- colName
  #if (is.null(rownames(param)))
  #  rownames(ecx) <- model 
  #else rownames(ecx) <- rownames(param)
  
  print(ecx)
  rownames(ecx) <- model
  return(ecx)
  
  ## NaN, Inf 출력 제외 조건 추가 - mwseo
  
  #final_data <- ecx[,!(colSums(is.na(ecx)| is.nan(ecx) | ecx < 0 | is.infinite(ecx) ))]
  #print(final_data)
  
  # 단일물질 graph 도출을 위한 부분
  #graph_data <- t(final_data)
  #rowName <- paste0(effv*100)
  #rownames(graph_data) <- rowName
  #print(graph_data)
  
  #나중에 변경 필요함
  #write.csv(graph_data, file=resultCsvName_ECx)
  #write.csv(graph_data, file="C:/Users/hkjin/Desktop/MRA_v2/Test_ECx.csv")
  
  #return(ecx)
  #return(final_data)
  #return(ecx[,!(colSums(is.na(ecx)| is.nan(ecx) | ecx < 0 | is.infinite(ecx) ))])  
}