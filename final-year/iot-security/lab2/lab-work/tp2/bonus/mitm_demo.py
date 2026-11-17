#!/usr/bin/env python3
"""Démo TP2 Q5 : ce que permet setInsecure() face à un broker usurpateur.

  mode "verifie"  : le client exige un certificat signé par la CA du labo
                    → refus du broker pirate (8884, CA-ROGUE).
  mode "insecure" : équivalent de wifi.setInsecure() sur ESP8266
                    → le client accepte n'importe quel certificat et parle au pirate.
"""
import os
import ssl
import sys
import time

import paho.mqtt.client as mqtt

HOST, PORT = "localhost", 8884
CA = "certs/ca.crt"  # CA légitime du laboratoire


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "verifie"
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"demo-{mode}")
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.maximum_version = ssl.TLSVersion.TLSv1_2
    if mode == "insecure":
        # wifi.setInsecure() : aucune vérification de l'identité du serveur
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        print("mode insecure : vérification du certificat DÉSACTIVÉE", flush=True)
    else:
        ctx.check_hostname = True
        ctx.verify_mode = ssl.CERT_REQUIRED
        ctx.load_verify_locations(cafile=CA)
        print(f"mode verifie : ancre de confiance = {CA}", flush=True)
    client.tls_set_context(ctx)
    try:
        client.connect(HOST, PORT, keepalive=10)
    except ssl.SSLError as exc:
        print(f"CONNEXION REFUSÉE : {exc}", flush=True)
        return 1
    client.loop_start()
    time.sleep(0.5)
    client.publish("capteurs/esp01/temp", "99")
    print("CONNEXION ACCEPTÉE : fausse mesure 99 publiée sur le broker usurpateur", flush=True)
    time.sleep(0.5)
    client.loop_stop()
    client.disconnect()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
