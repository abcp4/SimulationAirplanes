
# coding: utf-8

# In[10]:

from __future__ import division
import math
def simu(demanda,demandaType,nr):
    kr = 0
    maxIter = 100
    numIter = 0
    tolerance = 0.0005
    error = tolerance+1
    residenceTime = [0,0,0,0,0,0]
    NiMinus1R = 0
    resTime = 0
    throughput = 0
    Lk = []#fila com comprimentos
    previousLK = 0
    for d in demanda:
        if(d>0):
            kr+=1
    print "Kr " + str(kr)
    for d in demanda:
        if(d>0):
            Lk.append(nr/kr)
        else:
            Lk.append(0)
    print "LK "+str(Lk)
    while(error>tolerance and numIter <= maxIter): #até convergir
        if(numIter ==0):
            error = 0
        resTime = 0
        for i in range(len(demanda)):
            NiMinus1R = Lk[i]*(nr-1)/nr
            if(demandaType[i]=='Li'):
                residenceTime[i]= demanda[i]*(1+NiMinus1R)
            else:
                residenceTime[i] = demanda[i]
            resTime += residenceTime[i]
        throughput = nr/resTime
        
        numIter = numIter + 1
        error = 0
        for i in range(len(Lk)):
            if(demanda[i]>0):
                previousLK = Lk[i]
                Lk[i] = throughput*residenceTime[i]#verificar se rT tem o msm tamanho da demanda
                Diff = abs((previousLK - Lk[i])/Lk[i])
                if(Diff>error):
                    error = Diff
    utilizations = []
    for i in range(len(demanda)):#calcula utilizações
        utilizations.append(throughput*demanda[i])
    result = [error,throughput,residenceTime,utilizations]
    return result
    
demanda = [3.3,0.019,0.001,0.074,1.31,3.4]
demandaType = ['Ld','Li','Ld','Li','Ld','Li']
nr = 15# num de clientes
result = simu(demanda,demandaType,nr)
print result

