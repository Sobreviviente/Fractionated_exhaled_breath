#ifndef ESTADOS_SALIDA_H
#define ESTADOS_SALIDA_H
#include "defines.h"

void estado_deadspace(){
  digitalWrite(valv_negra_1,HIGH);
  digitalWrite(valv_negra_2,LOW);
  digitalWrite(valv_blanca_1,HIGH);
  digitalWrite(valv_blanca_2,LOW);
}

void estado_biomarcador(){
  digitalWrite(valv_negra_1,LOW);
  digitalWrite(valv_negra_2,HIGH);
  digitalWrite(valv_blanca_1,LOW);
  digitalWrite(valv_blanca_2,HIGH);
}

#endif // ESTADOS_SALIDA_H
