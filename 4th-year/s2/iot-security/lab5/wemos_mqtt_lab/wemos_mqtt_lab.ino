#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

const char* ssid = "LabNetwork";
const char* password = "REDACTED_WIFI_PASSWORD";
const char* mqtt_server = "broker.mqttdashboard.com";
const uint16_t mqtt_port = 1883;

const char* topic_cmd = "tpcysmqtt/test1";
const char* topic_temp = "tpcysmqtt/test2";
const char* topic_hum = "tpcysmqtt/test3";

#define DHTPIN D2
#define DHTTYPE DHT11
#define LED_ON LOW
#define LED_OFF HIGH
DHT dht(DHTPIN, DHTTYPE);

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMeasure = 0;

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.print("WiFi connected - ESP IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");

  String messageTemp;
  for (unsigned int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  if (String(topic) == topic_cmd) {
    Serial.print("Changing Room lamp to ");
    if (messageTemp == "true") {
      digitalWrite(LED_BUILTIN, LED_ON);
      Serial.print("On");
    } else if (messageTemp == "false") {
      digitalWrite(LED_BUILTIN, LED_OFF);
      Serial.print("Off");
    }
  }
  Serial.println();
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "wemosd1-" + String(ESP.getChipId(), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      client.subscribe(topic_cmd);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LED_OFF);
  dht.begin();
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMeasure > 1000) {
    lastMeasure = now;

    float h = dht.readHumidity();
    float t = dht.readTemperature();

    if (isnan(h) || isnan(t)) {
      Serial.println("Failed to read from DHT sensor");
      return;
    }

    char temperatureTemp[10];
    dtostrf(t, 6, 2, temperatureTemp);
    char humidityTemp[10];
    dtostrf(h, 6, 2, humidityTemp);

    client.publish(topic_temp, temperatureTemp, true);
    client.publish(topic_hum, humidityTemp, true);

    Serial.print("Humidity: ");
    Serial.print(h);
    Serial.print(" %\t Temperature: ");
    Serial.print(t);
    Serial.print(" *C");
    Serial.println();
  }
}
