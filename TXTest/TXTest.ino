#include <SPI.h>
#include <RH_RF22.h>

#include <RTCCounter.h>
void watchdog();
Counter watchdogTimer; // creates timer object

RHHardwareSPI spi;
RH_RF22 radio(SPI_CS_RFM, RF_NIRQ, spi);

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
  digitalWrite(RF_SDN, HIGH);
  delay(2000);
  digitalWrite(RF_SDN, LOW);
  delay(500);

  if(!radio.init()) {
    SerialUSB.println("We have a problem...");
    SerialUSB.println(radio.statusRead(), HEX);
  }
  else {
    SerialUSB.println("Good to go...");
    digitalWrite(LED_BUILTIN, HIGH);
  }
  radio.setModemConfig(radio.FSK_Rb_512Fd2_5);
  radio.setFrequency(437.505, 0.1);
  radio.setTxPower(RH_RF22_RF23BP_TXPOW_28DBM);
}

unsigned int n = 1;
void loop()
{
  radio.setModeTx();
  SerialUSB.println("Transmitting");
  radio.send((const uint8_t*)"Testing123", 10);
  radio.waitPacketSent(2000);
  radio.setModeIdle();
  delay(3000);
}

void watchdog() { // Function that runs every time watchdog timer triggers
  digitalWrite(WDT_WDI, HIGH);
  delayMicroseconds(2);
  digitalWrite(WDT_WDI, LOW);
}

