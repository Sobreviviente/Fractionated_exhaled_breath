
float sensor_p=0;  // valor de sensor presion
float sensor_co2_1=0;  //valor de sensor co2 primer cable 
float sensor_co2_2=0;  //valor de sensor co2 segundo cable
boolean Key = false;
int mensaje=0;
const int ledPin = 13; 
const int Bomba1 = 11;
const int Bomba2 = 12;
const int co2_1 = 23;
const int co2_2 = 22;
const int valv_blanca_1 = 16;
const int valv_negra_2 = 17;
const int valv_blanca_2 = 18;
const int valv_negra_1 = 19; 
#define umbral_high 2.8
#define umbral_low 2.6

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

}

void loop() {

  lectura_sensor();
  controla_bombas();
  
  
  
  if(Serial.available()>0){
    mensaje=Serial.read();
    if (mensaje=='1'){
      Key=true;
    }  
    else{
      Key=false;
    }
  }
  if (Key==true){
  digitalWrite(valv_negra_2, HIGH); 
  digitalWrite(valv_blanca_2, LOW);
  digitalWrite(valv_negra_1, LOW);
  digitalWrite(valv_blanca_1, LOW);
  delay(5000);
  digitalWrite(valv_negra_2, LOW);
  digitalWrite(valv_blanca_2,HIGH);
  digitalWrite(valv_negra_1, LOW);
  digitalWrite(valv_blanca_1, LOW);
  delay(5000);
  //lectura_escaner();
}
}

void lectura_sensor(){
  float cValue = (5.0*analogRead(20))/1023.0;
  sensor_p = 0.95*sensor_p + 0.05*cValue;
  Serial.println(sensor_p,4);
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
  Serial.print(sensor_co2_1,4);
  Serial.print(",");
  Serial.println(sensor_co2_2,4);
}
  
  // put your main code here, to run repeatedly:



