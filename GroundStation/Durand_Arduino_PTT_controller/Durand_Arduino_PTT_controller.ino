/* 
*  Controll PTT lines for Durand ground station
*
*  Author: Tane Tatum
*  Updated: 2-9-19
*/

#define amp 13          // Pin number for TX/RX switch      (0V = OFF, 5V = TX) 
#define ampMon A0       // Moinitor Amp power output
#define txrxSwitch 12   // Pin connected to TX/RX switch (0V = TX, 5V/Float = RX)
#define LNA 11          // Pin number for LNA control box  (0V = OFF, 5V/Float = ON)

bool overTemp = true;

void setup() {
  digitalWrite(amp, LOW);          // Preset amp to off
  digitalWrite(txrxSwitch, HIGH);   // Preset TX/RX switch to RX
  digitalWrite(LNA, HIGH);          // Preset LNA to on
  pinMode(amp, OUTPUT);             // Set amp pin to output
  pinMode(txrxSwitch, OUTPUT);      // Set TX/RX switch pin to output
  pinMode(LNA, OUTPUT);             // Set LNA to output
  pinMode(ampMon, INPUT);           // Set amp monitor pin to input
  
  Serial.begin(9600);
  Serial.println("Arduino Conncected");
}

void loop() {
  // Respond to serial commands
  while(Serial.available()){
    int input = Serial.read();  // Read serial command
    input = input - 48;         // Switch input from ASCII to value

    // Evaluate Serial Command
    switch (input) {
      
      // Set to mode to TX
      case 0:
        digitalWrite(txrxSwitch, LOW);
        digitalWrite(LNA, LOW);
        digitalWrite(amp, HIGH);
        Serial.println("Set to TX");
      break;

      // Set mode to RX
      case 1:
        digitalWrite(txrxSwitch, HIGH);
        digitalWrite(LNA, HIGH);
        digitalWrite(amp, LOW);
        Serial.println("Set to RX");
      break;
      
      default:
        Serial.println("Invalid input");
      break;
    } 
  }
  delay(1);
}
