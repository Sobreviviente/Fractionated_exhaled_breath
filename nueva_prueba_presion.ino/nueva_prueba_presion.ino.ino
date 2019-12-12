#include <AMS.h>

float Pressure;
float Temperature;
String DataString;
char PrintData[48];

AMS AMSa(5915, 0x28,0,5);

const int analogInPin = A1; // Analog input pin, connected to pressure sensor
const int analogButton = A0; // Button

float inputVolt = 0; // Voltage read from pressure sensor (in bits, 0 to 1023)
float volt_0 = 2.5; //Initial voltage
float volt = 0; // Voltage (converted from 0-255 to 0-5)
float pressure_psi = 0; // Pressure value calculated from voltage, in psi
float pressure_pa = 0; // Pressure converted to Pa
float massFlow = 0; // Mass flow rate calculated from pressure
float volFlow = 0; // Calculated from mass flow rate
float volume = 0; // Integral of flow rate over time
float pressure_psi_sensor = 0; 

// float vs = 5 ; // Voltage powering pressure sensor
float rho = 1.225; // Density of air in kg/m3
float area_1 = 0.000415; // Surface area in m2
float area_2 = 0.0000283; // Surface area in m2
float dt = 0;
int button = 0; // Value of button


void setup() {
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.write("prueba");
  if (AMSa.Available() == true) {
    //read the sensor's pressure data only
    Serial.write("sensor disponible");
    Pressure = AMSa.readPressure();
    if (isnan(Pressure)) {
       Serial.write("Please check the sensor family name.");
    } else {
        DataString = String(Pressure) + " mbar \n";
        DataString.toCharArray(PrintData, 48);
        Serial.write(PrintData);
        pressure_psi_sensor=Pressure*0.0145038;
        }
  } else{
    Serial.write("Sensor no responde");
    }
  
  delay(10);
// inputVolt = analogRead(analogInPin); // Voltage read in (0 to 1023)
// volt = inputVolt*(vs/1023.0);
// pressure_psi = (15/2)*(volt-2.492669); // Pressure in psi
 pressure_pa = pressure_psi_sensor*6894.75729; // Pressure in Pa
 massFlow = 1000*sqrt((abs(pressure_pa)*2*rho)/((1/(pow(area_2,2)))-(1/(pow(area_1,2))))); // Mass flow of air
 volFlow = massFlow/rho; // Volumetric flow of air
 volume = volFlow*dt + volume; // Total volume (essentially integrated over time)
 dt = 0.001;
 Serial.println(volume);
 delay(1);


}
