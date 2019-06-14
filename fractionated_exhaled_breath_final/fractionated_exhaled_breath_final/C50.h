#ifndef C50_H
#define C50_H
#include "estados_salida.h"
#include "defines.h" 
#include "funciones_ADS.h"

int estado_aux=1; 
float ultimos_3valores[3]={};
int pos=0;
float C50_maximo=-8;
float C50_minimo=8;
float C50_prom3=3.0;
bool C50_revisando = false;

void C50_init() {
 estado_aux = 1;  
 C50_revisando = false;
}

void actualizar_promedio() {
  float prom = 0.0;
  for (int i=0; i<3; i++) {
    if (ultimos_3valores[i] == 0)
      break;
    prom += ultimos_3valores[i]/3;
  }
  
  C50_prom3 =  prom;
}

void C50() {
  if (sensor_co2_1 > 1 && !C50_revisando){
    C50_revisando = true;
    C50_maximo = -8;
    C50_minimo = 8;
  }
  else if (sensor_co2_1 <= 0.05 && C50_revisando){
          int promedio;
          promedio = (C50_maximo+C50_minimo)/2.0;
          ultimos_3valores[pos%3]=promedio;
          actualizar_promedio();
          pos+=1;   
          C50_revisando=false;
  }

  if (C50_revisando){
    if (sensor_co2_1>C50_maximo){
      C50_maximo=sensor_co2_1;
    }
    if (sensor_co2_1<C50_minimo){
      C50_minimo=sensor_co2_1;
  }  
  }
  
  if ((sensor_co2_1<C50_prom3) && estado_aux==0){
    estado_deadspace();
    estado_aux=1;
    
  }
  else if((sensor_co2_1>C50_prom3) && estado_aux==1){
    estado_biomarcador();
    estado_aux=0;
  }
}








#endif // C50_H
