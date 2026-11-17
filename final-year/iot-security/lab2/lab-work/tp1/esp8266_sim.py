#!/usr/bin/env python3
"""Simulateur d'ESP8266 — TP1 : client MQTT en clair (port 1883).

Reproduit le sketch Arduino du TP1 sans matériel radio :
  - Wi-Fi « IOT-LAB »
  - broker 127.0.0.1:1883
  - utilisateur esp01 / mot de passe esp01pass
  - publication de capteurs/esp01/temp toutes les 5 s
"""
import os
import threading
import time

import paho.mqtt.client as mqtt

SSID = os.getenv("WIFI_SSID", "IOT-LAB")
BROKER = os.getenv("MQTT_HOST", "127.0.0.1")
PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USER", "esp01")
MQTT_PASS = os.getenv("MQTT_PASS", "esp01pass")
CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "esp01")
TOPIC = os.getenv("MQTT_TOPIC", "capteurs/esp01/temp")
INTERVAL = float(os.getenv("PUB_INTERVAL", "5"))
COUNT = int(os.getenv("PUB_COUNT", "0"))

connected = threading.Event()


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"CONNACK: {reason_code}", flush=True)
    connected.set()

def on_disconnect(client, userdata, flags, reason_code, properties):
    print(f"connection lost ({reason_code}) - reconnecting", flush=True)


def main() -> None:
    print(f"Wi-Fi: connected to {SSID} (simulated)", flush=True)
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(BROKER, PORT, keepalive=30)
    client.loop_start()
    connected.wait(timeout=5)
    t0 = time.time()
    n = 0
    while True:
        # Télémesure simulée : 20.0 .. 25.0, valeur différente à chaque envoi
        temp = 20.0 + ((n * 0.7) % 5.0)
        payload = f"{temp:.1f}"
        client.publish(TOPIC, payload)
        print(f"PUBLISH {TOPIC} = {payload}", flush=True)
        n += 1
        time.sleep(INTERVAL)
        if COUNT and n >= COUNT:
            break


if __name__ == "__main__":
    main()
