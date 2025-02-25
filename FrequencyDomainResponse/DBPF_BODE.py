import numpy as np 
import matplotlib.pyplot as plt 


def performing_fft(signal):
    N = len(signal)
    if N <= 1:
        return signal
    even = performing_fft(signal[0::2])
    odd = performing_fft(signal[1::2])
    terms = [np.exp(-2j * np.pi * k / N) * odd[k] for k in range(N // 2)]
    return [even[k] + terms[k] for k in range(N // 2)] + [even[k] - terms[k] for k in range(N // 2)]

signal = [2.14, 0.38, -1.67, -0.85]
res_fft = performing_fft(signal)

# print("res_fft:\n", res_fft)

def system_DBPF(vec_yn, vec_xn):
    # vec_yn = [y[n], y[n-1], y[n-2]]
    # vec_xn = [x[n], x[n-1], x[n-2]]
    wch = 10 * 2* np.pi 
    wcl = 100 * 2* np.pi 
    Ts = 1e-3
    exp_wlts = np.exp(-wcl*Ts)
    exp_whts = np.exp(-wch*Ts)
    a1 = exp_wlts + exp_whts
    a2 = np.exp(-(wcl+wch)*Ts)
    bval = wcl/(wcl-wch) * (exp_whts - exp_wlts)
    for i in range(1,len(vec_yn)):
        vec_yn[i] = vec_yn[i-1]
    vec_yn[0] = a1*vec_yn[1] + a2*vec_yn[2] + bval*(vec_xn[1] - vec_xn[2])
    print("a1: ", a1, "\ta2: ", a2)
    return vec_yn[0]

def rect2polar(yfft):
    mag = np.abs(yfft)
    phs = np.angle(yfft)
    return mag, phs


def controller_OPENLOOP(ref):
    return 1*ref 

yout = list()
err = list()
cinp = list()
Ts = 1e-3
tm = np.arange(0, 0.256, step=Ts)

for t in tm:
    if len(yout) < 3:
        yout.append(0)
        err.append(0)
        cinp.append(0)
        continue
    else:
        yout_ = system_DBPF(yout[-3:], cinp[-3:])
        ref_ = 1 if len(yout) == 3 else 0 
        err_ = ref_ - yout_
        cinp_ = controller_OPENLOOP(ref_)
        err.append(err_)
        yout.append(yout_)
        cinp.append(ref_)

yfft = performing_fft(yout)

mag, phs = rect2polar(yfft)
N = len(mag)
wlist = [2*np.pi*k/N for k in range(N)]

fig, ax = plt.subplots(2)
ax[0].plot(wlist, mag, '-r')
ax[1].plot(wlist, phs, '-k')

fig, ax = plt.subplots(2)
ax[0].stem(tm, cinp, 'ko', basefmt='')
ax[1].stem(tm, yout, 'ro', basefmt='')
plt.show()