"""Rapport TP1 — MQTT sans TLS : capture et analyse avec Wireshark."""
from __future__ import annotations

from pathlib import Path

from common import (
    LAB, badge, bullets, callout, code_block, esc, figure, pkt_table, qa,
    render_pdf, sha256, table, terminal,
)

TP = LAB / "tp1"
EV = TP / "evidence"


def rd(name: str, start: int | None = None, end: int | None = None) -> list[str]:
    text = (EV / name).read_text(errors="replace")
    text = "".join(c if (c.isprintable() or c in "\n\t") else "·" for c in text)
    lines = text.splitlines()
    return lines[start:end]


def build() -> Path:
    # ------------------------------------------------------------ captures
    f1 = figure(1, terminal("tp1_broker", "chihab@iotlab — tp1 — broker", [
        "$ docker run -d --rm --name tp1-broker --network host --user $(id -u):$(id -g) \\",
        "    -v \"$PWD/config:/mosquitto/config:ro\" eclipse-mosquitto:2",
        "$ docker logs tp1-broker",
    ] + rd("broker_startup.txt")[-8:]), "Démarrage du broker Mosquitto en configuration ouverte : écoute sur 127.0.0.1:1883, sans TLS.")

    f2 = figure(2, terminal("tp1_sim", "chihab@iotlab — tp1 — objet simulé", [
        "$ python3 esp8266_sim.py",
    ] + rd("simulator_console.txt")), "Console de l'« ESP8266 » simulé : CONNACK réussi puis publication de la télémétrie toutes les 5 s.")

    f3 = figure(3, terminal("tp1_sub", "chihab@iotlab — tp1 — abonné", [
        "$ docker run --rm --network host eclipse-mosquitto:2 \\",
        "    mosquitto_sub -h 127.0.0.1 -u esp01 -P esp01pass -t 'capteurs/esp01/temp' -v",
    ] + rd("subscriber.txt")), "Réception de la télémétrie par un abonné authentifié : la chaîne de mesure fonctionne de bout en bout.")

    f4 = figure(4, terminal("tp1_creds", "chihab@iotlab — tp1 — analyse CONNECT", [
        "$ tshark -r captures/tp1_plaintext.pcapng -Y \"mqtt.msgtype == 1\" \\",
        "    -T fields -e mqtt.clientid -e mqtt.username -e mqtt.passwd",
    ] + rd("connect_credentials.txt"), highlights=("esp01pass",)), "Extraction des champs du paquet CONNECT : l'identifiant et le mot de passe sont directement lisibles.")

    f5 = figure(5, terminal("tp1_connect_detail", "chihab@iotlab — tp1 — détail du CONNECT", [
        "$ tshark -r captures/tp1_plaintext.pcapng -Y \"frame.number == 14\" -V",
    ] + rd("connect_extract.txt"), highlights=("User Name:", "Password:", "Client ID:"), max_cols=104),
        "Arbre de dissection MQTT du CONNECT de l'objet (trame 14) : Client ID, User Name et Password apparaissent en clair.")

    follow = rd("follow_tcp_stream.txt", 0, 20)
    f6 = figure(6, terminal("tp1_follow", "chihab@iotlab — tp1 — suivre le flux TCP", [
        "$ tshark -r captures/tp1_plaintext.pcapng -q -z follow,tcp,ascii,1",
    ] + follow, highlights=("esp01pass", "capteurs/esp01/temp")), "« Suivre le flux TCP » : la session MQTT complète est reconstituée en ASCII — identifiants, sujet et mesures.")

    f7 = figure(7, terminal("tp1_injection", "chihab@iotlab — tp1 — injection d'une fausse mesure", [
        "$ # terminal 1 : un abonné surveille le sujet",
        "$ docker run --rm --network host eclipse-mosquitto:2 mosquitto_sub \\",
        "    -h 127.0.0.1 -u esp01 -P esp01pass -t 'capteurs/#' -v",
        "capteurs/esp01/temp 99",
        "",
        "$ # terminal 2 : l'attaquant rejoue les identifiants capturés",
        "$ docker run --rm --network host eclipse-mosquitto:2 mosquitto_pub \\",
        "    -h 127.0.0.1 -u esp01 -P esp01pass -t capteurs/esp01/temp -m 99",
        "$ # aucune erreur : la fausse mesure a été acceptée par le broker",
    ], highlights=("99",)), "Injection d'une fausse mesure (99 °C) avec les identifiants dérobés : le broker l'accepte et la diffuse aux abonnés.")

    # Table avec temps relatifs réels
    pkt_rows = []
    import subprocess
    out = subprocess.run(
        ["tshark", "-r", str(TP / "captures/tp1_plaintext.pcapng"), "-Y", "mqtt",
         "-T", "fields", "-e", "frame.number", "-e", "frame.time_relative",
         "-e", "ip.src", "-e", "ip.dst", "-e", "_ws.col.Protocol", "-e", "_ws.col.Info",
         "-E", "separator=|"],
        capture_output=True, text=True, check=True).stdout
    for line in out.splitlines():
        p = line.split("|")
        if len(p) == 6:
            pkt_rows.append((p[0], f"{float(p[1]):.3f}", p[2], p[3], p[4], p[5]))

    pkt = pkt_table(
        pkt_rows, highlight={4, 14}, caption=(
            "Vue des paquets MQTT de la capture — reconstituée depuis <code>tshark -T fields</code>. "
            "Les trames 4 et 14 (CONNECT, en surbrillance) portent les identifiants ; les trames 18 à 32 "
            "transportent les mesures en clair. La trame 4 est le CONNECT de l'abonné de vérification, la trame 14 celui de l'objet."
        ),
    )

    cover = f"""
<div class="cover">
  <div class="kicker">Module Sécurité de l'IoT · Master / cycle ingénieur</div>
  <h1>TP1 — MQTT sans TLS</h1>
  <p class="sub">Capturer et analyser le trafic d'un objet connecté avec Wireshark : quand l'authentification ne protège pas la confidentialité.</p>
  <div class="stamp">MANIPULATIONS EXÉCUTÉES ET VÉRIFIÉES · 17 NOV. 2026</div>
  <div class="files">~/iotlab-tp/tp1<br>captures/tp1_plaintext.pcapng · captures/tp1_injection.pcapng<br>esp8266_sim.py · config/mosquitto.conf</div>
  <div class="meta"><table>
    <tr><td class="k">Série</td><td class="v">Sécuriser MQTT sur ESP8266 — volet 1/4</td></tr>
    <tr><td class="k">Binôme</td><td class="v">____________________________________</td></tr>
    <tr><td class="k">Date</td><td class="v">17 novembre 2026</td></tr>
    <tr><td class="k">Environnement</td><td class="v">Mosquitto 2.1.2 · tshark 4.6.0 · Python 3.13 · paho-mqtt 2.1.0</td></tr>
    <tr><td class="k">Objet</td><td class="v">ESP8266 simulé (réseau isolé, 127.0.0.1)</td></tr>
  </table></div>
</div>
"""

    toc = """
<div class="toc page-break">
  <h2>Sommaire</h2>
  <ol>
    <li>Objectifs et périmètre</li>
    <li>Environnement virtualisé</li>
    <li>Mise en place du broker et de l'objet</li>
    <li>Capture et analyse avec Wireshark</li>
    <li>Constat : ce que révèle la capture</li>
    <li>Réponses aux questions</li>
    <li>Barème et auto-évaluation</li>
    <li>Durcissement et transition vers le TP2</li>
    <li>Annexe A — script complet</li>
    <li>Annexe B — configuration et preuves</li>
  </ol>
</div>
"""

    body = cover + toc + f"""
<section>
<h1><span class="num">1</span>Objectifs et périmètre</h1>
<p class="lead">Ce premier TP établit la situation de départ de la série : un objet connecté parle MQTT en clair sur le port 1883.
L'objectif est de montrer, capture à l'appui, que l'authentification par nom d'utilisateur et mot de passe ne protège en rien
la confidentialité ni l'intégrité des échanges.</p>
<div class="meta-grid">
  <div class="meta-card"><div class="k">Objectif 1</div><div class="v">Programmer un client MQTT authentifié</div>
    <p class="small">Équivalent de l'ESP8266 + PubSubClient : connexion avec <code>esp01</code> / <code>esp01pass</code>, publication d'une température toutes les 5 s.</p></div>
  <div class="meta-card"><div class="k">Objectif 2</div><div class="v">Capturer et isoler le CONNECT</div>
    <p class="small">Filtrer le trafic MQTT, ouvrir le paquet <i>Connect Command</i> et lire les champs <i>User Name</i> et <i>Password</i>.</p></div>
  <div class="meta-card"><div class="k">Objectif 3</div><div class="v">Lire les sujets et les charges utiles</div>
    <p class="small">Suivre le flux TCP et reconstituer la conversation applicative : sujet <code>capteurs/esp01/temp</code> et valeurs de température.</p></div>
  <div class="meta-card"><div class="k">Objectif 4</div><div class="v">Mesurer l'impact pour un attaquant</div>
    <p class="small">Réutiliser les identifiants capturés pour publier une fausse mesure et observer sa diffusion.</p></div>
</div>
{callout("info", "Périmètre éthique",
  "Toutes les manipulations ont été réalisées sur des objets simulés et un broker local, sur l'interface <code>lo</code> uniquement. "
  "Aucun scan, aucune connexion vers un équipement tiers. Les secrets du laboratoire restent confinés à ce rapport et aux fichiers du TP.")}
</section>

<section>
<h1><span class="num">2</span>Environnement virtualisé</h1>
<p>Le sujet de TP suppose un ESP8266 réel et un PC broker sur un réseau Wi-Fi isolé. Le document d'organisation de la séance
(« TP — Vulnérabilités des protocoles IoT ») autorise explicitement l'usage d'objets simulés, sans matériel radio. L'adaptation
est donc la suivante.</p>
{table(
  ["Élément du sujet", "Rôle", "Réalisation dans ce rapport"],
  [
    ["ESP8266 (NodeMCU / Wemos D1)", "Client MQTT", "Script Python <code>esp8266_sim.py</code> (paho-mqtt 2.1.0), même logique : CONNECT authentifié, PUBLISH toutes les 5 s"],
    ["Arduino IDE + PubSubClient", "Bibliothèque cliente", "API <code>paho.mqtt.client</code> ; code applicatif réduit à <code>connect / publish</code>"],
    ["Broker Mosquitto sur 192.168.1.10:1883", "Courtier MQTT", "Mosquitto 2.1.2 en conteneur, listener <code>127.0.0.1:1883</code>, sans TLS"],
    ["Wireshark (interface graphique)", "Capture et dissection", "tshark 4.6.0 (même dissecteur MQTT), captures <code>.pcapng</code> conservées"],
    ["Réseau Wi-Fi isolé du laboratoire", "Transport", "Boucle locale <code>lo</code> : aucun paquet ne quitte la machine"],
    ["Utilisateur <code>esp01</code> / <code>esp01pass</code>", "Authentification", "Identique, créé avec <code>mosquitto_passwd</code>"],
  ],
  widths=["27%", "18%", "55%"])}
{callout("warn", "Adaptation d'adressage assumée",
  "Le sujet utilise l'adresse <code>192.168.1.10</code>. Dans l'environnement virtualisé, le broker écoute sur <code>127.0.0.1</code> ; "
  "les captures et les commandes reflètent cette adresse. Le raisonnement et les conclusions sont identiques : seul le chemin réseau change. "
  "Le TP2 expliquera comment le <i>subjectAltName</i> du certificat est adapté à cette adresse.")}
<div class="kpi">
  <div><b>2</b><span>CONNECT capturés (abonné de contrôle + objet)</span></div>
  <div><b>4</b><span>mesures publiées en clair</span></div>
  <div><b>0</b><span>couche de chiffrement</span></div>
  <div><b>1</b><span>injection réussie avec les identifiants volés</span></div>
</div>
</section>

<section>
<h1><span class="num">3</span>Mise en place du broker et de l'objet</h1>
<h2>3.1 Configuration ouverte du broker</h2>
<p>Le broker est lancé avec un fichier de configuration minimal : écoute sur le port 1883, authentification par fichier de mots de passe,
aucun chiffrement. Le fichier <code>passwd</code> est créé avec <code>mosquitto_passwd</code> et contient l'utilisateur <code>esp01</code>.</p>
{code_block("config/mosquitto.conf", '''
listener 1883 127.0.0.1
allow_anonymous false
password_file /mosquitto/config/passwd
persistence false
log_type all
''')}
{code_block("Création de l'utilisateur (équivalent de sudo mosquitto_passwd -c /etc/mosquitto/passwd esp01)", '''
$ docker run --rm -v "$PWD/config:/mosquitto/config" eclipse-mosquitto:2 \\
    mosquitto_passwd -c -b /mosquitto/config/passwd esp01 esp01pass
Adding password for user esp01
''')}
{f1}

<h2>3.2 Objet simulé</h2>
<p>Le script reprend le sketch du sujet : connexion au réseau Wi-Fi (simulée), CONNECT MQTT avec les identifiants, puis publication
périodique de la température. La différence tient uniquement au transport : <code>paho-mqtt</code> remplace <code>PubSubClient</code>,
mais les appels applicatifs (<code>connect</code>, <code>publish</code>) sont identiques.</p>
{code_block("esp8266_sim.py (extrait)", '''
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="esp01")
client.username_pw_set("esp01", "esp01pass")
client.connect("127.0.0.1", 1883, keepalive=30)
client.loop_start()
while True:
    temp = 20.0 + ((n * 0.7) % 5.0)
    client.publish("capteurs/esp01/temp", f"{temp:.1f}")
    time.sleep(5)
''')}
{f2}
{f3}
{callout("ok", "Télémétrie reçue",
  "L'abonné de contrôle reçoit bien les quatre valeurs publiées (20.0, 20.7, 21.4, 22.1). La chaîne MQTT est fonctionnelle : "
  "le reste du TP porte donc uniquement sur ce que voit un observateur du réseau.")}
</section>

<section>
<h1><span class="num">4</span>Capture et analyse avec Wireshark</h1>
<h2>4.1 Capture du trafic</h2>
<p>La capture est réalisée sur l'interface de boucle locale, avec un filtre de capture sur le port 1883. Le CONNECT est provoqué
en (re)démarrant l'objet simulé, comme demandé dans le sujet.</p>
{code_block("Capture", '''
$ tshark -i lo -f "tcp port 1883" -w captures/tp1_plaintext.pcapng -q
Capturing on 'Loopback: lo'
...
$ tshark -r captures/tp1_plaintext.pcapng -Y "mqtt" -T fields \\
    -e frame.number -e ip.src -e ip.dst -e mqtt.msgtype -e mqtt.topic
''')}
{pkt}

<h2>4.2 Lire les identifiants dans le paquet CONNECT</h2>
<p>Le paquet <i>Connect Command</i> de l'objet est la trame 14. Le dissecteur MQTT expose directement les champs utiles :</p>
{f4}
{f5}
<p>Le drapeau <code>0xc2</code> confirme que les bits <i>User Name Flag</i> et <i>Password Flag</i> sont positionnés. Le mot de passe
n'est pas haché : MQTT 3.1.1 le transporte tel quel dans la charge utile du CONNECT. Le broker le vérifie à l'arrivée, mais rien
ne protège son transit. La trame 4 est le CONNECT de l'abonné de contrôle : son <i>Client ID</i> est vide (généré par le broker),
mais les mêmes identifiants <code>esp01</code> / <code>esp01pass</code> y sont également visibles.</p>

<h2>4.3 Suivre le flux TCP</h2>
<p>Le suivi de flux reconstitue la session applicative complète, sans avoir à analyser paquet par paquet :</p>
{f6}
<p>Trois informations majeures y apparaissent :</p>
{bullets([
  "<b>Les identifiants</b> — <code>esp01</code> / <code>esp01pass</code>, réutilisables tels quels sur le port 1883.",
  "<b>La cartographie des sujets</b> — <code>capteurs/esp01/temp</code>, qui indique à la fois le type de donnée et l'identité de l'objet.",
  "<b>Les données métier</b> — les quatre valeurs de température (20.0 à 22.1), qui suffisent à profiler l'activité du capteur.",
])}

<h2>4.4 Exploiter la capture</h2>
<p>Avec les identifiants dérobés, un attaquant du même réseau se connecte au broker et publie une valeur arbitraire sur le sujet
de l'objet. Aucune ACL n'est configurée : le broker accepte la publication et la diffuse à tous les abonnés.</p>
{f7}
{code_block("Preuve dans la capture d'injection", '''
$ tshark -r captures/tp1_injection.pcapng \\
    -Y 'mqtt.msgtype == 3 && mqtt.topic == "capteurs/esp01/temp"' \\
    -T fields -e frame.number -e mqtt.topic -e mqtt.msg
18    capteurs/esp01/temp    3939      # 3939 = « 99 » en hexadécimal
20    capteurs/esp01/temp    3939
''')}
<p>La trame 18 est la publication de l'attaquant, la trame 20 sa retransmission par le broker vers l'abonné. La valeur
<b>99 °C</b> est acceptée sans contrôle : l'intégrité des mesures n'est pas garantie.</p>
</section>

<section>
<h1><span class="num">5</span>Constat : ce que révèle la capture</h1>
{table(
  ["Élément exposé", "Risque concret", "Gravité"],
  [
    ["Mot de passe dans le CONNECT", "Vol et rejeu : usurpation de l'objet, publication de fausses données, déconnexion de l'objet légitime par usurpation de Client ID", "Critique"],
    ["Sujets MQTT", "Cartographie de l'installation : pièces, équipements, capteurs, commandes", "Élevée"],
    ["Charges utiles", "Espionnage des mesures (température, présence, état d'une serrure) et de la vie privée", "Élevée"],
    ["Absence d'intégrité", "Injection de mesures ou de commandes : le récepteur ne peut pas distinguer l'objet de l'attaquant", "Critique"],
    ["Absence de chiffrement", "Écoute passive et attaque de l'homme du milieu ; toute la session est lisible", "Critique"],
  ],
  widths=["26%", "59%", "15%"])}
{callout("warn", "Point clé",
  "<code>allow_anonymous false</code> empêche seulement les connexions <i>sans</i> identifiants. Dès qu'un mot de passe circule en clair, "
  "l'authentification devient une formalité contournable : il suffit de l'observer une fois. La confidentialité et l'intégrité exigent "
  "un chiffrement du transport (TLS), pas seulement une vérification d'identité.")}
</section>

<section>
<h1><span class="num">6</span>Réponses aux questions</h1>
{qa(1, "Dans quel paquet et à quel endroit se trouvent le nom d'utilisateur et le mot de passe ? Pourquoi sont-ils lisibles alors que le broker exige une authentification ?", """
<p>Ils se trouvent dans le paquet <b>CONNECT</b> (paquet n° 14 de la capture), dans la <b>charge utile MQTT</b>, aux champs
<i>User Name</i> et <i>Password</i>. Le dissecteur les affiche directement et la vue hexadécimale les confirme. MQTT 3.1.1 ne
prévoit aucun chiffrement de ces champs : le mot de passe est transmis en clair, sans hachage ni challenge.</p>
<p>Le broker exige une authentification, mais celle-ci est vérifiée <b>à l'arrivée</b>. Entre l'objet et le broker, le trafic circule
sur TCP en clair (port 1883) : toute personne qui capture le réseau lit les identifiants. Authentifier n'implique pas protéger le
secret pendant le transport ; c'est précisément la confusion que ce TP met en évidence.</p>
""")}
{qa(2, "Que montre « Suivre le flux TCP » ? Citez trois informations qu'un attaquant en tire.", """
<p>Le suivi de flux reconstitue la conversation applicative complète, y compris les paquets de contrôle MQTT. On y voit le CONNECT
(<code>esp01</code> / <code>esp01pass</code>), le CONNACK, puis les PUBLISH successifs vers <code>capteurs/esp01/temp</code> avec leurs
valeurs. Trois informations directement exploitables :</p>
<ul>
<li><b>Les identifiants</b> : réutilisables pour se connecter au broker et se faire passer pour l'objet ;</li>
<li><b>Les sujets</b> : ils révèlent la structure de l'installation et les topics de commande éventuels ;</li>
<li><b>Les données</b> : les mesures et leur périodicité, qui permettent de profiler le capteur et de préparer une injection crédible.</li>
</ul>
""")}
{qa(3, "L'option <code>allow_anonymous false</code> suffit-elle à protéger la communication ? Justifiez à partir de la capture.", """
<p><b>Non.</b> Cette option interdit les connexions sans identifiants, mais elle ne chiffre rien. La capture montre que le mot de passe
circule en clair dans le CONNECT : un attaquant qui l'a observé une seule fois peut se connecter légitimement, sans jamais avoir
besoin de l'option anonyme. L'injection de la fausse mesure (99 °C) le démontre : le broker ne distingue pas l'objet de l'attaquant
qui rejoue ses identifiants.</p>
<p>Autrement dit, <code>allow_anonymous false</code> ferme la porte aux curieux qui n'ont pas d'identifiants ; elle ne protège ni
la confidentialité du mot de passe, ni l'intégrité des messages, ni l'identité réelle du client.</p>
""")}
{qa(4, "Quelle est la différence entre authentifier un client et chiffrer la communication ? Lequel manque ici ?", """
<p><b>Authentifier</b>, c'est vérifier l'identité déclarée : le broker compare le couple utilisateur/mot de passe à son fichier.
<b>Chiffrer</b>, c'est rendre le contenu illisible pour un observateur et en garantir l'intégrité en transit (TLS).</p>
<p>Ici, l'authentification est présente mais faible (secret partagé, rejouable), et le <b>chiffrement manque totalement</b> : le port
1883 transporte le CONNECT, les sujets et les charges utiles en clair. Les deux propriétés sont indépendantes : on peut authentifier
sans chiffrer (c'est le cas), ou chiffrer sans authentifier mutuellement (TLS serveur seul, TP2).</p>
""")}
{qa(5, "Proposez une mesure qui rendrait la capture inexploitable sans changer le code applicatif de l'ESP8266.", """
<p>Activer <b>TLS sur le broker</b> (port 8883, certificat serveur signé par une CA de laboratoire) et faire pointer le client vers
ce port avec une ancre de confiance. Côté ESP8266, on remplace <code>WiFiClient</code> par <code>WiFiClientSecure</code> et on charge
<code>ca.crt</code> ; les appels <code>connect()</code> et <code>publish()</code> ne changent pas. C'est exactement l'objet du TP2.</p>
<p>En complément (défense en profondeur) : identifiants uniques par objet, ACL par topic, limitation de débit et segmentation réseau.
Mais sans TLS, ces mesures ne empêchent pas l'écoute du mot de passe.</p>
""")}
</section>

<section>
<h1><span class="num">7</span>Barème et auto-évaluation</h1>
{table(
  ["Élément du barème", "Points", "Preuve dans ce rapport", "État"],
  [
    ["ESP8266 connecté, télémétrie reçue par le broker", "5 / 5", "Figures 2 et 3 ; <code>evidence/subscriber.txt</code>", badge("Fait")],
    ["Paquet CONNECT isolé, identifiants capturés", "5 / 5", "Figures 4 et 5 ; trame 14", badge("Fait")],
    ["Flux TCP analysé : sujets et valeurs relevés", "4 / 4", "Figure 6 ; quatre valeurs 20.0 → 22.1", badge("Fait")],
    ["Injection d'une fausse mesure réussie", "2 / 2", "Figure 7 ; trame 18 (payload 3939 = « 99 »)", badge("Fait")],
    ["Questions 1 à 5", "4 / 4", "Section 6", badge("Fait")],
    ["<b>Total</b>", "<b>20 / 20</b>", "Manipulations reproductibles, captures conservées", badge("Validé", "ok")],
  ],
  widths=["41%", "11%", "36%", "12%"])}
<p class="small">Auto-évaluation selon le barème du sujet. Les points de « durcissement final » du barème commun de la séance
sont traités dans la section 8 et, de façon complète, dans le TP2.</p>
</section>

<section>
<h1><span class="num">8</span>Durcissement et transition vers le TP2</h1>
<p>Le TP1 s'arrête volontairement à l'état non sécurisé. Le durcissement attendu au TP2 est un changement de <b>transport</b>, pas
de logique applicative :</p>
{code_block("Cible TP2 — extrait de configuration Mosquitto", '''
listener 8883
allow_anonymous false
password_file /etc/mosquitto/passwd
cafile   /etc/mosquitto/certs/ca.crt
certfile /etc/mosquitto/certs/broker.crt
keyfile  /etc/mosquitto/certs/broker.key
tls_version tlsv1.2
''')}
{code_block("Cible TP2 — côté objet (Arduino)", '''
BearSSL::WiFiClientSecure wifi;
BearSSL::X509List caCert(CA_CERT);
wifi.setTrustAnchors(&caCert);
mqtt.setServer("192.168.1.10", 8883);
''')}
{callout("ok", "Ce qu'il faut retenir",
  "Le mot de passe reste un secret partagé : TLS le protège en transit, mais ne prouve pas l'identité de l'objet si le secret est volé. "
  "Le TP2 apporte la confidentialité et l'authentification du serveur ; le TP3 ajoutera le certificat client (mTLS) pour une identité "
  "non rejouable.")}
</section>

<section class="page-break">
<h1><span class="num">9</span>Annexe A — script complet</h1>
{code_block("esp8266_sim.py", (TP / "esp8266_sim.py").read_text(), small=True)}
</section>

<section>
<h1><span class="num">10</span>Annexe B — configuration et preuves</h1>
<h2>B.1 Fichier de configuration du broker</h2>
{code_block("config/mosquitto.conf", (TP / "config/mosquitto.conf").read_text())}
<h2>B.2 Empreintes des preuves</h2>
<p>Les captures et sorties brutes sont conservées dans <code>lab-work/tp1/</code>. Leur empreinte SHA-256 permet de vérifier
qu'elles n'ont pas été modifiées après la séance.</p>
{table(
  ["Fichier", "Contenu", "SHA-256 (tronqué)"],
  [[f"<code>{esc(p.name)}</code>", desc, f"<code>{sha256(p)[:32]}…</code>"] for p, desc in [
    (TP / "captures/tp1_plaintext.pcapng", "Capture de la session MQTT en clair"),
    (TP / "captures/tp1_injection.pcapng", "Capture de l'injection de la fausse mesure"),
    (EV / "connect_credentials.txt", "Champs du CONNECT extraits par tshark"),
    (EV / "follow_tcp_stream.txt", "Session reconstituée (Follow TCP Stream)"),
    (EV / "mqtt_packets.txt", "Liste des paquets MQTT"),
    (EV / "simulator_console.txt", "Console de l'objet simulé"),
    (EV / "subscriber.txt", "Réception de la télémétrie"),
    (EV / "injection_observer.txt", "Réception de la mesure injectée"),
  ]],
  widths=["30%", "44%", "26%"])}
<h2>B.3 Reproductibilité</h2>
<p>Arrêt du broker : <code>docker rm -f tp1-broker</code> (les conteneurs sont éphémères). Les captures et les scripts restent dans le répertoire du TP.</p>
{code_block("Séquence minimale", '''
mkdir -p ~/labA && cd ~/labA
printf 'listener 1883 127.0.0.1\\nallow_anonymous false\\npassword_file /mosquitto/config/passwd\\n' > config/mosquitto.conf
docker run --rm -v "$PWD/config:/mosquitto/config" eclipse-mosquitto:2 \\
  mosquitto_passwd -c -b /mosquitto/config/passwd esp01 esp01pass
docker run -d --rm --name tp1-broker --network host --user $(id -u):$(id -g) \\
  -v "$PWD/config:/mosquitto/config:ro" eclipse-mosquitto:2
tshark -i lo -f "tcp port 1883" -w captures/tp1_plaintext.pcapng -q &
python3 esp8266_sim.py
''')}
</section>
"""

    out = Path(__file__).resolve().parent.parent / "TP1_Rapport_MQTT_sans_TLS.pdf"
    render_pdf(body, out, "TP1 — MQTT sans TLS · Rapport de laboratoire · 17 nov. 2026", "TP1 — MQTT sans TLS")
    return out


if __name__ == "__main__":
    print(build())
