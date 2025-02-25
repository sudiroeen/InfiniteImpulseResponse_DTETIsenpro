/* 
 Author: sudiro [sudiro@mail.ugm.ac.id]
 this file can be downloaded from github.com/sudiroeen
*/

#include <stdio.h>
#include <math.h>

// vec_yn = [y[n], y[n-1], y[n-2]]
// vec_xn = [x[n], x[n-1], x[n-2]]

float system_DLPF(float* vec_yn, float* vec_xn){
	float wc = 2 * M_PI * 10;
	float Ts = 1e-3;
	float a1 = (float) pow(M_E,-wc*Ts);
	float b1 = 1 - a1;
	int nsize = sizeof(vec_yn)/sizeof(vec_yn[0]);

	for(int i=1; i<nsize; i++){
		vec_yn[i] = vec_yn[i-1];
	}
	vec_yn[0] = a1*vec_yn[1] + b1*vec_xn[1];
	return vec_yn[0]
}

float system_DHPF(float* vec_yn, float* vec_xn){
	float wc = 2 * M_PI * 50;
	float Ts = 1e-3;
	float a1 = (float) pow(M_E,-wc*Ts);
	int nsize = sizeof(vec_yn)/sizeof(vec_yn[0]);

	for(int i=1; i<nsize; i++){
		vec_yn[i] = vec_yn[i-1];
	}
	vec_yn[0] = a1*vec_yn[0] - vec_xn[1] + vec_xn[0];
	return vec_yn[0]
}

float system_DBPF(float* vec_yn, float* vec_xn){
	float wch = 10 * 2 * M_PI;
	float wcl = 100 * 2 * M_PI;
	float Ts = 1e-3;
	float exp_wlts = pow(M_PI, -wcl*Ts);
	float exp_whts = pow(M_PI, -wch*Ts);
	float bval = wcl/(wcl - wch) * (exp_whts - exp_wlts);
	int nsize = sizeof(vec_yn)/sizeof(vec_yn[0]);
	for(int i=1; i<nsize; i++){
		vec_yn[i] = vec_yn[i-1];
	}
	vec_yn[0] = a1*vec_yn[1] + b1*vec_yn[2] + bval*(vec_xn[1] - vec_xn[2]);
	return vec_yn[0];
}

float system_DBSF(float* vec_yn, float* vec_xn){
	float w1 = 10 * 2*M_PI;
	float w2 = 40 * 2*M_PI; 
	float w3 = 80 * 2*M_PI; 
	float w4 = 160 * 2*M_PI; 
	float Ts = 1e-3;
	float exp_w1ts = pow(M_E, -w1*Ts);
	float exp_w2ts = pow(M_E, -w2*Ts);
	float exp_w3ts = pow(M_E, -w3*Ts);
	float exp_w4ts = pow(M_E, -w4*Ts);

	float eta1 = w2 + w3 - w1 - w4;
	float eta2 = w2*w3 - w1*w4;

	float A = 1 + eta2/(w1*w4);
	float B = (w1*eta1 - eta2)/(w1*(w4 - w1));
	float C = (-w4*eta1 + eta2)/(w4*(w4-1));

	float gm0 = A + B + C;
	float gm1 = -B*(1 + exp_w4ts) -A*(exp_w4ts + exp_w1ts) -C*(1+exp_w1ts);
	float gm2 = exp_w1ts + (B + A*exp_w1ts)*exp_w4ts;
	float ap1 = -(exp_w1ts + exp_w4ts);
	float ap2 = np.exp(-(w1 + w4)*Ts);

	float gm_ = [gm0, gm1, gm2];
	float ap_ = [0, ap1, ap2];

	int nsize = sizeof(vec_yn)/sizeof(vec_yn[0]);

	for(int i=1; i<nsize; i++){
		vec_yn[i] = vec_yn[i-1];
	}
	float vec_yn[0] = 0;
	for(int i=0; i<nsize; i++){
		vec_yn[0] += -ap_[i]*vec_yn[i] + gm_[i]*vec_xn[i];
	}
	return vec_yn[0];
}
