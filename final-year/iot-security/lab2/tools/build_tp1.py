"""TP1 report: MQTT without TLS."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from report import (figure, h1, new_document, note, para, question, save,
                    table, title_block)


def build() -> Path:
    doc = new_document("TP1 - MQTT without TLS")

    title_block(
        doc,
        "IoT Security Lab - TP1",
        "MQTT without TLS",
        "Capturing the traffic of a connected object with Wireshark",
        "Chihab",
        "17 November 2026",
    )

    h1(doc, "1", "Goal and setup")
    para(doc, "In this lab I connect a small IoT device to a Mosquitto broker over MQTT on port 1883, "
              "without TLS. I capture the traffic with Wireshark and look at what an attacker on the "
              "same network can read. At the end I use the captured login to publish a fake value.")

    para(doc, "The lab sheet asks for a real ESP8266 board. I did not have one, so I used a small Python "
              "script (esp8266_sim.py) that makes the same MQTT calls: connect with a username and a "
              "password, then publish a temperature every second. The broker runs in a Docker container "
              "on 127.0.0.1, so nothing leaves the machine.")

    table(doc,
          ["Item", "What I used"],
          [
              ["Broker", "Mosquitto 2 in Docker, listener 127.0.0.1:1883"],
              ["Device", "esp8266_sim.py with paho-mqtt (no radio, simulated board)"],
              ["Login", "esp01 / esp01pass"],
              ["Topic", "capteurs/esp01/temp"],
              ["Capture", "Wireshark 4.6, display filter mqtt"],
          ],
          widths=[3.5, 12.0])

    # ------------------------------------------------------------------ 2
    h1(doc, "2", "Starting the broker")
    para(doc, "The broker is started with a very small configuration file: it listens on port 1883, it "
              "refuses clients without a login, and it has no TLS at all.")
    figure(doc, "tp1_broker.png",
           "Figure 1 - The broker container starts and listens on 127.0.0.1:1883.")
    figure(doc, "tp1_config.png",
           "Figure 2 - mosquitto.conf: password file required, no TLS.")

    # ------------------------------------------------------------------ 3
    h1(doc, "3", "The device publishes its data")
    para(doc, "The script connects with the login esp01 / esp01pass and publishes a value on the topic "
              "capteurs/esp01/temp every second. I only shortened the interval to one second so the "
              "capture stays readable.")
    figure(doc, "tp1_sim.png",
           "Figure 3 - The simulated device connects (CONNACK 0) and publishes a value every second.")

    para(doc, "To check that the chain works, a second client subscribes to capteurs/# and prints what it "
              "receives.")
    figure(doc, "tp1_sub.png",
           "Figure 4 - A subscriber receives the same values (20.7, 21.4, 22.1, 22.8).")

    # ------------------------------------------------------------------ 4
    h1(doc, "4", "What Wireshark shows")
    para(doc, "The capture file tp1_plaintext.pcapng contains the whole session. With the filter mqtt, "
              "Wireshark shows two CONNECT packets and then only PUBLISH packets.")
    figure(doc, "tp1_ws_list.png",
           "Figure 5 - All MQTT packets of the capture: CONNECT, CONNACK, SUBSCRIBE and PUBLISH.",
           width=14.6)

    para(doc, "Then I filter on mqtt && mqtt.msgtype == 1 to keep only the CONNECT packets, and I open the "
              "MQTT tree of the first one.")
    figure(doc, "tp1_ws_connect.png",
           "Figure 6 - The CONNECT packet in Wireshark: User Name: esp01 and Password: esp01pass.")

    note(doc, "Observation:",
         "the login is not hidden. Wireshark reads it directly in the MQTT fields, and the same bytes are "
         "visible in the hex pane. MQTT 3.1.1 sends the password as plain text: it is not hashed and not "
         "encrypted. Anyone who can capture the Wi-Fi or the network reads it in one click.")

    # ------------------------------------------------------------------ 5
    h1(doc, "5", "Publishing a fake value")
    para(doc, "With the login found in the capture, I connect a normal MQTT client and publish 99 on the "
              "same topic. The broker accepts the message without any error, and the subscriber receives "
              "it like a real measurement.")
    figure(doc, "tp1_inject.png",
           "Figure 7 - A fake value (99) is published with the stolen login and received by the subscriber.")

    para(doc, "The same packet in Wireshark shows the topic and the two bytes 39 39, which are the ASCII "
              "characters for 99.")
    figure(doc, "tp1_ws_publish.png",
           "Figure 8 - The fake PUBLISH in Wireshark: topic capteurs/esp01/temp, message 39 39 (\"99\").")

    note(doc, "Result:",
         "the broker cannot see the difference between the device and the attacker. Both use the same "
         "username, the same password and the same topic. Authentication happened, but it proves nothing "
         "about who is really sending the value.")

    # ------------------------------------------------------------------ 6
    h1(doc, "6", "Answers to the questions")

    question(doc, "Q1. Where are the username and the password, and why can we read them?")
    para(doc, "They are in the CONNECT packet, in the MQTT payload. Wireshark shows them as User Name and "
              "Password fields. They are readable because port 1883 sends everything in clear text: there "
              "is no TLS layer to encrypt the bytes.")

    question(doc, "Q2. Is allow_anonymous false enough to protect the communication?")
    para(doc, "No. This option only refuses clients that do not send a login. It does not encrypt anything. "
              "If somebody reads the password once, he can log in like a normal client. Section 5 shows it: "
              "the fake value 99 was accepted.")

    question(doc, "Q3. What is the difference between authentication and encryption?")
    para(doc, "Authentication checks who you are: here the broker compares the username and the password "
              "with its password file. Encryption makes the content unreadable for someone who captures the "
              "traffic. In this lab authentication is present, but encryption is missing, so both the "
              "password and the measurements travel in clear text.")

    question(doc, "Q4. What would make the capture useless without changing the application code?")
    para(doc, "Put TLS on the broker: open port 8883 with a server certificate and give the CA certificate "
              "to the device. The connect and publish calls stay the same, only the transport changes. "
              "This is exactly what TP2 does.")

    # ------------------------------------------------------------------ 7
    h1(doc, "7", "Conclusion")
    para(doc, "MQTT without TLS gives no confidentiality and no integrity. A user name and a password are "
              "sent in clear text, so a single capture is enough to steal them, read the topics, read the "
              "measurements and publish false data. Login and password are useful, but they only say who "
              "should connect; they do not protect the connection. The next lab adds a server certificate "
              "with TLS, and TP3 adds a client certificate so the broker can also check the device.")

    # ------------------------------------------------------------------ 8
    h1(doc, "8", "Files used")
    para(doc, "All the manipulations were done on the loopback interface, with a capture filter on TCP port "
              "1883. The capture files were then opened in Wireshark for the analysis.")
    table(doc,
          ["File", "Content"],
          [
              ["config/mosquitto.conf", "Broker configuration, no TLS"],
              ["config/passwd", "Password file with the user esp01"],
              ["esp8266_sim.py", "Simulated device: CONNECT then PUBLISH every second"],
              ["captures/tp1_plaintext.pcapng", "Normal session: CONNECT, CONNACK, SUBSCRIBE and PUBLISH"],
              ["captures/tp1_injection.pcapng", "Session with the fake value 99"],
          ],
          widths=[6.0, 9.5])

    return save(doc, "TP1_MQTT_without_TLS.docx")


if __name__ == "__main__":
    print(build())
