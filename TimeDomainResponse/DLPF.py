# 
# Author: sudiro [sudiro@mail.ugm.ac.id]
# this file can be downloaded from github.com/sudiroeen
# 

import numpy as np
import matplotlib.pyplot as plt 

def system_DLPF(vec_yn, vec_xn):
	# vec_yn = [y[n], y[n-1], y[n-2]]
	# vec_xn = [x[n], x[n-1], x[n-2]]
	wc = 2*np.pi*10
	Ts = 1e-3
	a1 = np.exp(-wc*Ts)
	b1 = 1-a1
	for i in range(1,len(vec_yn)):
		vec_yn[i] = vec_yn[i-1]
	vec_yn[0] = a1*vec_yn[1] + b1*vec_xn[1]
	return  vec_yn[0]

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
		yout_ = system_DLPF(yout[-3:], cinp[-3:])
		ref_ = ref_sig(t)
		err_ = ref_ - yout_
		# cinp_ = controller_DUNSTABLE_1ord(yout[-3:], cinp[-3:])
		cinp_ = controller_OPENLOOP(ref_)
		err.append(err_)
		yout.append(yout_)
		cinp.append(ref_)

fig, ax = plt.subplots(2)
ax[0].plot(tm, cinp, '-k', tm, yout, '-r')
ax[1].plot(tm, cinp, '-k', tm, yout, '-r')
plt.show()