demanda = [3.3,0.019,0.001,0.074,1.31,3.4]
demandaType = [Ld,Li,Ld,Li,Ld,Li]
k = demanda.size
kr = 0
residenceTime = []
NiMinus1R = 0
resTime = 0
Lk(fila com comprimentos)
for i=1 to k:
	if(demanda[i]>0):
		kr+=1
nr = 15(num de clientes)
for i=1 to k:
	if(demanda[i]>0):
		Lk.put(nr/kr)
	else:
		Lk.put(0)
tolerance = 0.0005, maxIter = 100
while(error>tolerance and numIter>maxIter): #até convergir
	for i=1 to k
		NiMinus1R = Lk[i]*(nr-1)/nr
		if(demandaType[i]=="Li"):
			residenceTime.append(demanda[i]*(1+NiMinus1R))
		else:
			residenceTime.append(demanda[i])
		resTime += residenceTime[i]
