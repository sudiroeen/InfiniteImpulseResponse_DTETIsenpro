import numpy as np
import matplotlib.pyplot as plt 

def TransfFunction(w):
	w1 = 10 * 2*np.pi 
	w2 = 20 * 2*np.pi 
	w3 = 640 * 2*np.pi 
	w4 = 1280 * 2*np.pi 
	K = w1*w4/(w2*w3)
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
