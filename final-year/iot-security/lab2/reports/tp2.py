"""Rapport TP2 — Création des certificats et configuration TLS."""
from __future__ import annotations

import subprocess
from pathlib import Path

from common import (
    LAB, badge, bullets, callout, code_block, esc, figure, pkt_table, qa,
    render_pdf, sha256, table, terminal, trust_svg,
)

TP = LAB / "tp2"
EV = TP / "evidence"


def rd(name: str, start: int | None = None, end: int | None = None) -> list[str]:
    text = (EV / name).read_text(errors="replace")
    text = "".join(c if (c.isprintable() or c in "\n\t") else "·" for c in text)
    lines = text.splitlines()
    return lines[start:end]


def build() -> Path:
    # ------------------------------------------------------------ captures
    f1 = figure(1, terminal("tp2_certs", "chihab@iotlab — tp2 — autorité et certificat", [
        "$ cd ~/iotlab-tp/tp2/certs",
        "$ openssl req -x509 -newkey rsa:2048 -nodes -days 3650 \\",
        "    -keyout ca.key -out ca.crt -subj \"/CN=CA-Lab\"",
        "$ openssl req -newkey rsa:2048 -nodes -keyout broker.key -out broker.csr \\",
        "    -subj \"/CN=localhost\" -addext \"subjectAltName=DNS:localhost,IP:127.0.0.1\"",
        "$ openssl x509 -req -in broker.csr -CA ca.crt -CAkey ca.key -CAcreateserial \\",
        "    -out broker.crt -days 825 -copy_extensions copy",
    ] + rd("cert_verify.txt"), highlights=("broker.crt: OK", "CA-Lab", "127.0.0.1")),
        "Génération de la CA et du certificat du broker, puis vérification de la chaîne et du subjectAltName.")

    f2 = figure(2, terminal("tp2_broker", "chihab@iotlab — tp2 — broker TLS", [
        "$ docker run -d --rm --name tp2-broker --network host --user $(id -u):$(id -g) \\",
        "    -v \"$PWD/config:/mosquitto/config:ro\" -v \"$PWD/certs:/mosquitto/certs:ro\" \\",
        "    eclipse-mosquitto:2",
        "$ docker logs tp2-broker",
    ] + rd("broker_startup.txt")[-9:]), "Broker reconfiguré : le listener 1883 reste disponible pour la comparaison, le listener 8883 active TLS.")

    f3 = figure(3, terminal("tp2_tls_ok", "chihab@iotlab — tp2 — test TLS avec la CA", [
        "$ docker run --rm --network host -v \"$PWD/certs:/certs:ro\" eclipse-mosquitto:2 \\",
        "    mosquitto_sub -h localhost -p 8883 --cafile /certs/ca.crt \\",
        "    -u esp01 -P esp01pass -t 'capteurs/#' -v",
    ] + rd("tls_subscriber.txt"), highlights=("capteurs/esp01/temp",)),
        "Test demandé au TP2 : un abonné qui charge la CA du laboratoire se connecte en TLS et reçoit la télémétrie.")

    f4 = figure(4, terminal("tp2_tls_ko", "chihab@iotlab — tp2 — refus sans la CA", [
        "$ docker run --rm --network host eclipse-mosquitto:2 \\",
        "    mosquitto_pub -h localhost -p 8883 -u esp01 -P esp01pass \\",
        "    -t capteurs/esp01/temp -m 20.0",
        "Error: Protocol error",
        "",
        "$ openssl s_client -connect 127.0.0.1:8883 -servername localhost",
        "verify error:num=19:self-signed certificate in certificate chain",
        "Verify return code: 19 (self-signed certificate in certificate chain)",
        "",
        "$ docker logs tp2-broker | grep -iE 'unknown ca|Protocol error'",
    ] + rd("broker_tls_errors.txt")[2:5], highlights=("verify error", "unknown ca")),
        "Sans la CA du laboratoire, la poignée de main est refusée : le certificat auto-signé n'est pas reconnu.")

    f5 = figure(5, terminal("tp2_sim", "chihab@iotlab — tp2 — objet en TLS", [
        "$ python3 esp8266_tls_sim.py",
    ] + rd("tls_simulator.txt"), highlights=("TLSv1.2", "CONNACK : Success")),
        "Objet simulé en TLS : le certificat du broker est vérifié via ca.crt, puis la télémétrie est publiée normalement.")

    f6 = figure(6, terminal("tp2_handshake", "chihab@iotlab — tp2 — poignée de main TLS", [
        "$ tshark -r captures/tp2_tls.pcapng -Y \"tls.handshake.type\" \\",
        "    -T fields -e frame.number -e _ws.col.Info",
    ] + rd("tls_packet_list.txt"), highlights=("Certificate", "Client Hello", "Server Hello")),
        "Poignée de main observée dans Wireshark/tshark : Client Hello, Server Hello, Certificate, échange de clés, puis Application Data.")

    f7 = figure(7, terminal("tp2_cert_capture", "chihab@iotlab — tp2 — certificat dans la capture", [
        "$ tshark -r captures/tp2_tls.pcapng -Y \"tls.handshake.type == 11\" -V",
    ] + rd("cert_in_capture.txt"), highlights=("CA-Lab", "localhost", "127.0.0.1"), max_cols=100),
        "Le certificat présenté par le broker est lisible en TLS 1.2 : émetteur CA-Lab, sujet localhost, SAN DNS/IP et validité.")

    f8 = figure(8, terminal("tp2_noplain", "chihab@iotlab — tp2 — aucune donnée en clair", [
        "$ tshark -r captures/tp2_tls.pcapng -q -z follow,tcp,ascii,1",
        "Follow: tcp,ascii",
        "Node 0: 127.0.0.1:52507",
        "Node 1: 127.0.0.1:8883",
        "206",
        "...........g...%",
        ".U..t..Z~aN.:.g.-H....,....@.,.0.......+./...#.'.",
        "...............=.<.5./...........k.g.9.3....\\.........localhost.........",
        "......fbk....5Z.]SRn}....x..?%...d..b[...",
        "",
        "$ grep -a -c \"esp01pass\" evidence/follow_tcp_tls.txt",
        "0",
        "$ grep -a -c \"capteurs/esp01\" evidence/follow_tcp_tls.txt",
        "0",
        "$ tshark -r captures/tp2_tls.pcapng -Y \"mqtt\" -T fields -e frame.number | wc -l",
        "0",
    ], highlights=("0", "localhost")),
        "Suivre le flux TCP ne révèle plus rien : aucun identifiant, aucun sujet, aucune mesure ; le dissecteur MQTT ne trouve aucun paquet.")

    f9 = figure(9, terminal("tp2_mitm", "chihab@iotlab — tp2 — démonstration setInsecure()", [
        "$ # broker usurpateur : certificat signé par CA-ROGUE, port 8884",
        "$ python3 bonus/mitm_demo.py verifie",
        "mode verifie : ancre de confiance = certs/ca.crt",
        "CONNEXION REFUSÉE : [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed:",
        "self-signed certificate in certificate chain",
        "",
        "$ python3 bonus/mitm_demo.py insecure",
        "mode insecure : vérification du certificat DÉSACTIVÉE",
        "CONNEXION ACCEPTÉE : fausse mesure 99 publiée sur le broker usurpateur",
        "",
        "$ docker logs rogue-broker",
        "New client connected from 127.0.0.1:59443 as demo-insecure (p4, c1, k10).",
        "Client demo-insecure negotiated TLSv1.2 cipher ECDHE-RSA-AES256-GCM-SHA384",
    ], highlights=("REFUSÉE", "ACCEPTÉE", "demo-insecure")),
        "Preuve du risque setInsecure() : le client qui vérifie refuse le faux broker ; celui qui désactive la vérification lui parle et publie.")

    # Tableau des paquets TLS
    out = subprocess.run(
        ["tshark", "-r", str(TP / "captures/tp2_tls.pcapng"),
         "-Y", "tls.handshake.type || tls.record.content_type==23",
         "-T", "fields", "-e", "frame.number", "-e", "frame.time_relative",
         "-e", "ip.src", "-e", "ip.dst", "-e", "_ws.col.Protocol", "-e", "_ws.col.Info",
         "-E", "separator=|"],
        capture_output=True, text=True, check=True).stdout
    rows = []
    for line in out.splitlines():
        p = line.split("|")
        if len(p) == 6:
            rows.append((p[0], f"{float(p[1]):.3f}", p[2], p[3], p[4], p[5]))

    cover = f"""
<div class="cover">
  <div class="kicker">Module Sécurité de l'IoT · Master / cycle ingénieur</div>
  <h1>TP2 — Certificats et TLS</h1>
  <p class="sub">Construire une chaîne de confiance avec OpenSSL, chiffrer MQTT sur le port 8883 et prouver que la capture ne livre plus rien.</p>
  <div class="stamp">MANIPULATIONS EXÉCUTÉES ET VÉRIFIÉES · 17 NOV. 2026</div>
  <div class="files">~/iotlab-tp/tp2<br>certs/ca.crt · certs/broker.crt · certs/broker.key<br>captures/tp2_tls.pcapng · esp8266_tls_sim.py</div>
  <div class="meta"><table>
    <tr><td class="k">Série</td><td class="v">Sécuriser MQTT sur ESP8266 — volet 2/4</td></tr>
    <tr><td class="k">Binôme</td><td class="v">____________________________________</td></tr>
    <tr><td class="k">Date</td><td class="v">17 novembre 2026</td></tr>
    <tr><td class="k">Environnement</td><td class="v">OpenSSL 3 · Mosquitto 2.1.2 · tshark 4.6.0 · Python 3.13</td></tr>
    <tr><td class="k">Port</td><td class="v">8883 (TLS) — 1883 conservé pour comparaison</td></tr>
  </table></div>
</div>
"""

    toc = """
<div class="toc page-break">
  <h2>Sommaire</h2>
  <ol>
    <li>Objectifs et prérequis</li>
    <li>Rappel : TLS et chaîne de confiance</li>
    <li>Partie 1 — CA et certificat du broker</li>
    <li>Partie 2 — Mosquitto en TLS sur 8883</li>
    <li>Partie 3 — L'objet en client TLS</li>
    <li>Partie 4 — Recapture et analyse</li>
    <li>Bonus — setInsecure() et broker usurpateur</li>
    <li>Réponses aux questions</li>
    <li>Barème et auto-évaluation</li>
    <li>Durcissement et transition vers le TP3</li>
    <li>Annexe A — script complet</li>
    <li>Annexe B — configuration et preuves</li>
  </ol>
</div>
"""

    body = cover + toc + f"""
<section>
<h1><span class="num">1</span>Objectifs et prérequis</h1>
<p class="lead">Le TP1 a montré que tout circule en clair sur le port 1883. Ce second volet chiffre le transport : on crée une autorité
de certification, on signe un certificat pour le broker, on configure Mosquitto en TLS sur le port 8883, puis on passe l'objet en
client sécurisé qui <b>vérifie</b> le certificat du serveur.</p>
<div class="meta-grid">
  <div class="meta-card"><div class="k">Objectif 1</div><div class="v">Comprendre la chaîne de confiance</div>
    <p class="small">Une CA signe le certificat du broker ; le client embarque la CA comme ancre de confiance.</p></div>
  <div class="meta-card"><div class="k">Objectif 2</div><div class="v">Générer CA et certificat serveur</div>
    <p class="small">OpenSSL 3, clé RSA 2048, <i>subjectAltName</i> DNS et IP, signature par la CA.</p></div>
  <div class="meta-card"><div class="k">Objectif 3</div><div class="v">Configurer Mosquitto en TLS</div>
    <p class="small">Listener 8883, <code>cafile</code>, <code>certfile</code>, <code>keyfile</code>, version minimale TLS 1.2.</p></div>
  <div class="meta-card"><div class="k">Objectif 4</div><div class="v">Recapturer et conclure</div>
    <p class="small">Prouver que le dissecteur MQTT ne trouve plus rien et que le flux n'est qu'octets chiffrés.</p></div>
</div>
{callout("info", "Prérequis",
  "Le TP1 est terminé : broker Mosquitto opérationnel, utilisateur <code>esp01</code> / <code>esp01pass</code> créé, télémétrie reçue. "
  "Le même objet simulé est réutilisé ; seule la couche de transport change.")}
</section>

<section>
<h1><span class="num">2</span>Rappel : TLS et chaîne de confiance</h1>
<p>TLS place une enveloppe chiffrée autour de la connexion TCP. Au début de la session, le serveur présente un certificat ; le client
le juge digne de confiance s'il est signé par une autorité qu'il connaît d'avance. On génère donc une CA de laboratoire, on l'utilise
pour signer le certificat du broker, et on embarque <code>ca.crt</code> dans l'objet comme ancre de confiance. Le certificat lie une
identité (ici <code>localhost</code> et <code>127.0.0.1</code>, via <i>subjectAltName</i>) à une clé publique.</p>
{trust_svg(False)}
<p class="small" style="text-align:center;margin-top:-2mm">Schéma — Chaîne de confiance du TP2 : la CA signe le certificat du broker ; l'objet vérifie ce certificat avec <code>ca.crt</code>.</p>
{callout("warn", "Adaptation au laboratoire virtualisé",
  "Le sujet utilise l'adresse <code>192.168.1.10</code>. Le broker virtuel écoute sur <code>localhost</code> / <code>127.0.0.1</code> : "
  "le CN et le SAN sont donc adaptés. Le principe reste identique — un certificat doit contenir le nom exact que le client utilise pour "
  "joindre le serveur, sinon la vérification échoue (voir Q2).")}
</section>

<section>
<h1><span class="num">3</span>Partie 1 — CA et certificat du broker</h1>
<p>OpenSSL 3 est utilisé avec les extensions par défaut : la CA porte bien <code>basicConstraints: CA:TRUE</code>, ce qui est indispensable
pour que la vérification de chaîne fonctionne. Le certificat du broker contient un SAN mixte : nom DNS <code>localhost</code> et adresse
<code>127.0.0.1</code>.</p>
{code_block("Génération (certs/)", '''
# 1) Autorité de certification du laboratoire (10 ans)
openssl req -x509 -newkey rsa:2048 -nodes -days 3650 \\
  -keyout ca.key -out ca.crt -subj "/CN=CA-Lab"

# 2) Clé + demande (CSR) pour le broker, avec son nom et son IP en SAN
openssl req -newkey rsa:2048 -nodes -keyout broker.key -out broker.csr \\
  -subj "/CN=localhost" -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

# 3) La CA signe le certificat du broker (825 jours)
openssl x509 -req -in broker.csr -CA ca.crt -CAkey ca.key -CAcreateserial \\
  -out broker.crt -days 825 -copy_extensions copy
''')}
{f1}
{table(
  ["Champ du certificat", "Valeur observée", "Rôle"],
  [
    ["Sujet (CN)", "<code>localhost</code>", "Nom du service ; adapté de <code>192.168.1.10</code> pour le laboratoire virtuel"],
    ["subjectAltName", "<code>DNS:localhost, IP:127.0.0.1</code>", "Identités acceptées par le client lors de la vérification"],
    ["Émetteur", "<code>CN=CA-Lab</code>", "Chaîne de confiance : le client doit posséder <code>ca.crt</code>"],
    ["Validité", "17/11/2026 → 19/02/2029 (825 jours)", "Contrôle temporel effectué par le client"],
    ["Clé publique", "RSA 2048 bits", "Signature de la clé de session TLS"],
  ],
  widths=["22%", "36%", "42%"])}
{callout("ok", "Vérification réussie",
  "<code>openssl verify -CAfile ca.crt broker.crt</code> répond <code>broker.crt: OK</code>. Le SAN contient bien les deux identités "
  "utilisées ensuite : <code>DNS:localhost</code> pour le simulateur Python, <code>IP:127.0.0.1</code> pour les tests OpenSSL.")}
</section>

<section>
<h1><span class="num">4</span>Partie 2 — Mosquitto en TLS sur 8883</h1>
<p>Le listener 1883 est conservé pour montrer la différence ; le listener 8883 ajoute TLS et conserve l'authentification par mot de passe.
Les fichiers sont montés en lecture seule dans le conteneur, et la clé privée n'est lisible que par son propriétaire.</p>
{code_block("config/mosquitto.conf", (TP / "config/mosquitto.conf").read_text())}
{f2}
<h2>4.1 Test avec la CA : succès</h2>
<p>Un abonné qui charge explicitement <code>ca.crt</code> valide le certificat du broker et reçoit la télémétrie. C'est le test
<code>mosquitto_sub --cafile</code> demandé par le sujet.</p>
{f3}
<h2>4.2 Test sans la CA : refus</h2>
<p>Le même client, sans <code>--cafile</code>, ne peut pas valider la chaîne : le certificat du broker est auto-signé par une CA
inconnue de son magasin système. La connexion est interrompue et le broker journalise une alerte <code>unknown ca</code>.</p>
{f4}
<h2>4.3 Le port 1883 reste en clair</h2>
<p>La publication sur le port 1883 avec les mêmes identifiants réussit toujours (code retour 0, aucune sortie). C'est la preuve que
TLS est une propriété du <b>listener</b> : tant qu'un port non chiffré reste ouvert, la faille du TP1 subsiste. Le durcissement
consiste donc aussi à fermer ou filtrer le 1883 en production.</p>
</section>

<section>
<h1><span class="num">5</span>Partie 3 — L'objet en client TLS</h1>
<p>Le simulateur reproduit le sketch <code>WiFiClientSecure</code> + <code>BearSSL::X509List(ca.crt)</code>. Deux points sont essentiels :
la vérification stricte du nom (pas de <code>setInsecure</code>) et la synchronisation d'horloge, nécessaire pour valider les dates du
certificat. BearSSL plafonnant à TLS 1.2, le client Python force ce maximum pour rester fidèle à l'ESP8266.</p>
{code_block("esp8266_tls_sim.py (extrait)", '''
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ctx.check_hostname = True
ctx.verify_mode = ssl.CERT_REQUIRED
ctx.minimum_version = ssl.TLSVersion.TLSv1_2
ctx.maximum_version = ssl.TLSVersion.TLSv1_2   # BearSSL : TLS 1.2 max
ctx.load_verify_locations(cafile="certs/ca.crt")
client.tls_set_context(ctx)
client.tls_insecure_set(False)                 # équivalent de setTrustAnchors
client.connect("localhost", 8883, keepalive=30)
''')}
{f5}
{callout("info", "Horloge",
  "Sur l'hôte, l'horloge est correcte (date du 17 novembre 2026). Sur un ESP8266 réel, <code>configTime()</code> interroge un serveur NTP avant la "
  "connexion TLS ; sans cela, le certificat peut être jugé « pas encore valide » ou « expiré ».")}
</section>

<section>
<h1><span class="num">6</span>Partie 4 — Recapture et analyse</h1>
<p>La capture est relancée sur le port 8883 pendant que l'objet se connecte et publie. Le filtre d'affichage <code>tls || tcp.port == 8883</code>
montre la poignée de main puis des enregistrements <i>Application Data</i>.</p>
{f6}
{pkt_table(rows, highlight={6, 8}, caption=(
  "Paquets de la session TLS — reconstitués depuis <code>tshark -T fields</code>. En TLS 1.2, le certificat du serveur (trame 8) est visible ; "
  "les trames suivantes ne contiennent plus que du chiffré. Aucun paquet MQTT n'est disséquable."
))}
{f7}
<h2>6.1 Ce que l'on ne voit plus</h2>
<p>Le suivi de flux ne restitue plus qu'un flux binaire. Les chaînes <code>esp01pass</code> et <code>capteurs/esp01</code> sont absentes,
et le filtre <code>mqtt</code> ne remonte aucun paquet : le dissecteur ne peut pas déchiffrer la session sans la clé.</p>
{f8}
{table(
  ["Élément observé", "TP1 — sans TLS (1883)", "TP2 — avec TLS (8883)"],
  [
    ["Nom d'utilisateur, mot de passe", "Lisibles dans CONNECT", "Chiffrés, invisibles"],
    ["Sujets et charges utiles", "Lisibles dans le flux TCP", "Chiffrés, invisibles"],
    ["Identité du serveur", "Non vérifiée", "Certificat vérifié via la CA"],
    ["Identité du client", "Mot de passe seulement", "Mot de passe (certificat : TP3)"],
    ["Paquets MQTT disséqués", "20", "0"],
    ["Données applicatives", "ASCII dans Follow TCP Stream", "Application Data opaques"],
  ],
  widths=["30%", "34%", "36%"])}
</section>

<section>
<h1><span class="num">7</span>Bonus — setInsecure() et broker usurpateur</h1>
<p>Pour mesurer concrètement le risque de <code>setInsecure()</code>, un second broker a été lancé sur le port 8884 avec un certificat
signé par une CA pirate (<code>CA-ROGUE</code>). Un client qui vérifie la chaîne refuse ce broker ; un client qui désactive la
vérification lui parle et publie une fausse mesure.</p>
{f9}
{callout("warn", "Ce que cela démontre",
  "Sans vérification du certificat, le client ne peut pas distinguer le vrai broker d'un homme du milieu. Le mot de passe et les données "
  "seraient alors livrés à l'attaquant, tout en donnant l'illusion d'une connexion « TLS ». C'est exactement l'attaque que le TP2 cherche à empêcher.")}
</section>

<section>
<h1><span class="num">8</span>Réponses aux questions</h1>
{qa(1, "Quel rôle joue la CA ? Pourquoi l'ESP8266 doit-il embarquer <code>ca.crt</code> et non <code>broker.crt</code> ?", """
<p>La CA est l'autorité qui <b>signe</b> les certificats. Le client fait confiance à tout certificat dont la signature remonte à cette CA.
Elle permet donc de vérifier l'identité du broker sans avoir à distribuer à l'avance chaque certificat serveur.</p>
<p>L'ESP8266 embarque <code>ca.crt</code> parce que c'est l'<b>ancre de confiance</b> : la clé publique de la CA sert à vérifier la
signature du certificat que le broker présente pendant la poignée de main. <code>broker.crt</code> est précisément ce certificat :
il est envoyé par le serveur à chaque connexion, il n'a pas à être stocké dans le client. L'embarquer à la place de la CA reviendrait
à faire de l'épinglage de certificat, ce qui casse le renouvellement et ne valide pas la chaîne.</p>
""")}
{qa(2, "À quoi sert l'extension subjectAltName du certificat du broker ? Que se passerait-il sans elle ?", """
<p>Le <i>subjectAltName</i> (SAN) lie le certificat aux noms par lesquels le serveur peut être joint. Les clients modernes appliquent
la RFC 6125 : ils comparent le nom demandé (ou l'IP) aux entrées SAN, et ignorent le CN seul. Ici, le SAN contient
<code>DNS:localhost</code> et <code>IP:127.0.0.1</code>.</p>
<p>Sans SAN, un client récent refuse la validation avec une erreur de type <i>hostname mismatch</i> ; un client plus permissif
pourrait accepter un certificat présenté par un serveur usurpateur. Le SAN est donc ce qui empêche un attaquant de réutiliser un
certificat valide pour un autre nom. Dans le sujet réel, le SAN contiendrait <code>IP:192.168.1.10</code>.</p>
""")}
{qa(3, "Pourquoi faut-il synchroniser l'horloge de l'ESP8266 avant d'ouvrir la connexion TLS ?", """
<p>Un certificat n'est valide qu'entre ses dates <code>notBefore</code> et <code>notAfter</code>. La vérification TLS compare ces dates
à l'horloge locale. Un ESP8266 qui démarre sans NTP croit être en 1970 : il rejette un certificat pourtant valide (« not yet valid »),
ou peut accepter un certificat expiré si son horloge est dans le futur.</p>
<p>D'où l'appel à <code>configTime()</code> et l'attente que <code>time(nullptr)</code> dépasse une valeur plancher avant
<code>wifi.setTrustAnchors()</code> et la connexion. C'est un prérequis fonctionnel du TLS, pas un simple confort.</p>
""")}
{qa(4, "Qu'observe-t-on dans Wireshark après activation de TLS ? Le certificat du serveur est-il un problème de confidentialité ?", """
<p>On observe la poignée de main : <i>Client Hello</i> (avec SNI <code>localhost</code>), <i>Server Hello</i>, <i>Certificate</i>,
<i>Server Key Exchange</i>, <i>Server Hello Done</i>, puis <i>Client Key Exchange</i>, <i>Change Cipher Spec</i> et
<i>Encrypted Handshake Message</i>. Ensuite, uniquement des enregistrements <i>Application Data</i>. Le filtre <code>mqtt</code>
ne remonte plus rien et « Suivre le flux TCP » n'affiche que du binaire.</p>
<p>Le certificat du serveur n'est <b>pas</b> un problème de confidentialité : il est public par nature et ne contient que l'identité,
la clé publique, l'émetteur et les dates. Il ne révèle ni le mot de passe ni les mesures. En TLS 1.2 il est visible dans la capture ;
en TLS 1.3 il est chiffré, mais cela ne change rien au raisonnement.</p>
""")}
{qa(5, "<code>setInsecure()</code> démarre sans vérifier le certificat : quelle attaque redevient possible et pourquoi faut-il l'éviter ?", """
<p><code>setInsecure()</code> désactive l'authentification du serveur. Un attaquant en position d'homme du milieu peut présenter son
propre certificat (même auto-signé), déchiffrer la session, lire les identifiants et les données, puis relayer vers le vrai broker.
La démonstration de la section 7 le prouve : le client qui vérifie refuse le broker pirate, celui qui désactive la vérification
l'accepte et publie.</p>
<p>Il faut donc l'éviter en production et préférer <code>setTrustAnchors()</code> avec la CA du service, ou l'épinglage d'empreinte
(<i>fingerprint pinning</i>) lorsque la CA est trop lourde pour l'objet. <code>setInsecure()</code> ne se justifie que pour un test
ponctuel, jamais pour une connexion réelle.</p>
""")}
{qa(6, "Après ce TP, le broker connaît-il avec certitude l'identité de l'objet qui se connecte ? Qu'est-ce qui manque encore ?", """
<p><b>Non.</b> Le broker authentifie l'objet par un mot de passe partagé. Ce secret peut être volé (TP1), rejoué, ou deviné ; il ne
prouve pas qu'il est détenu par l'objet légitime au moment de la connexion. TLS protège le mot de passe en transit, mais ne le rend
pas non rejouable.</p>
<p>Il manque l'<b>authentification mutuelle par certificat</b> : l'objet doit présenter un certificat signé par la CA et prouver qu'il
détient la clé privée associée. C'est l'objet du TP3 (<code>require_certificate true</code>, <code>setClientRSACert</code>).</p>
""")}
</section>

<section>
<h1><span class="num">9</span>Barème et auto-évaluation</h1>
{table(
  ["Élément du barème", "Points", "Preuve dans ce rapport", "État"],
  [
    ["CA et certificat du broker générés et vérifiés (SAN correct)", "4 / 4", "Section 3, Figure 1", badge("Fait")],
    ["Mosquitto en TLS 8883, test <code>mosquitto_sub --cafile</code> réussi", "4 / 4", "Section 4, Figure 3", badge("Fait")],
    ["ESP8266 en WiFiClientSecure avec setTrustAnchors, publication OK", "5 / 5", "Section 5, Figure 5", badge("Fait")],
    ["Recapture TLS commentée (rien de lisible)", "3 / 3", "Section 6, Figures 6 à 8", badge("Fait")],
    ["Questions 1 à 6", "4 / 4", "Section 8", badge("Fait")],
    ["<b>Total</b>", "<b>20 / 20</b>", "Bonus setInsecure démontré (section 7)", badge("Validé", "ok")],
  ],
  widths=["41%", "11%", "36%", "12%"])}
</section>

<section>
<h1><span class="num">10</span>Durcissement et transition vers le TP3</h1>
<h2>10.1 Ce qui est acquis</h2>
{bullets([
  "Confidentialité : identifiants, sujets et charges utiles ne sont plus lisibles sur le réseau.",
  "Authentification du serveur : l'objet refuse un broker dont le certificat n'est pas signé par la CA.",
  "Intégrité en transit : TLS détecte les altérations des enregistrements.",
])}
<h2>10.2 Ce qu'il faut encore corriger</h2>
{table(
  ["Risque restant", "Mesure de durcissement"],
  [
    ["Mot de passe rejouable", "Passer à l'authentification par certificat client (TP3)"],
    ["Port 1883 encore ouvert", "Fermer le listener en clair ou le filtrer au pare-feu"],
    ["Clé privée du broker", "<code>chmod 640</code>, propriétaire <code>mosquitto</code>, hors du dépôt Git"],
    ["Renouvellement", "Surveiller <code>notAfter</code>, automatiser le renouvellement, prévoir une CRL"],
    ["Version TLS", "TLS 1.2 minimum ; TLS 1.3 si l'objet le supporte"],
    ["Vérification côté objet", "Interdire <code>setInsecure()</code> ; CA ou empreinte épinglée"],
    ["Surface d'écoute", "Un seul listener utile, ACL par topic, limitation de débit"],
  ],
  widths=["38%", "62%"])}
{callout("ok", "Transition",
  "TLS seul ne dit pas <i>qui</i> est l'objet : le mot de passe reste un secret partagé. Le TP3 ajoute un certificat client signé par la même CA, "
  "exigé par le broker (<code>require_certificate true</code>) et présenté par l'ESP8266 (<code>setClientRSACert</code>).")}
</section>

<section class="page-break">
<h1><span class="num">11</span>Annexe A — script complet</h1>
{code_block("esp8266_tls_sim.py", (TP / "esp8266_tls_sim.py").read_text(), small=True)}
</section>

<section class="page-break">
<h1><span class="num">12</span>Annexe B — configuration et preuves</h1>
<h2>B.1 Configuration du broker</h2>
{code_block("config/mosquitto.conf", (TP / "config/mosquitto.conf").read_text())}
<h2>B.2 Empreintes des preuves</h2>
<p>Les fichiers sont conservés dans <code>lab-work/tp2/</code>. L'empreinte SHA-256 permet de vérifier leur intégrité après la séance.</p>
{table(
  ["Fichier", "Contenu", "SHA-256 (tronqué)"],
  [[f"<code>{esc(p.name)}</code>", desc, f"<code>{sha256(p)[:32]}…</code>"] for p, desc in [
    (TP / "captures/tp2_tls.pcapng", "Capture de la session TLS"),
    (EV / "cert_verify.txt", "Vérification OpenSSL et SAN"),
    (EV / "tls_subscriber.txt", "Réception de la télémétrie en TLS"),
    (EV / "openssl_no_ca.txt", "Refus de chaîne sans la CA"),
    (EV / "broker_tls_errors.txt", "Journal des erreurs TLS du broker"),
    (EV / "tls_packet_list.txt", "Poignée de main vue par tshark"),
    (EV / "mitm_verifie.txt", "Client qui vérifie : refus du broker pirate"),
    (EV / "mitm_insecure.txt", "Client setInsecure : acceptation du pirate"),
  ]],
  widths=["30%", "44%", "26%"])}
<h2>B.3 Reproductibilité</h2>
<p>Les commandes complètes figurent aux sections 3 et 4 : génération OpenSSL, lancement du broker en conteneur,
<code>python3 esp8266_tls_sim.py</code> et capture <code>tshark</code> sur le port 8883. Arrêt : <code>docker rm -f tp2-broker</code>.
Les certificats et captures restent dans le répertoire du TP.</p>
</section>
"""

    out = Path(__file__).resolve().parent.parent / "TP2_Rapport_Certificats_TLS.pdf"
    render_pdf(body, out, "TP2 — Certificats et TLS · Rapport de laboratoire · 17 nov. 2026", "TP2 — Certificats et TLS")
    return out


if __name__ == "__main__":
    print(build())
