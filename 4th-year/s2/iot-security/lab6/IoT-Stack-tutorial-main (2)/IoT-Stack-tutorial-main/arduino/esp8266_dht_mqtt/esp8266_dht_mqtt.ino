#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <DHT.h>
#include <PubSubClient.h>

// WiFi credentials
const char* ssid = "Chihab’s iPhone";
const char* password = "1234567890";

// MQTT settings
const char* mqtt_server = "10.66.139.11";
const int mqtt_port = 1883;
const char* mqtt_user = "";
const char* mqtt_password = "";

// MQTT topics
const char* topic_temp = "home/esp8266/temperature";
const char* topic_humidity = "home/esp8266/humidity";
const char* topic_status = "home/esp8266/status";
const char* topic_temp_lab = "sensor/temp";

// DHT setup
#define DHTPIN D4
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;
const unsigned long interval = 1000; // publish every 1 second

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect_mqtt() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");

    String clientId = "ESP8266Client-";
    clientId += String(ESP.getChipId(), HEX);

    bool connected;
    if (strlen(mqtt_user) > 0) {
      connected = client.connect(
        clientId.c_str(),
        mqtt_user,
        mqtt_password,
        topic_status,
        0,
        true,
        "offline"
      );
    } else {
      connected = client.connect(
        clientId.c_str(),
        topic_status,
        0,
        true,
        "offline"
      );
    }

    if (connected) {
      Serial.println("connected");
      client.publish(topic_status, "online", true);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" retrying in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  dht.begin();
  setup_wifi();

  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi disconnected, reconnecting...");
    setup_wifi();
  }

  if (!client.connected()) {
    reconnect_mqtt();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg >= interval) {
    lastMsg = now;

    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();

    if (isnan(humidity) || isnan(temperature)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }

    char tempString[8];
    char humString[8];

    dtostrf(temperature, 1, 2, tempString);
    dtostrf(humidity, 1, 2, humString);

    Serial.print("Publishing temperature: ");
    Serial.println(tempString);
    client.publish(topic_temp, tempString, true);
    client.publish(topic_temp_lab, tempString, true);

    Serial.print("Publishing humidity: ");
    Serial.println(humString);
    client.publish(topic_humidity, humString, true);
  }
}
