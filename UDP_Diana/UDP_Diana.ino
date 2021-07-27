// Ethernet
#include <SPI.h>
#include <Ethernet2.h>
#include <EthernetUdp2.h>

// PWM Out
#include <TimerThree.h>  // 2,3,5 
#include <TimerFour.h>  //6,7,8
#include <TimerFive.h> //44, 45, 46

///////////////////////////////////////////////////
// PWM

const int OutputPin[9] = {2,3,5,6,7,8,44,45,46}; // Pin at which duty cycle output will be written

#define INIT_PWM 0


///////////////////////////////////////////////////
// PROTOCOL

struct FanData
{
  uint16_t status;  // 2byte == short on windows
  uint16_t fan[9]; 
};  // total length == 20 bytes



///////////////////////////////////////////////////
// ETHERNET
#define NUMBER   103

byte g_mac[] = { 0x20, 0xA2, 0xDA, 0x10, 0x3A, NUMBER}; //4

EthernetClient client;
EthernetUDP g_handle;

IPAddress g_myIp(192, 168, 1, NUMBER);  //4
unsigned int g_myPort = 8888;

IPAddress g_targetIp(192, 168, 1, 1);
unsigned int g_targetPort = 8000;

#define MAX_RCV_BUF 256
byte g_rcvBuffer[MAX_RCV_BUF];



// todo
unsigned long g_timeNow = 0;
unsigned long g_lastUdpComTime = 0;

void txPacket(byte* txBuffer, int dataLen, IPAddress remoteIpNum, unsigned int remotePortNum, EthernetUDP handle)
{
    handle.beginPacket(remoteIpNum, remotePortNum);
    handle.write(txBuffer, dataLen);
    handle.endPacket();
}

bool checkForPacket(byte* rcvBuf, int maxBufLen, int* packetSize, EthernetUDP handle)
{
    //startoff assuming we dont have a packet
    bool foundPacket = false;
    
    //find the size (if any) of packet in buffer
    *packetSize = handle.parsePacket();
    
    //if the packet is -1 or 0 length (no packet) pass it, else (go inside if) it has a length, read it!
    if (*packetSize)
    {
        //Read in the packet
        handle.read(rcvBuf, maxBufLen);

        //Tell the caller we found a packet          
        foundPacket = true;
    }
    
    return foundPacket;
}


void set_fans(uint16_t fans[9]) {

  for (int i = 0; i <= 2; i++) {
    Timer3.setPwmDuty(OutputPin[i], fans[i]);
  }
  for (int j = 3; j <= 5; j++) {
    Timer4.setPwmDuty(OutputPin[j], fans[j]);
  }
  for (int k = 6; k <= 8; k++) {
     Timer5.setPwmDuty(OutputPin[k], fans[k]);
  }
}

void setup() 
{
   // Startup serial
  Serial.begin(57600);             
  Serial.flush();
  Serial.print("DIANA FAN SYSTEM");  


  // PWM Init
  Timer3.initialize(40);  //40 us = 25 kHz ..36-46
  Timer4.initialize(40);  
  Timer5.initialize(40);
  for (int i = 0; i <= 2; i++) {
    Timer3.pwm(OutputPin[i], INIT_PWM);
  }
  for (int j = 3; j <= 5; j++) {
    Timer4.pwm(OutputPin[j], INIT_PWM);
  }
  for (int k = 6; k <= 8; k++) {
    Timer5.pwm(OutputPin[k], INIT_PWM);
  }

  uint16_t fans[9] = { 0, 400, 0, 400, 0, 400, 0, 800, 0};
  set_fans(fans);


  // Ethernet
  Ethernet.init(10); // SS pin changed from default pin 10 to 53
  // start the Ethernet connection:
  Ethernet.begin(g_mac,g_myIp);
  // print your local IP address:
  Serial.print("My IP address: ");
  for (byte thisByte = 0; thisByte < 4; thisByte++) {
    // print the value of each byte of the IP address:
    Serial.print(Ethernet.localIP()[thisByte], DEC);
    Serial.print("."); 
  }
  Serial.println();


  // Print out begining
  delay(5000);
  g_handle.begin(g_myPort);
    
  Serial.print("My IP address: ");
  for (byte thisByte = 0; thisByte < 4; thisByte++) {
    // print the value of each byte of the IP address:
    Serial.print(Ethernet.localIP()[thisByte], DEC);
    Serial.print("."); 
  }  

}

void loop() 
{
    // Only handle coms every second
    //g_timeNow = micros();
    //if(g_timeNow-g_lastUdpComTime >= (1.0/UDP_COM_RATE)*1000000.0)
    //{
    //    Serial.println("Handle Coms v2");
        receiveFanData();
    //    g_lastUdpComTime = g_timeNow;
    //}
}

void receiveFanData()
{
    int packetSize;
    bool foundPacket = checkForPacket((byte*)&g_rcvBuffer, MAX_RCV_BUF, &packetSize,  g_handle);
    if(foundPacket)
    {
        FanData* hbt = (FanData*)&g_rcvBuffer;

        
        Serial.print("FanData! Status: ");
        Serial.print(hbt->status);
        Serial.print(", random value ");
        Serial.println(hbt->fan[0]);
        set_fans(hbt->fan);
    
        sendFanData(hbt->status, hbt->fan[0]);
    }
}

void sendFanData(int count, int val)
{
    // Create a packet
    FanData hbt;
    hbt.status = count;
    for (int i=0;i<9;i++) {
      hbt.fan[i] = val;
    }

    // Send the data
    txPacket((byte*)&hbt, sizeof(FanData), g_targetIp, g_targetPort, g_handle);
}
