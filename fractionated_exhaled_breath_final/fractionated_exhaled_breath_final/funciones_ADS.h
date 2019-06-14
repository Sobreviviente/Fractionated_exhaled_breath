#ifndef funciones_ADS_H
#define funciones_ADS_H
#include "defines.h"
#include "estados_salida.h" 

float sensor_p=0;  // valor de sensor presion
float sensor_co2_1=0;  //valor de sensor co2 primer cable 
float sensor_co2_2=0;  //valor de sensor co2 segundo cable

void lectura_sensor(){
  float cValue = (5.0*analogRead(Presion))/1023.0;
  sensor_p = 0.95*sensor_p + 0.05*cValue;
}

void controla_bombas(){ 
    lectura_sensor();
    if (sensor_p >= umbral_high){
      digitalWrite(Bomba1, LOW);
      digitalWrite(Bomba2, LOW);
    }
    else{
      if(sensor_p<umbral_low) {
        digitalWrite(Bomba1,HIGH);
        digitalWrite(Bomba2,HIGH);
      
      }
    }
}

float lectura_escaner(){
  sensor_co2_1 = (5.0*analogRead(23))/1023.0;
  sensor_co2_2 = (5.0*analogRead(22))/1023.0;
  return sensor_co2_1;
}



#endif // funciones_ADS_H
