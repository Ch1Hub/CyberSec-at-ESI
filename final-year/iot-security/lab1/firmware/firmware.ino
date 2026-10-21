
const char WIFI_SSID[]      = "Chihab's Iphone";
const char WIFI_PASSWORD[]  = "123456789";
const char API_KEY[]        = "something";
const char ADMIN_PASSWORD[] = "admin123";

unsigned int checksum(const char *s) {
  unsigned int h = 0;
  while (*s) h = h * 31 + *s++;
  return h;
}

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.println("TP Firmware UART - version C");
  Serial.print("SSID: ");
  Serial.println(WIFI_SSID);

  Serial.print("Checksums: ");
  Serial.print(checksum(WIFI_PASSWORD), HEX);
  Serial.print(' ');
  Serial.print(checksum(API_KEY), HEX);
  Serial.print(' ');
  Serial.println(checksum(ADMIN_PASSWORD), HEX);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
}
