#define PCe  0
#define Ce50 1
#define SUMA_TIEMPO 150000 // [ms]
float sensor_p=0;  // valor de sensor presion
float sensor_co2_1=0;  //valor de sensor co2 primer cable 
float sensor_co2_2=0;  //valor de sensor co2 segundo cable
char Key = '0';
int mensaje=0;
int estado_curva=0;
const int ledPin = 13; 
const int Bomba1 = 11;
const int Bomba2 = 12;
const int co2_1 = 23;
const int co2_2 = 22;
const int valv_blanca_1 = 16; //1 es el de la derecha
const int valv_negra_2 = 17;  // 2 es el de la izquierda 
const int valv_blanca_2 = 18;
const int valv_negra_1 = 19; 
unsigned long tiempo = 0;
unsigned long tiempo_t = 0;
uint8_t useMethod = PCe;
#define umbral_high 3.1
#define umbral_low 3.0
int estado_aux=0; 
float ultimos_3valores[3]={};
int c=0;
int pos=0;
float C50_maximo=-8;
float C50_minimo=8;
float C50_prom3=0;
bool C50_revisando = true;
unsigned long tiempo_trigger = 0; 

void setup() {
 Serial.begin(9600);
 pinMode( 20, INPUT); // pin 20 como input 
 pinMode( ledPin, OUTPUT);
 pinMode( Bomba1, OUTPUT);
 pinMode( Bomba2, OUTPUT);
 pinMode( co2_1, INPUT);
 pinMode( co2_2, INPUT);
 pinMode( valv_blanca_1, OUTPUT);
 pinMode( valv_negra_2, OUTPUT);
 pinMode( valv_blanca_2, OUTPUT);
 pinMode( valv_negra_1, OUTPUT);
  // put your setup code here, to run once:
  
  for (int i=0; i<3; i++){
      ultimos_3valores[i] = -1;
  }
}

void loop() {
  tiempo = millis();
  lectura_escaner();
  lectura_sensor();
  controla_bombas();

  if (useMethod == Ce50)
    C50();
  else if (useMethod == PCe)
    PC();
     
}

void C50_nuevoValor(float v) {
  c++;
  ultimos_3valores[c%3] = v;
}

void actualizar_promedio() {
  float prom = 0.0;
  for (int i=0; i<3; i++) {
    if (ultimos_3valores[i] == -1)
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



void PC() {
  if (estado_curva==0 && sensor_co2_1 > 3.0){    // CURVA SUBIENDO
    estado_curva=1;
  }
  else if (estado_curva==1 && sensor_co2_1 < 0.5){  // 
    estado_curva=2;
    tiempo_trigger = tiempo + SUMA_TIEMPO; 
  }
  else if (estado_curva=2 && tiempo>tiempo_trigger){            // TRIGGER 
    estado_curva=3;
  }
  else if(estado_curva=3 && sensor_co2_1<0.05){
    estado_curva=0;
  }
}

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

void lectura_sensor(){
  float cValue = (5.0*analogRead(20))/1023.0;
  sensor_p = 0.95*sensor_p + 0.05*cValue;
  //Serial.println(sensor_p,4);
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
void lectura_escaner(){
  sensor_co2_1 = (5.0*analogRead(23))/1023.0;
  sensor_co2_2 = (5.0*analogRead(22))/1023.0;
  //Serial.print (analogRead(23));
  //Serial.print(",");
  //Serial.print (analogRead(22));
  //Serial.print(",");
  //Serial.print(sensor_co2_1,4);
  //Serial.print(",");
  //Serial.println(sensor_co2_2,4);
}


void prueba_globos_alternando(){
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
  // put your main code here, to run repeatedly:

