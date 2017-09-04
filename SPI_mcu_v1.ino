
#include <SPI.h>

byte message[10];

void setup() {


Serial.begin(9600);

SPI.begin();
SPI.setBitOrder(MSBFIRST);
SPI.setDataMode(SPI_MODE3);
SPI.setClockDivider(SPI_CLOCK_DIV128); // 16MHz / 128 = 125 kHz

delay(100);
busyPoll();
delay(100);
Serial.write("MaxCanonControl v0.2\n  ");

}

void loop() {
char message;

if (Serial.available() > 0)
{
  message = Serial.read();
  Serial.println(message);

if (message == 'f') {
  Serial.println("full opening\n");
  openAperture();
}
if (message == 'c') {
  Serial.println("closing 1/3");
  setFStop(0x02);
}

if (message == 'o') {
  Serial.println("opening 1/3");
  setFStop(0xFF);
}

if (message == 'e') {
  Serial.println("focusing deeper");
  focusRing(40);
}

if (message == 'a') {
  Serial.println("focusing closer");
  focusRing(-40);
}

if (message == 'i') {
  Serial.println("focusing");
  focusInf();
}
}
}

byte sendCommand(byte Cmd) {
byte Ack = SPI.transfer(Cmd);
delayMicroseconds(250);
return(Ack);
}

unsigned int busyPoll() {
byte *msg_ptr;
msg_ptr = &message[0];
*msg_ptr++ = sendCommand(0x0A);
*msg_ptr++ = sendCommand(0x00);
return(0);
}

unsigned int setFStop(byte f_value) {
byte *msg_ptr;
msg_ptr = &message[0];
*msg_ptr++ = sendCommand(0x07);
*msg_ptr++ = sendCommand(0x13);
*msg_ptr++ = sendCommand(f_value);
*msg_ptr++ = sendCommand(0x00);
return(0);
}

unsigned int focusRing(int d_value) {
byte *msg_ptr;
msg_ptr = &message[0];
byte low_byte = d_value & 0xFF;
byte high_byte = (d_value & 0xFF00) >> 8;
*msg_ptr++ = sendCommand(0x44);
*msg_ptr++ = sendCommand(high_byte);
*msg_ptr++ = sendCommand(low_byte);
return(0);
}

unsigned int focusInf() {
byte *msg_ptr;
*msg_ptr++ = sendCommand(0x4F);
*msg_ptr++ = sendCommand(0x50);
//*msg_ptr++ = sendCommand(0xA0);
return(0);
}

unsigned int openAperture() {
byte *msg_ptr;
msg_ptr = &message[0];
*msg_ptr++ = sendCommand(0x13);
*msg_ptr++ = sendCommand(0x80);
delay(200);
*msg_ptr++ = sendCommand(0x00);
return(0);
}


