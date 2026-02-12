void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  Serial.println("Hello World! System Initialized.");
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on
  Serial.println("LED is ON");
  delay(1000);                       // wait for a second
  
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off
  Serial.println("LED is OFF");
  delay(1000);                       // wait for a second
}
