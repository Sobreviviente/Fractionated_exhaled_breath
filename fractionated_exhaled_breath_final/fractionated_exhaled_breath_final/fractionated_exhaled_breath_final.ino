#include "pc.h"
#include "estados_salida.h"
#include "defines.h"
#include "funciones_ADS.h"
#include "pruebas.h"
#include "C50.h"

unsigned long tiempo = 0;
uint8_t useMethod = PCe;

void setup() {
 Serial.begin(9600);
 pinMode( Presion, INPUT);
 pinMode( ledPin, OUTPUT);
 pinMode( Bomba1, OUTPUT);
 pinMode( Bomba2, OUTPUT);
 pinMode( co2_1, INPUT);
 pinMode( co2_2, INPUT);
 pinMode( valv_blanca_1, OUTPUT);
 pinMode( valv_negra_2, OUTPUT);
 pinMode( valv_blanca_2, OUTPUT);
 pinMode( valv_negra_1, OUTPUT);
 pinMode( pin_switch, INPUT);
 
 init();
}

void loop() {
  tiempo = micros();
  float escaner_value=lectura_escaner();
  lectura_sensor();
  controla_bombas();
  
  useMethod = digitalRead(pin_switch);

  if ( sensor_co2_1 > 4.95 ) // Sensor saturado
    init();
  
  if (useMethod == Ce50) {
     Serial.println("C50");
     C50();
  }
  else if (useMethod == PCe) {
     Serial.print("DM: ");
     PC(escaner_value,tiempo );
  }
}

void init() {
 estado_deadspace();

 if (useMethod == Ce50) 
   C50_init();
 else if (useMethod == PCe)
   PC_init();
  
}

