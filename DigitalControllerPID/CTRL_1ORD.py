# 
# Author: sudiro [sudiro@mail.ugm.ac.id]
# this file can be downloaded from github.com/sudiroeen
# 

import numpy as np
import matplotlib.pyplot as plt 

def vietaformula(poles):
	if len(poles) == 1:
		return np.array([[1,-poles[0]]]).T 
	else:
		seedvec = vietaformula([poles[0]])
		for i in range(1,len(poles)):
			Idt = np.eye(i+1)
			Ozr = np.zeros((1,i+1))
			matm = np.vstack([Idt, Ozr]) + np.vstack([Ozr, -poles[i]*Idt])
			seedvec = matm @ seedvec
		return np.real(seedvec)

Ts = 1e-3
paramd = (1.01, -0.01)

poles = [0.95+1j*0., 0.9-1j*0., 0.9]
# poles = [0.1+1j*0.9, 0.1-1j*0.9, 0.9]
_, q2, q1, q0 = vietaformula(poles)
apar, bpar = paramd
# print((q2[0],q1[0], q0[0]))
bt0des = (q2[0] + apar + 1)/bpar
bt1des = (q1[0] - apar)/bpar
bt2des = q0[0]/bpar

def thesystem(ynm1, cnm1):
	a1, b1 = paramd
	ynm0 = a1*ynm1 + b1*cnm1
	return  ynm0

def thecontroller(enm0, enm1, enm2, cnm1):
	cnm0 = cnm1 + bt0des*enm0 + bt1des*enm1 + bt2des*enm2
	return cnm0

def square_sig(ctr, pct):
	# return np.sin(2*np.pi*t) #, counter
	if(ctr<pct): 
		ctr += 1
		return 1,ctr 
	elif ctr < 1000:
		ctr+=1
		return -2, ctr 
	else:
		ctr = 0 
		return -2, ctr 


def controller_OPENLOOP(ref):
	return 1*ref 

ynlist = list()
rnlist = list()
cnlist = list()
enlist = list()
Ts = 1e-3
tm = np.arange(0, 2, step=Ts)
counter = 0 
cnm0, cnm1, cnm2 = [0,0,0]
enm0, enm1, enm2 = [0,0,0]
ynm0, ynm1 = [0,0]
rnm0, rnm1 = [0,0]

for t in tm:
	if len(ynlist) < 3:
		ynlist.append(0)
		rnlist.append(0)
		cnlist.append(0)
		enlist.append(0)
	else:
		ynm1 = np.copy(ynm0)
		rnm0, counter = square_sig(counter, 500)
		enm2 = np.copy(enm1)
		enm1 = np.copy(enm0)

		cnm2 = np.copy(cnm1)
		cnm1 = np.copy(cnm0)

		ynm0 = thesystem(ynm1, cnm1)

		enm0 = rnm0 - ynm0
		# cnm0 = controller_OPENLOOP(rnm0)
		cnm0 = thecontroller(enm0, enm1, enm2, cnm1)
		rnlist.append(rnm0)
		ynlist.append(ynm0)
		cnlist.append(cnm0)
		enlist.append(enm0)

fig, ax = plt.subplots(2)
ax[0].plot(tm, rnlist, '-k', tm, ynlist, '-r')
ax[1].plot(tm, cnlist, '-k')
plt.show()
