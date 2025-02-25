# 
# Author: sudiro [sudiro@mail.ugm.ac.id]
# this file can be downloaded from github.com/sudiroeen
# 

import numpy as np
import matplotlib.pyplot as plt 

def system_DBSF(vec_yn, vec_xn):
	# vec_yn = [y[n], y[n-1], y[n-2]]
	# vec_xn = [x[n], x[n-1], x[n-2]]
	w1 = 10 * 2*np.pi 
	w2 = 40 * 2*np.pi 
	w3 = 80 * 2*np.pi 
	w4 = 160 * 2*np.pi 
	Ts = 1e-3
	exp_w1ts = np.exp(-w1*Ts)
	exp_w2ts = np.exp(-w2*Ts)
	exp_w3ts = np.exp(-w3*Ts)
	exp_w4ts = np.exp(-w4*Ts)

	eta1 = w2 + w3 - w1 - w4 
	eta2 = w2*w3 - w1*w4 

	A = 1 + eta2/(w1*w4)
	B = (w1*eta1 - eta2)/(w1*(w4 - w1))
	C = (-w4*eta1 + eta2)/(w4*(w4-1))

	gm0 = A + B + C 
	gm1 = -B*(1 + exp_w4ts) -A*(exp_w4ts + exp_w1ts) -C*(1+exp_w1ts)
	gm2 = exp_w1ts + (B + A*exp_w1ts)*exp_w4ts
	ap1 = -(exp_w1ts + exp_w4ts)
	ap2 = np.exp(-(w1 + w4)*Ts)

	gm_ = [gm0, gm1, gm2]
	ap_ = [0, ap1, ap2]

	for i in range(1,len(vec_yn)):
		vec_yn[i] = vec_yn[i-1]
	vec_yn[0] = 0
	for i in range(len(vec_yn)):
		vec_yn[0] += -ap_[i]*vec_yn[i] + gm_[i]*vec_xn[i]
	return vec_yn[0]


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
		yout_ = system_DBSF(yout[-3:], cinp[-3:])
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