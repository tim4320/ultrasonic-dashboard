const int trigPin = 9;
const int echoPin = 10;
const int ledPin = 13;  // Use built-in LED or external one

float distance = 0;
bool ledState = false;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
}

void loop() {
  distance = readDistance();
  sendDistanceAndLED();

  checkSerialCommand();

  delay(200);  // Limit update rate
}

float readDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  float dist = duration * 0.034 / 2.0;
  return dist;
}

void sendDistanceAndLED() {
  Serial.print("D:");
  Serial.print(distance, 1);  // 1 decimal place
  Serial.print(",L:");
  Serial.println(ledState ? 1 : 0);
}

void checkSerialCommand() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c == 'H') {
      ledState = true;
      digitalWrite(ledPin, HIGH);
    } else if (c == 'L') {
      ledState = false;
      digitalWrite(ledPin, LOW);
    }
  }
}
