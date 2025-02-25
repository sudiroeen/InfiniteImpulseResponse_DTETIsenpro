# 
# Author: sudiro [sudiro@mail.ugm.ac.id]
# this file can be downloaded from github.com/sudiroeen
# 

import numpy as np
import matplotlib.pyplot as plt 

param = (1.01, 0.8)

def system_DUNSTABLE_1ord(vec_yn, vec_xn):
	# vec_yn = [y[n], y[n-1], y[n-2]]
	# vec_xn = [x[n], x[n-1], x[n-2]]
	wc = 2*np.pi*10
	Ts = 1e-3
	a1 = param[0]
	b1 = param[1]
	for i in range(1,len(vec_yn)):
		vec_yn[i] = vec_yn[i-1]
	vec_yn[0] = a1*vec_yn[1] + b1*vec_xn[1]
	return  vec_yn[0]

def controller_DUNSTABLE_1ord(vec_en, vec_cn, param):
	# vec_en = [e[n], e[n-1], e[n-2]]
	# vec_cn = [c[n], c[n-1], c[n-2]]
	# param = [a,b]
	apar, bpar = param
	for i in range(1,len(vec_cn)):
		vec_cn[i] = vec_cn[i-1]
		vec_en[i] = vec_en[i-1]
	Ts = 1e-3
	Kp = (apar + 0.1)/bpar
	Td = -0.1/(apar + 0.1)
	Ti = (apar + 0.1)/(0.59 + 2*Td*(apar + 0.1)) * Ts
	vec_cn[0] = vec_cn[1] + Kp*(1+Td)*vec_en[0] + Kp*(Ts/Ti - 1 - 2*Td)*vec_en[1] + Kp*Td*vec_en[2]
	return vec_cn[0]

def ref_sig(t):
	return 1 * np.sin(2*np.pi*t*1) + 0.2*np.sin(2*np.pi*t*100)

def controller_OPENLOOP(ref):
	return 1*ref 

yout = list()
err = list()
cinp = list()
Ts = 1e-3
tm = np.arange(0, 5, step=Ts)

for t in tm:
	if len(yout) < 3:
		yout.append(0)
		err.append(0)
		cinp.append(0)
		continue
	else:
		yout_ = system_DUNSTABLE_1ord(yout[-3:], cinp[-3:])
		ref_ = ref_sig(t)
		err_ = ref_ - yout_
		cinp_ = controller_DUNSTABLE_1ord(yout[-3:], cinp[-3:], param)
		err.append(err_)
		yout.append(yout_)
		cinp.append(ref_)

fig, ax = plt.subplots(2)
ax[0].plot(tm, cinp, '-k', tm, yout, '-r')
ax[1].plot(tm, cinp, '-k', tm, yout, '-r')
plt.show()