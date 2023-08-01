#define IN1_PIN 3
#define IN2_PIN 4
#define IN3_PIN 5
#define IN4_PIN 6
#define IN_1 7
#define IN_2 8
#define IN_3 9
#define IN_4 10
const int maxSpeed = 255;
const int normSpeed = 60;
const int turnSpeed = 40;
const int minSpeed = 20;


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
  digitalWrite(IN_1, LOW);
  digitalWrite(IN_2, LOW);
  digitalWrite(IN_3,LOW);
  digitalWrite(IN_4, LOW);
}

void waitUntilRelease(){
    while (true){
    if (Serial.available()){
        String msg = Serial.readStringUntil('\n');
        if (msg == "stop"){
            break;
        }
    }
  }
  stop();
}

void forward(){
  startEngine();
  analogWrite(IN1_PIN, normSpeed);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  analogWrite(IN4_PIN, normSpeed);
  waitUntilRelease();
}

void backward(){
  startEngine();
  digitalWrite(IN1_PIN, LOW);
  analogWrite(IN2_PIN, normSpeed);
  analogWrite(IN3_PIN, normSpeed);
  digitalWrite(IN4_PIN, LOW);
  waitUntilRelease();
}

void rotateLeft(){
  startEngine();
  digitalWrite(IN1_PIN, LOW);
  analogWrite(IN2_PIN, turnSpeed);
  digitalWrite(IN3_PIN, LOW);
  analogWrite(IN4_PIN, turnSpeed);
  waitUntilRelease();
}
void rotateRight(){
  startEngine();
  analogWrite(IN1_PIN, turnSpeed);
  digitalWrite(IN2_PIN, LOW);
  analogWrite(IN3_PIN, turnSpeed);
  digitalWrite(IN4_PIN, LOW);
  waitUntilRelease();
}

void turnLeft(){
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  analogWrite(IN4_PIN, turnSpeed);
  waitUntilRelease();
}

void turnRight(){
  analogWrite(IN1_PIN, turnSpeed);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  digitalWrite(IN4_PIN, LOW);
  waitUntilRelease();
}

void forward(float second){
  startEngine();
  analogWrite(IN1_PIN, normSpeed);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  analogWrite(IN4_PIN, normSpeed);
  delay(second*1000);
  Serial.println("Done executing");
}

void backward(float second){
  startEngine();
  digitalWrite(IN1_PIN, LOW);
  analogWrite(IN2_PIN, normSpeed);
  analogWrite(IN3_PIN, normSpeed);
  digitalWrite(IN4_PIN, LOW);
  delay(second*1000);
  Serial.println("Done executing");
}

void rotateLeft(float second){
  startEngine();
  digitalWrite(IN1_PIN, LOW);
  analogWrite(IN2_PIN, turnSpeed);
  digitalWrite(IN3_PIN, LOW);
  analogWrite(IN4_PIN, turnSpeed);
  delay(second*1000);
  stop();
  Serial.println("Done executing");
}
void rotateRight(float second){
  startEngine();
  analogWrite(IN1_PIN, turnSpeed);
  digitalWrite(IN2_PIN, LOW);
  analogWrite(IN3_PIN, turnSpeed);
  digitalWrite(IN4_PIN, LOW);
  delay(second*1000);
  stop();
  Serial.println("Done executing");
}

void turnLeft(float second){
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  analogWrite(IN4_PIN, turnSpeed);
  delay(second*1000);
  stop();
  Serial.println("Done executing");
}

void turnRight(float second){
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  analogWrite(IN4_PIN, turnSpeed);
  delay(second*1000);
  stop();
  Serial.println("Done executing");
}

void slowAround(float second){
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  analogWrite(IN4_PIN, minSpeed);
  delay(second*500);
  stop(100);
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  analogWrite(IN4_PIN, minSpeed);
  delay(second*500);
  stop();
  Serial.println("Done executing");
}

void ctrlLeft(int leftSpeed, int rightSpeed, int second){
  digitalWrite(IN1_PIN, LOW);
  analogWrite(IN2_PIN, leftSpeed);
  digitalWrite(IN3_PIN, LOW);
  analogWrite(IN4_PIN, rightSpeed);
  delay(second*1000);
  stop();
  Serial.println("Done executing");
}

void ctrlRight(int leftSpeed, int rightSpeed, int second){
  analogWrite(IN1_PIN, leftSpeed);
  digitalWrite(IN2_PIN, LOW);
  analogWrite(IN3_PIN, rightSpeed);
  digitalWrite(IN4_PIN, LOW);
  delay(second*1000);
  stop();
  Serial.println("Done executing");
}

void stopForever(){
  while (true){
    stop();
  }
}

void caseChoose(String msg){
  if (msg == "backward"){
      backward();
    }
    else if (msg == "turnLeft"){
      turnLeft();
    }
    else if (msg == "turnRight"){
      turnRight();
    }
    else if (msg == "forward"){
      forward();
    }
  //automatic bottle centering control
    else if (msg == "farLeft"){
      turnLeft(0.5);
    }
    else if (msg == "farRight"){
      turnRight(0.5);
    }
    else if (msg == "nearLeft"){
      turnLeft(0.2);
    }
    else if (msg == "nearRight"){
      turnRight(0.2);
    }
    else if (msg == "outFrame"){
      slowAround(0.5);
    }
}

void loop() {
   startEngine();
   if (Serial.available()){
    String msg = Serial.readStringUntil('\n');
    msg.trim();
    caseChoose(msg);
  }
  else{
    stop(0.1);
  }
}