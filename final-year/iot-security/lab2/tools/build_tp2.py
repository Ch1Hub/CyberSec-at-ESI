"""TP2 report: TLS with a server certificate."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from report import (figure, h1, new_document, note, para, question, save,
                    table, title_block)


def build() -> Path:
    doc = new_document("TP2 - TLS with a server certificate")

    title_block(
        doc,
        "IoT Security Lab - TP2",
        "TLS with a server certificate",
        "Encrypting the MQTT session on port 8883",
        "Chihab",
        "17 November 2026",
    )

    h1(doc, "1", "Goal")
    para(doc, "In TP1 the login and the measurements were readable in Wireshark. In this lab I add TLS to "
              "the broker: it receives a certificate signed by a small laboratory CA, and the device checks "
              "this certificate before it sends anything. I capture the traffic again and check that the "
              "MQTT content is not readable anymore.")

    table(doc,
          ["Item", "What I used"],
          [
              ["Broker", "Mosquitto 2 in Docker, port 8883 with TLS (port 1883 still open for comparison)"],
              ["Certificates", "ca.crt / ca.key, broker.crt / broker.key (RSA 2048)"],
              ["Device", "esp8266_tls_sim.py with paho-mqtt and the CA certificate"],
              ["Login", "esp01 / esp01pass"],
              ["Capture", "Wireshark 4.6, filter tls"],
          ],
          widths=[3.5, 12.0])

    # ------------------------------------------------------------------ 2
    h1(doc, "2", "The certificates")
    para(doc, "I create one CA for the lab, then a certificate for the broker. The broker certificate "
              "contains CN=localhost and a subjectAltName with DNS:localhost and IP:127.0.0.1, so it is "
              "valid for the address used by the device.")
    figure(doc, "tp2_certs.png",
           "Figure 1 - The certificates, the verification of the chain and the subjectAltName.")

    note(doc, "Important:",
         "the subjectAltName must contain the name or the IP address that the client uses. A certificate "
         "with only CN=localhost is rejected when the client connects to 127.0.0.1.")

    # ------------------------------------------------------------------ 3
    h1(doc, "3", "Broker with TLS")
    para(doc, "The broker keeps the plain listener on 1883 (to compare with TP1) and opens a second "
              "listener on 8883 with the CA, the certificate and the private key.")
    figure(doc, "tp2_config.png",
           "Figure 2 - mosquitto.conf: the 8883 listener uses the CA and the broker certificate.")
    figure(doc, "tp2_broker.png",
           "Figure 3 - The broker opens port 1883 and port 8883.")

    # ------------------------------------------------------------------ 4
    h1(doc, "4", "The device connects with TLS")
    para(doc, "On the device side only two things change: the client connects to port 8883, and it loads "
              "certs/ca.crt as its trust anchor. On a real ESP8266 this is WiFiClientSecure with "
              "setTrustAnchors() instead of WiFiClient. The connect and publish calls do not change.")
    figure(doc, "tp2_sim.png",
           "Figure 4 - The device negotiates TLS 1.2, verifies the broker certificate, then publishes.")

    para(doc, "A second client with the same CA also works, which shows that the configuration is not "
              "specific to the device script.")
    figure(doc, "tp2_sub.png",
           "Figure 5 - A subscriber with --cafile receives the measurements over TLS.")

    # ------------------------------------------------------------------ 5
    h1(doc, "5", "When the CA is wrong")
    para(doc, "If I run the same script with the system CA bundle instead of the lab CA, the certificate "
              "cannot be verified and the connection stops before any MQTT packet is sent.")
    figure(doc, "tp2_noca.png",
           "Figure 6 - Without the right CA, the device refuses the connection.")

    note(doc, "Result:",
         "TLS does not only encrypt, it also checks the identity of the broker. With the wrong CA there is "
         "no session at all, so no password and no measurement are sent.")

    # ------------------------------------------------------------------ 6
    h1(doc, "6", "What Wireshark shows")
    para(doc, "The capture contains one TLS session. The filter tls shows the handshake first, then only "
              "Application Data packets.")
    figure(doc, "tp2_ws_list.png",
           "Figure 7 - One TLS session: Client Hello, Server Hello with Certificate, then Application Data.")

    para(doc, "The Server Hello gives the version and the cipher suite used for the session.")
    figure(doc, "tp2_ws_serverhello.png",
           "Figure 8 - Server Hello: TLS 1.2 and cipher suite TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384.",
           width=14.6)

    para(doc, "The Certificate message can also be read, and this is normal: a certificate is public. "
              "Wireshark shows the issuer (CA-Lab), the subject (localhost) and the validity dates.")
    figure(doc, "tp2_ws_cert.png",
           "Figure 9 - The broker certificate inside the handshake: issuer CA-Lab, subject CN=localhost.")

    para(doc, "The MQTT messages are now inside the encrypted part. Wireshark knows the protocol used on "
              "port 8883, but it can only print Encrypted Application Data.")
    figure(doc, "tp2_ws_appdata.png",
           "Figure 10 - The application data is encrypted: the topic and the values are not readable.",
           width=14.6)

    note(doc, "Check:",
         "if I apply the filter mqtt on this same capture file, Wireshark displays 0 packets. The login, "
         "the topic capteurs/esp01/temp and the temperatures have disappeared from the analysis. On the "
         "wire there is only TLS, and the password is inside the tunnel.")

    # ------------------------------------------------------------------ 7
    h1(doc, "7", "Answers to the questions")

    question(doc, "Q1. What does the device check when it receives the broker certificate?")
    para(doc, "Three things. First, the signature: the certificate must be signed by a CA that is in the "
              "device trust store, here certs/ca.crt. Second, the name: the address used by the client must "
              "appear in the subjectAltName. Third, the dates: the certificate must be valid at the current "
              "time. If one check fails, the handshake stops, like in Figure 6.")

    question(doc, "Q2. The Client Hello shows SNI=localhost. Is that a problem?")
    para(doc, "No. The server name is sent in clear at the beginning, because the broker needs it to choose "
              "the certificate. It only says which host the client wants. The password, the topics and the "
              "values are sent later, inside the encrypted channel.")

    question(doc, "Q3. Is the password still transmitted? Is it still a problem?")
    para(doc, "Yes, the CONNECT packet still contains esp01 and esp01pass, because MQTT keeps the same "
              "authentication. But the packet is now encrypted: in Figure 10 Wireshark shows only encrypted "
              "application data, and an attacker who captures the traffic cannot read it. The password is "
              "protected in transit; it is still a shared secret, so it must stay secret on the device.")

    question(doc, "Q4. What happens if the device does not verify the certificate (setInsecure)?")
    para(doc, "Any certificate is accepted, so an attacker can put his own broker in the middle with a "
              "self-signed certificate. The device then speaks TLS with the attacker and sends the password "
              "and the data to him. Encryption without verification protects against a passive listener, "
              "not against a man in the middle. This is why the CA must be loaded on the device.")

    question(doc, "Q5. What is still missing after TP2?")
    para(doc, "TLS authenticates the broker, not the device. Any client that knows esp01/esp01pass can "
              "connect and publish, exactly like the injection in TP1. To authenticate the device itself, "
              "the broker must ask for a client certificate: this is mutual TLS, the subject of TP3.")

    # ------------------------------------------------------------------ 8
    h1(doc, "8", "Conclusion")
    para(doc, "With a certificate signed by the lab CA, the MQTT session becomes confidential: Wireshark "
              "still sees the handshake and the certificate, but the login and the measurements are "
              "encrypted. The device also refuses a broker that it cannot verify, so a simple interception "
              "is not enough anymore. The weak point left is the client: the password can still be replayed "
              "by anyone who knows it. TP3 replaces this shared secret with a client certificate.")

    h1(doc, "9", "Files used")
    table(doc,
          ["File", "Content"],
          [
              ["certs/ca.crt, certs/ca.key", "Laboratory CA"],
              ["certs/broker.crt, certs/broker.key", "Broker certificate, CN=localhost with SAN"],
              ["config/mosquitto.conf", "Listener 8883 with cafile, certfile and keyfile"],
              ["esp8266_tls_sim.py", "Device with a TLS context and the CA as trust anchor"],
              ["captures/tp2_tls.pcapng", "TLS session: handshake and encrypted application data"],
          ],
          widths=[6.4, 9.1])

    return save(doc, "TP2_TLS_server_certificate.docx")


if __name__ == "__main__":
    print(build())
