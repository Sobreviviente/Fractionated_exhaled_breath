#ifndef PC_H
#define PC_H

#include "estados_salida.h"
#include "defines.h"
#include "funciones_ADS.h"

unsigned long tiempo_trigger = 0;
int estado_curva = 0;
float alpha=0.99;
float value = 0 ;
float value_prev = 0;
unsigned long tiempo_prev=0;
float value_2=0;
float dd=0;

void PC_init() {
  estado_curva = 0;
}

void actualizar(unsigned long t) {
  tiempo_prev = t;
  value_prev = value;
}

void PC(float sensor, unsigned long t) {
  Serial.print(sensor);
  Serial.print(' ');
  Serial.print(estado_curva);
  Serial.print(' ');
  Serial.print(t);
  Serial.print(' ');
  Serial.print(tiempo_trigger);
  value = alpha * value + (1-alpha) * sensor;
  dd = (value - value_prev)/((t-tiempo_prev)/1000000.0);
  value_2=alpha*value_2+(1-alpha)*dd;
  actualizar(t);
  Serial.print(' ');
  Serial.println(value_2);
  
  if (estado_curva==0 && value_2 < 3.0){
    estado_curva=1;
    estado_deadspace();
  }
  
  
  else if (estado_curva==1 && value_2 > 3.0){    // CURVA SUBIENDO
    estado_curva=2;
    estado_deadspace();
  }
  else if (estado_curva==2 && value_2 < 0.5){  // 
    estado_curva=3;
    tiempo_trigger = t + SUMA_TIEMPO; 
    estado_deadspace();
  }
  else if (estado_curva==3 && t>tiempo_trigger){            // TRIGGER 
    estado_curva=4;
    estado_biomarcador();
  }
  else if(estado_curva==4 && sensor<0.05){
    estado_curva=0;
    estado_deadspace();
  }
}

#endif // PC_H
