/* Not So Wireless Wireless Joystick USB Example
 * by: Alex Wende
 * SparkFun Electronics
 * date: 9/28/16
 * 
 * license: Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)
 * Do whatever you'd like with this code, use it for any purpose.
 * Please attribute and keep this license.
 * 
 * This example sends ASCII arrow key characters over USB when the left
 * joystick is moved or a space character when right trigger button is pressed.
 */


#define H_JOYSTICK    A2
#define V_JOYSTICK    A3
#define Y_TRIGGER     8
#define X_TRIGGER     4
#define B_TRIGGER     9
#define A_TRIGGER     2

struct sticks{
    uint8_t vertical;
    uint8_t horizontal;
};
union unSticks {
  unsigned int Full;
  sticks VuH;
} mov;
int h=0;
uint8_t inicio=0x80;
uint8_t fin=0xff;
uint8_t Vant=0;
uint8_t Hant=0;

void setup() {
  SerialUSB.begin(115200);
  Serial1.begin(9600);
  pinMode(Y_TRIGGER, INPUT_PULLUP);
  pinMode(A_TRIGGER, INPUT_PULLUP);
  pinMode(B_TRIGGER, INPUT_PULLUP);
  pinMode(X_TRIGGER, INPUT_PULLUP);
}

void loop() {
  int hStick = analogRead(H_JOYSTICK);
  int vStick = analogRead(V_JOYSTICK);
  mov.VuH.horizontal=map(hStick,0,1023,0,253);
  mov.VuH.vertical=map(vStick,0,1023,0,254);
  if(digitalRead(X_TRIGGER)==LOW) {
    mov.VuH.horizontal=253;
    mov.VuH.vertical=255;
  }
  if(digitalRead(Y_TRIGGER)==LOW) {
    mov.VuH.horizontal=254;
    mov.VuH.vertical=254;
  }
  if(digitalRead(A_TRIGGER)==LOW) {
    mov.VuH.horizontal=254;
    mov.VuH.vertical=255;
  }
  if(digitalRead(B_TRIGGER)==LOW) {
    mov.VuH.horizontal=255;
    mov.VuH.vertical=254;
  }
  //Serial1.write(mov.Full);
  uint8_t inicio=0x80;
  uint8_t fin=0xff;
  if(abs(Vant-mov.VuH.vertical)>20||abs(Hant-mov.VuH.horizontal)>20){
    Serial1.write(inicio);
    Serial1.write(mov.VuH.vertical);
    Serial1.write(mov.VuH.horizontal);
    Serial1.write(fin);
    
    SerialUSB.print("Vertical: ");
    SerialUSB.print(mov.VuH.vertical);
    SerialUSB.print(" Horizontal: ");
    SerialUSB.print(mov.VuH.horizontal);
    SerialUSB.print(" FULL: ");
    SerialUSB.println(mov.Full, BIN);
  }
  //Serial1.println();
  Vant=mov.VuH.vertical;
  Hant=mov.VuH.horizontal;
  delay(100);
}
