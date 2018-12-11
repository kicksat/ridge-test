#include <SPI.h>
#include <RH_RF22.h>

#include <RTCCounter.h>
void watchdog();
Counter watchdogTimer; // creates timer object

RHHardwareSPI spi;
RH_RF22 radio(SPI_CS_RFM, RF_NIRQ, spi);
uint8_t RcvBuffer[255];
uint8_t bufLen = sizeof(RcvBuffer);
uint8_t rcvLen = bufLen;

RH_RF22::ModemConfig FSK1k2 = {
  0x2B, //reg_1c
  0x03, //reg_1f
  0x41, //reg_20
  0x60, //reg_21
  0x27, //reg_22
  0x52, //reg_23
  0x00, //reg_24
  0x9F, //reg_25
  0x2C, //reg_2c - Only matters for OOK mode
  0x11, //reg_2d - Only matters for OOK mode
  0x2A, //reg_2e - Only matters for OOK mode
  0x80, //reg_58
  0x60, //reg_69
  0x09, //reg_6e
  0xD5, //reg_6f
  0x24, //reg_70
  0x22, //reg_71
  0x01  //reg_72
};

void setup() 
{

  watchdogTimer.init(1,watchdog); // timer delay, seconds
  pinMode(WDT_WDI, OUTPUT);
  digitalWrite(WDT_WDI, LOW);

  //Make sure other SPI devices are off
  pinMode(SPI_CS_XTB1, OUTPUT);
  digitalWrite(SPI_CS_XTB1, HIGH);
  pinMode(SPI_CS_XTB2, OUTPUT);
  digitalWrite(SPI_CS_XTB2, HIGH);
  pinMode(SPI_CS_XTB3, OUTPUT);
  digitalWrite(SPI_CS_XTB3, HIGH);
  pinMode(SPI_CS_XTB4, OUTPUT);
  digitalWrite(SPI_CS_XTB4, HIGH);
  pinMode(SPI_CS_SD, OUTPUT);
  digitalWrite(SPI_CS_SD, HIGH);
  pinMode(SPI_CS_MRAM, OUTPUT);
  digitalWrite(SPI_CS_MRAM, HIGH);

  SerialUSB.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(RF_SDN, OUTPUT);

  //Need a delay before turning on radio
  //so that power supply can stabilize
  digitalWrite(RF_SDN, LOW);

  //Fill receive buffer with 0s
  for(int k = 0; k < bufLen; ++k) {
    RcvBuffer[k] = 0;
  }

  if(!radio.init()) {
    SerialUSB.println("We have a problem...");
    SerialUSB.println(radio.statusRead(), HEX);
  }
  else {
    SerialUSB.println("Good to go...");
    digitalWrite(LED_BUILTIN, HIGH);
  }
  radio.setModemConfig(radio.FSK_Rb_512Fd2_5);
  //radio.setModemRegisters(&FSK1k2);
  radio.setFrequency(437.505, 0.05);
  radio.setTxPower(RH_RF22_RF23BP_TXPOW_30DBM);
  radio.setPromiscuous(true);
  radio.setModeRx();
  //radio.setTxPower(RH_RF22_TXPOW_1DBM );
}

void loop()
{
  while(radio.available() == 0) {
    delay(5000);
    SerialUSB.println("Listening...");
  }
  // Should be a reply message for us now   
  if (radio.recv(RcvBuffer, &rcvLen))
  {
    SerialUSB.println("Got a packet!");
    SerialUSB.println((char*)RcvBuffer);
  
    //Fill receive buffer with 0s
    for(int k = 0; k < rcvLen; ++k) {
      RcvBuffer[k] = 0;
    }
    rcvLen = bufLen;
  }
}

void watchdog() { // Function that runs every time watchdog timer triggers
  digitalWrite(WDT_WDI, HIGH);
  delayMicroseconds(2);
  digitalWrite(WDT_WDI, LOW);
}



