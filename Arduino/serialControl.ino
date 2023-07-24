#define IN1_PIN 3
#define IN2_PIN 4
#define IN3_PIN 5
#define IN4_PIN 6
#define IN_1 7
#define IN_2 8
#define IN_3 9
#define IN_4 10
// #define maxSpeed 208
// #define minSpeed 70


void setup() {
  Serial.begin(9600);
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  pinMode(IN3_PIN, OUTPUT);
  pinMode(IN4_PIN, OUTPUT);
  pinMode(IN_1, OUTPUT);
  pinMode(IN_2, OUTPUT);
  pinMode(IN_3, OUTPUT);
  pinMode(IN_4, OUTPUT);
}

void stop(){
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  digitalWrite(IN4_PIN, LOW);
  digitalWrite(IN_1, LOW);
  digitalWrite(IN_2, LOW);
  digitalWrite(IN_3, LOW);
  digitalWrite(IN_4, LOW);
}

void stop(float second){
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  digitalWrite(IN4_PIN, LOW);
  delay(second*1000);
}

void startEngine(){
  digitalWrite(IN_1, HIGH);
  digitalWrite(IN_2, LOW);
  digitalWrite(IN_3,LOW);
  digitalWrite(IN_4, HIGH);
}

void forward(float second){
  startEngine();
  digitalWrite(IN1_PIN, HIGH);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  digitalWrite(IN4_PIN, HIGH);
  delay(second*1000);
  Serial.println("Done executing");
}

void backward(float second){
  startEngine();
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, HIGH);
  digitalWrite(IN3_PIN, HIGH);
  digitalWrite(IN4_PIN, LOW);
  delay(second*1000);
  Serial.println("Done executing");
}

void rotateLeft(float second){
  startEngine();
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, HIGH);
  digitalWrite(IN3_PIN, LOW);
  digitalWrite(IN4_PIN, HIGH);
  delay(second*1000);
  stop();
  Serial.println("Done executing");
}
void rotateRight(float second){
  startEngine();
  digitalWrite(IN1_PIN, HIGH);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, HIGH);
  digitalWrite(IN4_PIN, LOW);
  delay(second*1000);
  stop();
  Serial.println("Done executing");
}


void loop() {
   startEngine();
   if (Serial.available()){
    char msg = Serial.read();
    if (msg == '2'){
      backward(0.3);
    }
    else if (msg == '4'){
      rotateLeft(0.3);
    }
    else if (msg == '6'){
      rotateRight(0.3);
    }
    else if (msg == '8'){
      forward(0.3);
    }

    else if (msg == '1'){
      rotateLeft(0.5);
    }
    else if (msg == '3'){
      rotateLeft(0.3);
    }
    else if (msg == '5'){
      forward(10);
    }
    else if (msg == '7'){
      rotateRight(0.3);
    }
    else if (msg == '9'){
      rotateRight(0.5);
    }
    else{
      stop(0.2);
    }
  }
  else{
    stop(0.1);
  }
}