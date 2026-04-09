// TP4 - Partie 1: ESP8266 comme serveur web (boutons ON/OFF LED)
#include <ESP8266WiFi.h>

#define LED_PIN 4  // GPIO4 (D2 sur NodeMCU)

const char *ssid = "LabNetwork";
const char *password = "REDACTED_WIFI_PASSWORD";
String deviceName = "ESP8266";

WiFiServer server(80);

void handleRequest(const String &request) {
  if (request.indexOf("/light1on") > 0) {
    digitalWrite(LED_PIN, LOW);   // LED active bas
  }
  if (request.indexOf("/light1off") > 0) {
    digitalWrite(LED_PIN, HIGH);
  }
}

void webpage(WiFiClient &client) {
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println("Connection: close");
  client.println();
  client.println("<!DOCTYPE HTML>");
  client.println("<html>");
  client.println("<head>");
  client.println("<meta name='apple-mobile-web-app-capable' content='yes' />");
  client.println("<meta name='apple-mobile-web-app-status-bar-style' content='black-translucent' />");
  client.println("</head>");
  client.println("<body bgcolor='#70706F'>");
  client.println("<hr/><hr>");
  client.println("<h1 style='color:#3AAA35; text-align:center;'>" + deviceName + " Device Control</h1>");
  client.println("<hr/><hr><br><br>");
  client.println("<center>Pin A0 <input value='" + String(analogRead(A0)) + "' readonly></center>");
  client.println("<br><center>");
  client.println("Built-in LED ");
  client.println("<a href='/light1on'><button>Turn On</button></a>");
  client.println("<a href='/light1off'><button>Turn Off</button></a><br/>");
  client.println("</center><br><br>");
  client.println("<center><table border='5'><tr><td>LED is</td>");
  if (digitalRead(LED_PIN)) {
    client.println("<td>OFF</td>");
  } else {
    client.println("<td>ON</td>");
  }
  client.println("</tr></table></center>");
  client.println("</body></html>");
  delay(1);
}

void setup() {
  Serial.begin(115200);
  Serial.println();
  Serial.println(F("Initialize System"));
  Serial.print(F("Connecting to "));
  Serial.println(ssid);

  pinMode(LED_PIN, OUTPUT);
  pinMode(A0, INPUT);
  digitalWrite(LED_PIN, HIGH);  // LED eteinte au demarrage

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(F("."));
  }

  server.begin();
  Serial.println();
  Serial.println(F("Web server initialized"));
  Serial.print(F("IP Address: "));
  Serial.println(WiFi.localIP());
}

void loop() {
  WiFiClient client = server.available();
  if (!client) {
    return;
  }

  while (!client.available()) {
    delay(1);
  }

  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();

  handleRequest(request);
  webpage(client);
}
