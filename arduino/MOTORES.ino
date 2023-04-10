float PWM=5;
char buffer_in[10];
char buffer_out[10];
char input_message_size=3;
char output_message_size=2;
uint8_t HighV,LowV;

//Salidas del motor
const int PWMmotor=10;
const int DirMotor=8;
const int Enable=7;
//Señal de velocidad
const int VelSignal=2;

//Variables para detectar velocidad
double tiempo=0;
double df=0;
float velx=0;
float velxa=velx;
int bandera=0;

//Variables de para muestreo
float tiempo1=0;
float tiempoa=0;
float dt=0.05;
float contador=0;

//Variables para elegir voltaje de salida
float angulo=0;
float Voltx=0;
float valorx=0;

//Control
float KP=0.05;
float KI=0.1;
float integral=0;
float refkm=-20;
float ref=round(((refkm*1000)/3600)/0.175);
float refa=ref;
float error=0;
int contador2=0;
int oneB=0;
char one=0;
float karman=0.1;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  attachInterrupt( 0, Encoder, RISING); 
  pinMode(VelSignal,INPUT);
  
  pinMode(PWMmotor,OUTPUT);
  pinMode(DirMotor,OUTPUT);
  pinMode(Enable,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  tiempoa=tiempo1;
  tiempo1=millis();
  if(tiempoa>tiempo1) {
    tiempoa=tiempo1;
  }
  
  /**/
  if(Serial.available()>0) {
    Serial.readBytes(buffer_in,input_message_size);
    if(buffer_in[0]=='M'){
        HighV=buffer_in[1];
        LowV=buffer_in[2];
        PWM=(float(HighV))*256+float(LowV);
        PWM=PWM/1000;
        /*PWM=(PWM)/0.18;*/
        
        buffer_out[0]='R';
        buffer_out[1]='X';
        Serial.write(buffer_out,output_message_size);   
      }
  }
  ref=PWM-(5);
  if(ref>40){
    ref=40;
  }else if(ref<-40) {
    ref=-40;
  }
  if(refa==8||refa==-8) {
    if(ref<=-20||ref>=20) {
      ref=refa;
    }
  }
  refa=ref;
  error=ref-velx;
  integral=integral+error*((tiempo1-tiempoa)/1000);
  Voltx=KP*error+KI*integral;
  if(Voltx>=5) {
    Voltx=5;
  }else if(Voltx<=-5) {
    Voltx=-5;
  }
  if(ref>0) {
    Voltx=1.5;
  }else if(ref<0) {
    Voltx=-1.5;
  }else {
    Voltx=0;
  }
  Voltx=ref;
  valorx=(abs(Voltx)/5)*255;
  valorx=round(valorx);

  /*
  Serial.print(tiempo1);
  Serial.print(", ");
  Serial.print(Voltx);
  Serial.print(", ");
  Serial.print(valorx);
  Serial.print(", ");
  Serial.print(error);
  Serial.print(", ");
  Serial.print(df);
  Serial.print(", ");
  Serial.print(integral);
  Serial.print(", ");
  Serial.print(bandera);
  Serial.print(", ");
  Serial.print(ref);
  Serial.print(", ");
  Serial.print(PWM);
  Serial.print(", ");
  Serial.print(contador2);
  Serial.print(", ");
  Serial.println(velx);
  */    
  
  
  

  
  if(Voltx<0&&velx>0){
    Voltx=0;
    integral=0;
  }else if(Voltx>0&&velx<0) {
    Voltx=0;
    integral=0;
  }
  //valorx=map(abs(Voltx),0,5,0,255);  
  digitalWrite(Enable, HIGH);    
   if (Voltx>0&&velx==0) {
    bandera=0;
    digitalWrite(DirMotor,LOW);
   }else if(Voltx<0&&velx==0){
    bandera=1;
    digitalWrite(DirMotor,HIGH);
   }
   analogWrite(PWMmotor,valorx);
  if((micros()-tiempo)>500000) {
    velx=0; 
    velxa=velx;
  } 

  if(ref==0) {
    integral=0;
  }
  //while((millis()-tiempo1)<(0.05*1000)){}
}


void Encoder() 
   {
    delay(5);
    oneB=digitalRead(VelSignal);
    
    if(oneB==1) {
      //contador2=contador2+1;
      df=micros()-tiempo;
      tiempo=micros();
      df=df;
      
      
      //velx=(velx)/(30);
  
      if(bandera==0) {
        
        velx=1000000/(float (df));
        velx=(velx*2*PI)/(30);
        /*
          if(velx-velxa>5) {
          velx=velxa;
        }*/
        if(velx<0) {
          velx=velxa;
        }
      }else if(bandera==1){
        velx=-1000000/(float (df));
        velx=(velx*2*PI)/(30);
        /*
        if(velx-velxa<-5) {
          velx=velxa;
        }
        */
        if(velx>0) {
          velx=velxa;
        }
      }
      velx=velxa*(1-karman)+velx*karman;
      velxa=velx;
    }
    
    
    
    
   }
