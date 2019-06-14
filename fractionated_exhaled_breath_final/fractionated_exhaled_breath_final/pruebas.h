#ifndef PRUEBAS_H
#define PRUEBAS_H
#include "defines.h"
unsigned long tiempo_t = 0;


char Key = '0';
int mensaje=0;


void prueba_globos_alternando(unsigned long tiempo){
   if(tiempo - tiempo_t> 7000){
    digitalWrite(valv_negra_1,LOW);
    //digitalWrite(valv_blanca_1,HIGH);
    digitalWrite(valv_negra_2,LOW);
    //digitalWrite(valv_blanca_2,LOW);
    tiempo_t = tiempo;
  }
 else if (tiempo - tiempo_t > 5000){
   // digitalWrite(valv_negra_1,LOW);
    //digitalWrite(valv_blanca_1,HIGH);
   // digitalWrite(valv_negra_2,HIGH);
    //digitalWrite(valv_blanca_2,HIGH);
  }
  else if (tiempo - tiempo_t > 3000){
    //digitalWrite(valv_negra_1, LOW);
    //digitalWrite(valv_blanca_1,LOW);
    //digitalWrite(valv_negra_2,HIGH);
    //digitalWrite(valv_blanca_2,HIGH);
  }
  else if (tiempo - tiempo_t > 1000){
    digitalWrite(valv_negra_1, HIGH);
    //digitalWrite(valv_blanca_1,HIGH);
    digitalWrite(valv_negra_2,LOW);
    //digitalWrite(valv_blanca_2,HIGH);
  }
}

//CODIGO PRUEBAS POR SERIAL 

 /*
 if(Serial.available()>0){
    Key=Serial.read();
    Serial.print (Key);
     
    }
    
    
  
  if (Key=='1'){
  
    digitalWrite(valv_negra_1,LOW);
    digitalWrite(valv_negra_2,HIGH);
    digitalWrite(valv_blanca_1,LOW);
    digitalWrite(valv_blanca_2,HIGH);
  }
  else if (Key=='0'){
    digitalWrite(valv_negra_1,HIGH);
    digitalWrite(valv_negra_2,LOW);
    digitalWrite(valv_blanca_1,HIGH);
    digitalWrite(valv_blanca_2,LOW);
  }
  else if (Key == '2'){
    digitalWrite(valv_blanca_2,HIGH);
  }

  */















#endif // PRUEBAS_H
