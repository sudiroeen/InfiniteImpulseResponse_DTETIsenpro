# 
# Author: sudiro [sudiro@mail.ugm.ac.id]
# this file can be downloaded from github.com/sudiroeen
# 
import numpy as np
import matplotlib.pyplot as plt 

def TransfFunction(w):
	wc = 10 * 2*np.pi 
	Hjw = wc/(1j*w + wc)
	mag = np.abs(Hjw)
	phs = np.angle(Hjw)
	return mag, phs 


wm = np.arange(0,int(1e5),step=1)
mp = list()
for w in wm:
	mag, phs = TransfFunction(w)
	mp.append([mag, phs])

mp = np.array(mp).T
# fig, ax = plt.subplots(2)
plt.figure("Magnitude")
plt.semilogx(wm, mp[0])
plt.grid()
# plt.figure("Phase")
# plt.semilogx(wm, mp[1])
# plt.grid()
plt.show()
