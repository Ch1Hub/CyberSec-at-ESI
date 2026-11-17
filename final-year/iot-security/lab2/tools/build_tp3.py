"""TP3 report: mutual TLS with a client certificate."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from report import (figure, h1, new_document, note, page_break, para, question,
                    save, table, title_block)


def build() -> Path:
    doc = new_document("TP3 - Mutual TLS with a client certificate")

    title_block(
        doc,
        "IoT Security Lab - TP3",
        "Mutual TLS with a client certificate",
        "Authenticating the device, not only the broker",
        "Chihab",
        "17 November 2026",
    )

    h1(doc, "1", "Goal")
    para(doc, "In TP2 the device checked the broker with TLS, but the broker accepted any client that "
              "knew the password esp01pass. In this lab I add a client certificate: the device proves "
              "its identity with a certificate signed by the laboratory CA, and the broker refuses "
              "every client that does not present one. This is mutual TLS (mTLS).")

    table(doc,
          ["Item", "What I used"],
          [
              ["Broker", "Mosquitto 2 in Docker, port 8883 with TLS and require_certificate true"],
              ["Certificates", "ca.crt, broker.crt, esp01.crt (CN=esp01-client) and their keys"],
              ["Device", "esp8266_mtls_sim.py with the CA and the client certificate"],
              ["Login", "esp01 / esp01pass"],
              ["Capture", "Wireshark 4.6, filter tls"],
          ],
          widths=[3.5, 12.0])

    # ------------------------------------------------------------------ 2
    h1(doc, "2", "The client certificate")
    para(doc, "The CA is the same as in TP2. I create a second certificate for the device, signed by "
              "this CA, with CN=esp01-client. The broker will verify this certificate during the "
              "handshake.")
    figure(doc, "tp3_certs.png",
           "Figure 1 - The certificate of the device: CN=esp01-client, issuer CA-Lab, valid.")

    # ------------------------------------------------------------------ 3
    h1(doc, "3", "Broker requiring a certificate")
    para(doc, "One line changes compared to TP2: require_certificate true. The broker still has the CA "
              "certificate, because it needs it to verify the certificate sent by the device.")
    figure(doc, "tp3_config.png",
           "Figure 2 - mosquitto.conf: require_certificate true on the 8883 listener.")
    figure(doc, "tp3_broker.png",
           "Figure 3 - The broker starts with the client certificate check enabled.")

    # ------------------------------------------------------------------ 4
    h1(doc, "4", "The device connects with its certificate")
    para(doc, "On the device side I load the CA certificate and the pair esp01.crt / esp01.key. On a real "
              "ESP8266 this is WiFiClientSecure with setTrustAnchors() and setClientRSACert(). The rest "
              "of the code does not change: same broker, same port, same login, same topic.")
    figure(doc, "tp3_sim.png",
           "Figure 4 - The device authenticates the broker and is authenticated with its certificate.")

    para(doc, "A second client with the same certificate pair also connects, so the configuration works "
              "for any client that owns a valid certificate.")
    figure(doc, "tp3_sub.png",
           "Figure 5 - A subscriber with --cert and --key receives the measurements on port 8883.")

    # ------------------------------------------------------------------ 5
    h1(doc, "5", "Refusal without a certificate")
    para(doc, "If I run the same script without the client certificate, the broker stops the handshake "
              "with a fatal alert. The connection is closed before the MQTT CONNECT packet, so the "
              "device cannot send the password or any measurement.")
    figure(doc, "tp3_nocert.png",
           "Figure 6 - Without the client certificate: TLS error, handshake failure.")

    # ------------------------------------------------------------------ 6
    h1(doc, "6", "What Wireshark shows")
    para(doc, "The TLS filter shows one session. Compared to TP2 there is a new message in the server "
              "flight: Certificate Request.")
    figure(doc, "tp3_ws_list.png",
           "Figure 7 - The handshake contains Certificate Request, then the client Certificate.")

    para(doc, "In frame 10 the client sends its own certificate. Wireshark displays the subject, the "
              "issuer and the signature algorithm, like it did for the broker certificate in TP2.")
    figure(doc, "tp3_ws_clientcert.png",
           "Figure 8 - The client certificate in the handshake: subject CN=esp01-client, issuer CA-Lab.")

    para(doc, "The second capture is the session without a client certificate. The client answers the "
              "Certificate Request with an empty Certificate message, and the broker sends an alert.")
    figure(doc, "tp3_ws_alert.png",
           "Figure 9 - The broker refuses the session: Alert (Fatal, Handshake Failure).")

    note(doc, "Check:",
         "in the refused capture there is no MQTT packet at all. The filter mqtt returns 0 packets in "
         "both captures: on port 8883, MQTT is always inside TLS.")

    # ------------------------------------------------------------------ 7
    h1(doc, "7", "Answers to the questions")

    question(doc, "Q1. What is the difference between TP2 and TP3?")
    para(doc, "In TP2 only the server has a certificate: the device verifies the broker. In TP3 both "
              "sides have one: the broker also asks the device for its certificate. TP2 protects "
              "against a fake broker, TP3 protects against a fake device.")

    question(doc, "Q2. Is the password esp01pass still useful with mTLS?")
    para(doc, "It is still sent inside TLS, but it is no longer the main protection. A client without a "
              "certificate is refused during the handshake, before the password. The certificate proves "
              "which device is connecting; the password only adds a second check. In a real deployment "
              "the password could even be removed with use_identity_as_username true.")

    question(doc, "Q3. What happens if somebody copies esp01.crt and esp01.key?")
    para(doc, "He can connect like the real device, because the broker recognises the certificate and "
              "not the physical board. This is why the private key must stay on the device, ideally in "
              "a secure element. If a device is lost, its certificate must be revoked, which requires "
              "a CRL or a shorter certificate lifetime.")

    question(doc, "Q4. Why does the broker send Certificate Request before Server Hello Done?")
    para(doc, "Because the client must know which certificate to send while the handshake is still "
              "running. The server sends its own certificate, then Certificate Request, and only after "
              "that the client sends its Certificate and Certificate Verify messages. If the client "
              "has nothing to send, it sends an empty Certificate message, and the broker closes the "
              "handshake with an alert (Figure 9).")

    question(doc, "Q5. Does mTLS replace TLS?")
    para(doc, "No, it is an option of TLS. The encryption, the cipher suite and the verification of the "
              "broker are exactly the same as in TP2. mTLS only adds the verification of the client. "
              "Without TLS there is no certificate at all, so mTLS cannot work on a plain port.")

    question(doc, "Q6. What is left to improve after TP3?")
    para(doc, "The certificate lifetime, the revocation list and the storage of the private key. Also "
              "the broker configuration: one certificate per device instead of a shared one, TLS 1.3, "
              "and an ACL so each device can only publish on its own topic.")

    # ------------------------------------------------------------------ 8
    page_break(doc)
    h1(doc, "8", "Conclusion")
    para(doc, "With mTLS the broker knows which device is connected, and a client without a valid "
              "certificate is rejected during the handshake. The capture confirms it: the certificate "
              "is exchanged in clear (it is public), the rest is encrypted, and a missing certificate "
              "ends with a fatal alert before any MQTT packet. TP1 showed the clear text problem, TP2 "
              "solved the confidentiality, and TP3 solves the identity of the device. The remaining "
              "work is the management of the certificates: creation, distribution, renewal and "
              "revocation.")

    h1(doc, "9", "Recap of the three labs")
    para(doc, "The three labs follow each other: each one closes the weakness that the previous one left "
              "open.")
    table(doc,
          ["Lab", "What is protected", "What an attacker can still do"],
          [
              ["TP1 - MQTT, port 1883", "Nothing: login, topics and values in clear text",
               "Read the password and the measurements, publish fake data"],
              ["TP2 - TLS, port 8883", "Traffic encrypted, broker verified by the device",
               "Replay the password from any other client"],
              ["TP3 - mTLS, port 8883", "Traffic encrypted, broker and device both verified",
               "Connect only if the private key of a device is stolen"],
          ],
          widths=[4.2, 6.0, 5.3])

    h1(doc, "10", "Files used")
    table(doc,
          ["File", "Content"],
          [
              ["certs/ca.crt, certs/ca.key", "Laboratory CA, used by both sides"],
              ["certs/broker.crt, certs/broker.key", "Broker certificate, CN=localhost with SAN"],
              ["certs/esp01.crt, certs/esp01.key", "Client certificate, CN=esp01-client"],
              ["config/mosquitto.conf", "Listener 8883 with require_certificate true"],
              ["esp8266_mtls_sim.py", "Device with the CA and its client certificate"],
              ["captures/tp3_mtls.pcapng", "Normal session: Certificate Request and client Certificate"],
              ["captures/tp3_mtls_refus.pcapng", "Session without client certificate: fatal alert"],
          ],
          widths=[6.4, 9.1])

    return save(doc, "TP3_mTLS_client_certificate.docx")


if __name__ == "__main__":
    print(build())
