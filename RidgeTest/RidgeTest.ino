#include <SPI.h>
#include <RH_RF22.h>

#include <RTCCounter.h>
int cnt;
void watchdog();
bool LEDSTATE = false;
Counter watchdogTimer; // creates timer object


RHHardwareSPI spi;
RH_RF22 radio(SPI_CS_RFM, RF_NIRQ, spi);
uint8_t RcvSequence[450];
uint8_t len = sizeof(RcvSequence);
unsigned int FCS = 0;
#define FLAG 0x7E
//Protocol Identifier. 0xF0 means : No Layer 3 protocol implemented
#define PID 0xF0
//Control Field Type for Unnumbered Information Frames : 0x03
#define CONTROL 0x03
#define MAX_LENGTH 280
#define MAX_LENGTH_FINAL 450
//CRC-CCITT
#define CRC_POLYGEN     0x1021

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
                   
uint8_t packet[] = {
  0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111,
  0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111,
  0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111,
  0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111,
  0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111,
  0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111,
  0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111,
  0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111,
  0b01110101, 0b10010110, 0b01010100, 0b10101011, 0b01010100, 0b10101011, 0b01010111, 0b01110010,
  0b01011010, 0b01001000, 0b10110101, 0b10101101, 0b10001010, 0b00101000, 0b11101010, 0b10101111,
  0b10110011, 0b00110111, 0b00010000, 0b10110000, 0b11011000, 0b10000111, 0b00001000, 0b10101001,
  0b00101110, 0b10010001, 0b00010001, 0b00000011, 0b01111101, 0b11000000, 0b01111111
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
  digitalWrite(RF_SDN, HIGH);
  delay(2000);
  digitalWrite(RF_SDN, LOW);
  delay(500);

  //Fill receive buffer with 0s
  for(int k = 0; k < len; ++k) {
    RcvSequence[k] = 0;
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
  radio.setFrequency(437.505, 0.1);
  radio.setTxPower(RH_RF22_RF23BP_TXPOW_30DBM);
  //radio.setTxPower(RH_RF22_TXPOW_1DBM );
}

unsigned int n = 1;
void loop()
{
//  SerialUSB.println("Transmitting...");
//  radio.setModemRegisters(&FSK1k2);
//  radio.setTxPower(RH_RF22_RF23BP_TXPOW_30DBM);
//  radio.send(packet, 95);
//  radio.waitPacketSent(2000);
//  radio.setModeIdle();

SerialUSB.println("Listening...");
radio.setModemConfig(radio.FSK_Rb_512Fd2_5);
if (radio.waitAvailableTimeout(15000))
  { 
    // Should be a reply message for us now   
    if (radio.recv(RcvSequence, &len))
    {
      SerialUSB.println("Got a packet!");
      SerialUSB.println((char*)RcvSequence);
    }
    else SerialUSB.println("Decode failed");
  }
}

void watchdog() { // Function that runs every time watchdog timer triggers
  digitalWrite(WDT_WDI, HIGH);
  delayMicroseconds(2);
  digitalWrite(WDT_WDI, LOW);
//  if (LEDSTATE) {
//    digitalWrite(LED_BUILTIN, HIGH);
//  } else {
//    digitalWrite(LED_BUILTIN, LOW);
//  }
//  LEDSTATE = !LEDSTATE;
}



