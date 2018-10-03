#include <SPI.h>
#include <RH_RF22.h>

#include <RTCCounter.h>
int cnt;
void watchdog();
bool LEDSTATE = false;
Counter watchdogTimer; // creates timer object


RHHardwareSPI spi;
RH_RF22 radio(SPI_CS_RFM, RF_NIRQ, spi);
byte RcvSequence[450];
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

  if(!radio.init()) {
    SerialUSB.println("We have a problem...");
    SerialUSB.println(radio.statusRead(), HEX);
  }
  else {
    SerialUSB.println("Good to go...");
    digitalWrite(LED_BUILTIN, HIGH);
  }
  radio.setFrequency(437.505, 0.1);
  radio.setModemRegisters(&FSK1k2);
  radio.setTxPower(RH_RF22_RF23BP_TXPOW_30DBM);
  //radio.setTxPower(RH_RF22_TXPOW_1DBM );
}

unsigned int n = 1;
void loop()
{
  SerialUSB.println("Transmitting...");
  radio.send(packet, 95);
  radio.waitPacketSent(2000);

SerialUSB.println("Listening...");
if (radio.waitAvailableTimeout(10000))
  { 
    // Should be a reply message for us now   
    if (radio.recv(RcvSequence, &len))
    {
      SerialUSB.println("Got a packet!");
      Demod(RcvSequence,450);
    }
    else SerialUSB.println("Decode failed");
  }
}


void Demod(byte *Buffer, uint8_t bytelength)
{
  
    byte BitSequence[bytelength*8];
    byte ByteSequence[bytelength];
    byte BitSequence_temp[bytelength*8];
    byte ByteSequence_temp[bytelength];
    char Message[256];
    byte Checksum[3];
    char DestCS[7];
    char SourceCS[7];
    int k = 0; //general counter
    int _size = 0;
    int s = 0;
    uint8_t cnt = 0 ;//Bit stuff counter  
    uint8_t extraBit = 0;
    uint8_t extraByte = 0;
    byte temp = 0;
    boolean pastFlag;
    boolean BitFound;

    //Initialization
    for (int i=0; i < bytelength*8 ; i++) BitSequence[i] = 0x00;  
    for (int i=0; i < bytelength*8 ; i++) BitSequence_temp[i] = 0x00; 
    for (int i=0; i < bytelength ; i++) ByteSequence[i] = 0x00; 
    for (int i=0; i < bytelength ; i++) ByteSequence_temp[i] = 0x00; 
   
    //Convert bits to byte size
    for (int i = 0; i< bytelength ; i++)
    {
      for (register uint8_t t=128; t>0 ; t = t/2) {
        if (Buffer[i] & t) BitSequence[_size++] = 0x01;
        else BitSequence[_size++] = 0x00;
       }       
    }
   
    for (int i=1; i < _size ; i++) 
    {
       if (BitSequence[i] == BitSequence[i-1]) 
       {
         BitSequence_temp[i-1] = 0x01;
       } else BitSequence_temp[i-1] = 0x00;
       
    }

    //Convert bit to Byte
    k = 0;
    for (int i = 0; i < _size-1; i = i + 8)
    {
        temp = 0;
        if  (BitSequence_temp[i] == 0x01)   temp = temp + 0b10000000;
        if  (BitSequence_temp[i+1] == 0x01) temp = temp + 0b01000000;
        if  (BitSequence_temp[i+2] == 0x01) temp = temp + 0b00100000;
        if  (BitSequence_temp[i+3] == 0x01) temp = temp + 0b00010000;
        if  (BitSequence_temp[i+4] == 0x01) temp = temp + 0b00001000;
        if  (BitSequence_temp[i+5] == 0x01) temp = temp + 0b00000100;
        if  (BitSequence_temp[i+6] == 0x01) temp = temp + 0b00000010;
        if  (BitSequence_temp[i+7] == 0x01) temp = temp + 0b00000001;
        ByteSequence[k++] = temp;
    }
//Test
//    radio.printBuffer("NRZI:", ByteSequence, k);

    pastFlag = false;
    cnt = 0;
    //Find and Remove Flags
    for (int i = 0; i < k; i++)
    {
       if (ByteSequence[i] != FLAG)
       {
          pastFlag = true;
          ByteSequence_temp[cnt++] = ByteSequence[i]; 
       } else if (pastFlag) break;
    }
    
//Test
//    radio.printBuffer("Removed Flags:", ByteSequence_temp, cnt);
    
    //Re-init
    for (int i=0; i < bytelength*8 ; i++) BitSequence[i] = 0x00;
    k = 0;
    
    //Convert bits to byte size
    for (int i = 0; i< cnt ; i++)
    {
      for (register uint8_t t=128; t>0 ; t = t/2) {
        if (ByteSequence_temp[i] & t) BitSequence[k++] = 0x01;
        else BitSequence[k++] = 0x00;
       }       
    }
   
   //Re-init
   for (int i=0; i < bytelength*8 ; i++) BitSequence_temp[i] = 0x00;
   
   //Bit unstuff : Remove 0 after five consecutive 1s.
   cnt = 0;
   s = 0;
   BitFound = false;
   extraBit = 0;

   for (int i = 0; i < k ; i++)
   {
      if (BitFound) 
      {
        BitFound = false;
        extraBit++;
        continue;
      }
      
      if (BitSequence[i] == 0x01) cnt++;
      else cnt = 0; // restart count at 1

      if (cnt == 5) // there are five consecutive bits of the same value
      {
          BitFound = true;
          cnt = 0; // and reset cnt to zero
      }
      BitSequence_temp[s++] = BitSequence[i]; // add the bit to the final sequence
    }
    
    extraByte = (extraBit / 8);
    if ( ((extraBit) % 8) > 0) extraByte++ ;
    
    //Re-init ByteSequence
    for (int i=0; i < bytelength ; i++) ByteSequence[i] = 0x00; 
    //Convert bit to Byte
    k = 0;
    for (int i = 0; i < s - extraByte*8; i = i + 8)
      {
        temp = 0;
        if  (BitSequence_temp[i] == 0x01)   temp = temp + 0b10000000;
        if  (BitSequence_temp[i+1] == 0x01) temp = temp + 0b01000000;
        if  (BitSequence_temp[i+2] == 0x01) temp = temp + 0b00100000;
        if  (BitSequence_temp[i+3] == 0x01) temp = temp + 0b00010000;
        if  (BitSequence_temp[i+4] == 0x01) temp = temp + 0b00001000;
        if  (BitSequence_temp[i+5] == 0x01) temp = temp + 0b00000100;
        if  (BitSequence_temp[i+6] == 0x01) temp = temp + 0b00000010;
        if  (BitSequence_temp[i+7] == 0x01) temp = temp + 0b00000001;
        ByteSequence[k++] = temp;
      }
    
 //   Serial.println("Received Stream"); 
 //   radio.printBuffer("received:", ByteSequence, k);
    //for (int i=0 ; i < k; i++) Serial.print(ByteSequence[i],HEX);
    //SerialUSB.println(""); 
    
    //Check if message has errors
    //Compute FCS on received byte stream
    FCS = 0;
    FCS = CRC_CCITT(ByteSequence, k-2);
    
    Checksum[1] = ByteSequence[k-2];
    Checksum[2] = ByteSequence[k-1];
    
    //Serial.println("Checksums : ");
    //Serial.println(Checksum[1],HEX);
    //Serial.println(Checksum[2],HEX);
    //Serial.println("FCS in LSB: ");
    //Serial.print(FCS,HEX);
    //Serial.println("Checksums computed: ");
    //Serial.print((FCS >> 8) & 0xff,HEX);
    //Serial.print(FCS & 0xff,HEX);
    
    if (Checksum[1] != ((FCS >> 8) & 0xff))
    {
      SerialUSB.println("Error in Checksum 1 : ");
      SerialUSB.print(Checksum[1]);SerialUSB.print(" != ");SerialUSB.println((FCS >> 8) & 0xff);
    } 
    if (Checksum[2] != (FCS & 0xff))
    {
      SerialUSB.println("Error in Checksum 2: ");
      SerialUSB.print(Checksum[2]);SerialUSB.print(" != ");SerialUSB.println(FCS & 0xff);
    }
    
    //Convert form LSB to MSB
    for (int i=0; i < bytelength ; i++) ByteSequence_temp[i] = 0x00; 
    for (int i=0; i < k-2 ; i++) ByteSequence_temp[i] = MSB_LSB_swap_8bit(ByteSequence[i]);
    
    cnt = 0;
    //Recover header
    for (int i=0; i < 6; i++) DestCS[i] = char(ByteSequence_temp[cnt++]>>1);

    //SSID Destination
    cnt++; 

    //Append Source Callsign
    for (int i=0; i < 6; i++) SourceCS[i] = char(ByteSequence_temp[cnt++]>>1);

    //Append SSID Source
    cnt++;
    //Append Control bits
    cnt++;
    //Append Protocol Identifier
    cnt++;
    //Recover message
    s = k-2-cnt;
    SerialUSB.println("Decoded Message: ");
    for (int i=0; i < s; i++) 
    {
      Message[i] = char(ByteSequence_temp[cnt++]);
      SerialUSB.print(Message[i]);
    }
    SerialUSB.println("\n");
}

unsigned int CRC_CCITT (byte *Buffer, uint8_t bytelength)
{
  uint8_t OutBit = 0;
  unsigned int XORMask = 0x0000;
  unsigned int SR = 0xFFFF;
  
  for (int i=0; i<bytelength ; i++)
  {
    for (uint8_t b = 128 ; b > 0 ; b = b/2) {
       
      OutBit = SR & 1 ? 1 : 0; //Bit shifted out of shift register
    
      SR = SR>>1; // Shift the register to the right and shift a zero in

      XORMask = logicXOR((Buffer[i] & b),OutBit) ? MSB_LSB_swap_16bit(CRC_POLYGEN) : 0x0000;

      SR = SR ^ XORMask;
    }
  }
  return  MSB_LSB_swap_16bit(~SR);  
}

boolean logicXOR(boolean a, boolean b)
{
  return (a||b) && !(a && b); 
}

byte MSB_LSB_swap_8bit(byte v)
{
  // swap odd and even bits
  v = ((v >> 1) & 0x55) | ((v & 0x55) << 1);
  // swap consecutive pairs
  v = ((v >> 2) & 0x33) | ((v & 0x33) << 2);
  // swap nibbles ... 
  v = ((v >> 4) & 0x0F) | ((v & 0x0F) << 4);
  return v;
}

unsigned int MSB_LSB_swap_16bit(unsigned int v)
{
  // swap odd and even bits
  v = ((v >> 1) & 0x5555) | ((v & 0x5555) << 1);
  // swap consecutive pairs
  v = ((v >> 2) & 0x3333) | ((v & 0x3333) << 2);
  // swap nibbles ... 
  v = ((v >> 4) & 0x0F0F) | ((v & 0x0F0F) << 4);
  // swap bytes
  v = ((v >> 8) & 0x00FF) | ((v & 0x00FF) << 8);  
  return v;
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



