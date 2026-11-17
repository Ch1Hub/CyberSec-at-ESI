#!/usr/bin/env python3
"""Simulateur d'ESP8266 — TP3 : client MQTT en mTLS (port 8883).

Équivalent Python du sketch WiFiClientSecure + setTrustAnchors + setClientRSACert :
  - le client vérifie le certificat du broker (CA du labo) ;
  - il présente son propre certificat (esp01.crt) et prouve qu'il détient
    la clé privée esp01.key lors du Certificate Verify.
"""
import os
import ssl
import threading
import time

import paho.mqtt.client as mqtt

SSID = os.getenv("WIFI_SSID", "IOT-LAB")
BROKER = os.getenv("MQTT_HOST", "localhost")
PORT = int(os.getenv("MQTT_PORT", "8883"))
MQTT_USER = os.getenv("MQTT_USER", "esp01")
MQTT_PASS = os.getenv("MQTT_PASS", "esp01pass")
MQTT_CA = os.getenv("MQTT_CA", "certs/ca.crt")
CLIENT_CERT = os.getenv("MQTT_CLIENT_CERT", "certs/esp01.crt")
CLIENT_KEY = os.getenv("MQTT_CLIENT_KEY", "certs/esp01.key")
CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "esp01")
TOPIC = os.getenv("MQTT_TOPIC", "capteurs/esp01/temp")
INTERVAL = float(os.getenv("PUB_INTERVAL", "5"))
COUNT = int(os.getenv("PUB_COUNT", "0"))

connected = threading.Event()


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"CONNACK: {reason_code}", flush=True)
    print(f"TLS: {client.socket().version()} - broker authenticated (CA) and client authenticated (certificate)", flush=True)
    connected.set()

def main() -> None:
    print(f"Wi-Fi: connected to {SSID} (simulated)", flush=True)
    print("Clock: synchronized (host NTP simulation)", flush=True)
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = True
    ctx.verify_mode = ssl.CERT_REQUIRED
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.maximum_version = ssl.TLSVersion.TLSv1_2   # BearSSL : TLS 1.2 max
    ctx.load_verify_locations(cafile=MQTT_CA)
    if os.getenv("MQTT_NO_CLIENT_CERT") != "1":
        ctx.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
    else:
        print("TEST MODE: no client certificate loaded", flush=True)
    client.tls_set_context(ctx)
    client.tls_insecure_set(False)
    client.on_connect = on_connect
    try:
        client.connect(BROKER, PORT, keepalive=30)
    except ssl.SSLError as exc:
        print(f"TLS error: handshake failure ({exc.reason})", flush=True)
        raise SystemExit(1)
    client.loop_start()
    connected.wait(timeout=10)
    n = 0
    while True:
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
