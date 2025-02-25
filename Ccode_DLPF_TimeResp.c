#include "stdio.h"
#include "math.h"

#define nBuf 2 

char msg[30];
uint16_t adc_read;
int cek = 0;
uint16_t adcBuf[nBuf];


float system_DLPF(){
	// ambilkan dari file CcodeOfAllFilters.c
}

void HAL_ADC_ConvCpltCallback(ADC_HandleTyped* hadc){

}

void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc){
	// scaling nilai ADC dengan mengalikan 3.3/4095 dengan mengubah ke tipe data float
	cek = 1;
}

void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef* htim){
	if(htim->Instance == TIM3){
		if(cek){
			// panggil system_DLPF() atau filter lain
			sprintf(msg, "%f, %f\r\n", adcBuf[0], adcBuf[1]);
			HAL_UART_Transmit_IT(&huart2, (uint8_t*)msg, strlen(msg));
			HAL_ADC_Start(&hadc1);
		}
	}
}

// tidak perlu penambahan code di while(1){ }