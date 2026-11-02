#define IR_PIN D1
#define RELAY_PIN D2
#define BUZZER_PIN D3

unsigned long lastPersonDetectedTime = 0;
const unsigned long COOLDOWN_MS = 5000;

void setup() {
  Serial.begin(9600);
  pinMode(IR_PIN, INPUT);
  
  // Relay is active LOW, so default HIGH = locked
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH);
  
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);
  
  delay(1000); // Wait for serial to initialize
}

void loop() {
  unsigned long currentMillis = millis();
  
  // Read IR sensor
  int irState = digitalRead(IR_PIN);
  
  // If IR detects person (HIGH) and cooldown has passed
  if (irState == HIGH && (currentMillis - lastPersonDetectedTime >= COOLDOWN_MS)) {
    lastPersonDetectedTime = currentMillis;
    Serial.println("PERSON_DETECTED");
  }
  
  // Read from Serial
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim(); // Remove any \r or whitespace
    
    if (command == "UNLOCK") {
      // Unlock door
      digitalWrite(RELAY_PIN, LOW); // energize relay (active LOW)
      delay(5000); // 5 seconds
      digitalWrite(RELAY_PIN, HIGH); // de-energize relay
      
      // 2 short beeps
      digitalWrite(BUZZER_PIN, HIGH);
      delay(100);
      digitalWrite(BUZZER_PIN, LOW);
      delay(100);
      digitalWrite(BUZZER_PIN, HIGH);
      delay(100);
      digitalWrite(BUZZER_PIN, LOW);
    } 
    else if (command == "LOCK") {
      // Ensure it stays locked
      digitalWrite(RELAY_PIN, HIGH);
      
      // 1 long beep
      digitalWrite(BUZZER_PIN, HIGH);
      delay(800);
      digitalWrite(BUZZER_PIN, LOW);
    }
  }
}
