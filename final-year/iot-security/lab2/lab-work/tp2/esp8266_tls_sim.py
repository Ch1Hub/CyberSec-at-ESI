#!/usr/bin/env python3
"""Simulateur d'ESP8266 — TP2 : client MQTT en TLS (port 8883).

Équivalent Python du sketch WiFiClientSecure + BearSSL::X509List(ca.crt) :
le client vérifie le certificat du broker avec la CA du laboratoire.
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
CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "esp01")
TOPIC = os.getenv("MQTT_TOPIC", "capteurs/esp01/temp")
INTERVAL = float(os.getenv("PUB_INTERVAL", "5"))
COUNT = int(os.getenv("PUB_COUNT", "0"))

connected = threading.Event()


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"CONNACK: {reason_code}", flush=True)
    print(f"TLS: {client.socket().version()} - broker certificate verified with {MQTT_CA}", flush=True)
    connected.set()

def main() -> None:
    print(f"Wi-Fi: connected to {SSID} (simulated)", flush=True)
    print("Clock: synchronized (host NTP simulation)", flush=True)
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    # BearSSL (ESP8266) plafonne à TLS 1.2 : on reproduit ce comportement.
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = True
    ctx.verify_mode = ssl.CERT_REQUIRED
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.maximum_version = ssl.TLSVersion.TLSv1_2
    ctx.load_verify_locations(cafile=MQTT_CA)
    client.tls_set_context(ctx)
    client.tls_insecure_set(False)  # équivalent de setTrustAnchors : vérification stricte
    client.on_connect = on_connect
    try:
        client.connect(BROKER, PORT, keepalive=30)
    except ssl.SSLCertVerificationError as exc:
        print(f"TLS error: certificate verify failed - {exc.verify_message}", flush=True)
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
