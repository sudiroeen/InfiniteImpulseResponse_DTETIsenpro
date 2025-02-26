# 
# Author: sudiro [sudiro@mail.ugm.ac.id]
# this file can be downloaded from github.com/sudiroeen
# 

import numpy as np
import matplotlib.pyplot as plt 

def TransfFunction(w):
	w2 = 10 * 2*np.pi 
	w1 = 20 * 2*np.pi 
	w4 = 640 * 2*np.pi 
	w3 = 1280 * 2*np.pi 
	K = w2*w3/(w1*w4)
	Hjw = (1j*w + w2)*(1j*w + w3)/((1j*w + w1) * (1j*w + w4))
	mag = np.abs(Hjw)
	phs = np.angle(Hjw)
	return mag, phs 


wm = np.arange(0,int(81920),step=1)
mp = list()
for w in wm:
	mag, phs = TransfFunction(w)
	mp.append([mag, phs])

mp = np.array(mp).T
# fig, ax = plt.subplots(2)
plt.figure("Magnitude")
plt.semilogx(wm, mp[0])
plt.grid()
plt.figure("Phase")
plt.semilogx(wm, mp[1])
plt.grid()
plt.show()
