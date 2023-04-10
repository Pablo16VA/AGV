#include <SoftwareSerial.h>
#include <Leddar2.h>

char buffer_in[10];
char buffer_out[10];
char input_message_size=1;
char output_message_size=3;
uint8_t dato=0;

LeddarOne Leddar1(115200,1);;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial1.begin(115200);
  Serial2.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  unsigned int Distance = 0;
  unsigned int Amplitude = 0;

  
  if(Serial.available()>0) {
    Serial.readBytes(buffer_in,input_message_size);
    if(buffer_in[0]=='M'){
      char result = Leddar1.getDetections();
      if (result >= 0)
      {
        // Show the first detection only
        Distance = Leddar1.Detections[0].Distance;
        Amplitude = Leddar1.Detections[0].Amplitude;
      }
        buffer_out[0]='R';
        buffer_out[1]=highByte(Distance);
        buffer_out[2]=lowByte(Distance);
        Serial.write(buffer_out,output_message_size);   
      }
  }
}
