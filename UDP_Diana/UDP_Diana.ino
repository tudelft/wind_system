#include <SPI.h>
#include <Ethernet2.h>
#include <EthernetUdp2.h>

#define MAX_RCV_BUF 256
#define UDP_COM_RATE 0.5 //Hz

struct FanData
{
  uint16_t status;  // 2byte == short on windows
  uint16_t fan[9]; 
};  // total length == 4 bytes

#if defined(WIZ550io_WITH_MACADDRESS) // Use assigned MAC address of WIZ550io;
#else

#define NUMBER   103

//byte g_mac[] = { 0x20, 0xA2, 0xDA, 0x10, 0x3A, 0x1C}; // 2
//byte g_mac[] = { 0x20, 0xA2, 0xDA, 0x10, 0x3A, 0x1D}; //3
byte g_mac[] = { 0x20, 0xA2, 0xDA, 0x10, 0x3A, NUMBER}; //4
//byte g_mac[] = { 0x20, 0xA2, 0xDA, 0x10, 0x3A, 0x1A}; //5
#endif
EthernetClient client;

//IPAddress g_myIp(192, 168, 1, 102); //2
//IPAddress g_myIp(192, 168, 1, 103);  //3
IPAddress g_myIp(192, 168, 1, NUMBER);  //4
//IPAddress g_myIp(192, 168, 1, 105);  //5
unsigned int g_myPort = 8888;

IPAddress g_targetIp(192, 168, 1, 1);
unsigned int g_targetPort = 8000;

EthernetUDP g_handle;

byte g_rcvBuffer[MAX_RCV_BUF];

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

void setup() 
{
   // Startup serial
  Serial.begin(9600);
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
    Serial.println("Starting up...");
    delay(5000);
    g_handle.begin(g_myPort);
    // print your local IP address:
    
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
    
        sendFanData(hbt->status, hbt->fan[0]);
    }
}

void sendFanData(int count, int val)
{
    Serial.print("Send ");
    Serial.println( count);
    // Create a packet
    FanData hbt;
    hbt.status = count;
    for (int i=0;i<9;i++) {
      hbt.fan[i] = val;
    }

    // Send the data
    txPacket((byte*)&hbt, sizeof(FanData), g_targetIp, g_targetPort, g_handle);
}
