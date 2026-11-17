"""Rapport TP3 — Authentification mutuelle (mTLS)."""
from __future__ import annotations

import subprocess
from pathlib import Path

from common import (
    LAB, badge, bullets, callout, code_block, esc, figure, pkt_table, qa,
    render_pdf, sha256, table, terminal, trust_svg, sequence_svg,
)

TP = LAB / "tp3"
EV = TP / "evidence"


def rd(name: str, start: int | None = None, end: int | None = None) -> list[str]:
    text = (EV / name).read_text(errors="replace")
    text = "".join(c if (c.isprintable() or c in "\n\t") else "·" for c in text)
    lines = text.splitlines()
    return lines[start:end]


def build() -> Path:
    # ------------------------------------------------------------ captures
    f1 = figure(1, terminal("tp3_cert", "chihab@iotlab — tp3 — certificat client", [
        "$ openssl req -newkey rsa:2048 -nodes -keyout esp01.key -out esp01.csr \\",
        "    -subj \"/CN=esp01-client/O=IOT-LAB\"",
        "$ openssl x509 -req -in esp01.csr -CA ca.crt -CAkey ca.key -CAcreateserial \\",
        "    -out esp01.crt -days 825",
    ] + rd("cert_verify_client.txt"), highlights=("esp01.crt: OK", "esp01-client", "CA-Lab")),
        "Certificat client généré par la même CA, vérifié par OpenSSL : sujet CN=esp01-client, émetteur CA-Lab.")

    f2 = figure(2, terminal("tp3_broker", "chihab@iotlab — tp3 — broker mTLS", [
        "$ docker run -d --rm --name tp3-broker --network host --user $(id -u):$(id -g) \\",
        "    -v \"$PWD/config:/mosquitto/config:ro\" -v \"$PWD/certs:/mosquitto/certs:ro\" \\",
        "    eclipse-mosquitto:2",
        "$ docker logs tp3-broker",
    ] + rd("broker_startup.txt")[-8:]), "Broker configuré avec require_certificate true : le listener 8883 exige désormais un certificat client.")

    f3 = figure(3, terminal("tp3_refus_cert", "chihab@iotlab — tp3 — connexion sans certificat", [
        "$ docker run --rm --network host -v \"$PWD/certs:/certs:ro\" eclipse-mosquitto:2 \\",
        "    mosquitto_pub -h localhost -p 8883 --cafile /certs/ca.crt \\",
        "    -u esp01 -P esp01pass -t capteurs/esp01/temp -m 20.0",
        "Error: The connection was lost",
        "",
        "$ docker logs tp3-broker | grep -i certificate",
    ] + [l.split(": ", 1)[1].replace("OpenSSL Error while trying to get the error[0]: ", "")
         for l in rd("broker_mtls_errors.txt")], highlights=("peer did not return a certificate", "Error")),
        "Preuve par l'absurde : sans certificat client, le broker interrompt la poignée de main et journalise « peer did not return a certificate ».")

    f4 = figure(4, terminal("tp3_ok", "chihab@iotlab — tp3 — connexion avec certificat", [
        "$ docker run --rm --network host -v \"$PWD/certs:/certs:ro\" eclipse-mosquitto:2 \\",
        "    mosquitto_sub -h localhost -p 8883 --cafile /certs/ca.crt \\",
        "    --cert /certs/esp01.crt --key /certs/esp01.key \\",
        "    -u esp01 -P esp01pass -t 'capteurs/#' -v",
    ] + rd("mtls_subscriber.txt"), highlights=("capteurs/esp01/temp",)),
        "Avec le certificat et la clé, la connexion mTLS est acceptée et la télémétrie circule normalement.")

    f5 = figure(5, terminal("tp3_sim", "chihab@iotlab — tp3 — objet en mTLS", [
        "$ python3 esp8266_mtls_sim.py",
    ] + rd("mtls_simulator2.txt"), highlights=("TLSv1.2", "CONNACK : Success")),
        "Objet simulé en mTLS : le broker est authentifié par la CA et le client par son certificat, puis les publications passent.")

    f6 = figure(6, terminal("tp3_handshake", "chihab@iotlab — tp3 — poignée de main mTLS", [
        "$ tshark -r captures/tp3_mtls.pcapng -Y \"tls.handshake.type\" \\",
        "    -T fields -e frame.number -e _ws.col.Info",
    ] + rd("mtls_packet_list.txt"), highlights=("Certificate Request", "Certificate, Client", "Certificate Verify")),
        "Poignée de main mTLS : le serveur ajoute Certificate Request ; le client répond Certificate + Certificate Verify.")

    f7 = figure(7, terminal("tp3_certreq", "chihab@iotlab — tp3 — Certificate Request", [
        "$ tshark -r captures/tp3_mtls.pcapng -Y \"frame.number == 8\" -V",
    ] + rd("cert_request.txt", 0, 15) + ["                …"], highlights=("Certificate Request (13)", "RSA Sign", "ECDSA Sign")),
        "Détail du Certificate Request envoyé par le broker : types de certificats acceptés et algorithmes de signature.")

    f8 = figure(8, terminal("tp3_clientcert", "chihab@iotlab — tp3 — certificat présenté par l'objet", [
        "$ tshark -r captures/tp3_mtls.pcapng -Y \"frame.number == 10\" -V",
    ] + [
        "Certificate",
        "  signedCertificate",
        "    version: v3 (2)",
        "    signature (sha256WithRSAEncryption)",
        "    issuer: rdnSequence: 1 item (id-at-commonName=CA-Lab)",
        "        uTF8String: CA-Lab",
        "    validity",
        "      notBefore: 2026-11-17 11:37:06 (UTC)",
        "      notAfter:  2029-02-19 11:37:06 (UTC)",
        "    subject: rdnSequence: 2 items",
        "        (id-at-organizationName=IOT-LAB, id-at-commonName=esp01-client)",
        "      uTF8String: esp01-client",
        "      uTF8String: IOT-LAB",
        "    subjectPublicKeyInfo",
        "      algorithm (rsaEncryption)",
    ], highlights=("CA-Lab", "esp01-client", "IOT-LAB")),
        "Certificat client présenté dans le flux : émetteur CA-Lab, sujet CN=esp01-client / O=IOT-LAB, validité 2026-2029.")

    f9 = figure(9, terminal("tp3_refus_handshake", "chihab@iotlab — tp3 — handshake refusé", [
        "$ tshark -r captures/tp3_mtls_refus.pcapng \\",
        "    -Y \"tls.handshake.type || tls.alert_message\" \\",
        "    -T fields -e frame.number -e _ws.col.Info",
    ] + rd("refus_evidence.txt"), highlights=("Certificate Request", "Alert", "Handshake Failure")),
        "Sans certificat : le serveur demande un certificat, le client n'en fournit pas, le serveur émet une alerte fatale et aucune donnée applicative ne passe.")

    # Tableau des paquets mTLS
    out = subprocess.run(
        ["tshark", "-r", str(TP / "captures/tp3_mtls.pcapng"),
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
  <h1>TP3 — Authentification mutuelle</h1>
  <p class="sub">mTLS sur MQTT : donner un certificat à l'objet, exiger sa preuve côté broker, et observer Certificate Request / Certificate Verify.</p>
  <div class="stamp">MANIPULATIONS EXÉCUTÉES ET VÉRIFIÉES · 17 NOV. 2026</div>
  <div class="files">~/iotlab-tp/tp3<br>certs/esp01.crt · certs/esp01.key · config/mosquitto.conf<br>captures/tp3_mtls.pcapng · captures/tp3_mtls_refus.pcapng</div>
  <div class="meta"><table>
    <tr><td class="k">Série</td><td class="v">Sécuriser MQTT sur ESP8266 — volet 3/4</td></tr>
    <tr><td class="k">Binôme</td><td class="v">____________________________________</td></tr>
    <tr><td class="k">Date</td><td class="v">17 novembre 2026</td></tr>
    <tr><td class="k">Environnement</td><td class="v">OpenSSL 3 · Mosquitto 2.1.2 · tshark 4.6.0 · Python 3.13</td></tr>
    <tr><td class="k">Mode</td><td class="v">TLS 1.2 + require_certificate true</td></tr>
  </table></div>
</div>
"""

    toc = """
<div class="toc page-break">
  <h2>Sommaire</h2>
  <ol>
    <li>Objectifs et prérequis</li>
    <li>Rappel : TLS mutuel</li>
    <li>Partie 1 — certificat client</li>
    <li>Partie 2 — exiger le certificat côté broker</li>
    <li>Partie 3 — l'objet présente son certificat</li>
    <li>Partie 4 — observer mTLS dans Wireshark</li>
    <li>Réponses aux questions</li>
    <li>Barème et auto-évaluation</li>
    <li>Durcissement et transition vers le TP4</li>
    <li>Annexe A — script complet</li>
    <li>Annexe B — configuration et preuves</li>
  </ol>
</div>
"""

    body = cover + toc + f"""
<section>
<h1><span class="num">1</span>Objectifs et prérequis</h1>
<p class="lead">Au TP2, l'objet vérifie le broker, mais le broker n'identifie l'objet que par un mot de passe — volé ou rejoué, il suffit
à se faire passer pour lui. Ici, l'objet reçoit son propre certificat, signé par la même CA, et le broker l'exige. Les deux pairs se
prouvent mutuellement leur identité.</p>
<div class="meta-grid">
  <div class="meta-card"><div class="k">Objectif 1</div><div class="v">Générer un certificat client</div>
    <p class="small">Clé et CSR avec <code>CN=esp01-client</code>, signés par <code>CA-Lab</code>, vérifiés avec OpenSSL.</p></div>
  <div class="meta-card"><div class="k">Objectif 2</div><div class="v">Exiger le certificat au broker</div>
    <p class="small"><code>require_certificate true</code> sur le listener 8883, preuve du refus sans certificat.</p></div>
  <div class="meta-card"><div class="k">Objectif 3</div><div class="v">Charger le certificat dans l'objet</div>
    <p class="small">Équivalent de <code>setClientRSACert(&amp;clientCrt, &amp;clientKey)</code> avec <code>ssl.load_cert_chain</code>.</p></div>
  <div class="meta-card"><div class="k">Objectif 4</div><div class="v">Observer mTLS dans Wireshark</div>
    <p class="small">Repérer <i>Certificate Request</i>, <i>Certificate</i> client et <i>Certificate Verify</i>.</p></div>
</div>
{callout("info", "Prérequis",
  "TP2 terminé : CA du laboratoire, certificat broker avec SAN, Mosquitto en TLS 8883, objet qui vérifie le serveur. "
  "On réutilise la même CA ; seul le certificat client et l'exigence côté broker sont ajoutés.")}
</section>

<section>
<h1><span class="num">2</span>Rappel : TLS mutuel</h1>
<p>En TLS classique, seul le serveur prouve son identité. En mTLS, le serveur envoie en plus un <i>Certificate Request</i> ; le client
répond par son <i>Certificate</i> et un <i>Certificate Verify</i> — une signature qui prouve qu'il détient la clé privée associée.
Le broker n'accepte alors que des objets porteurs d'un certificat signé par la CA de confiance : le secret n'est plus un mot de passe
réutilisable, mais une clé privée qui ne quitte jamais l'objet.</p>
{trust_svg(True)}
<p class="small" style="text-align:center;margin-top:-2mm">Schéma — mTLS : la CA signe le broker et l'objet ; chacun vérifie le certificat de l'autre.</p>
{sequence_svg()}
<p class="small" style="text-align:center;margin-top:-2mm">Schéma — Séquence mTLS observée dans la capture : demande, présentation, preuve de possession, puis données chiffrées.</p>
</section>

<section class="page-break">
<h1><span class="num">3</span>Partie 1 — certificat client</h1>
<p>Le certificat client est signé par la CA du TP2. Le CN identifie l'objet ; l'organisation ajoute un contexte de déploiement.
La clé privée <code>esp01.key</code> reste sur l'objet et ne sera jamais transmise.</p>
{code_block("Génération (certs/)", '''
cd ~/iotlab-tp/tp3/certs
openssl req -newkey rsa:2048 -nodes -keyout esp01.key -out esp01.csr \\
  -subj "/CN=esp01-client/O=IOT-LAB"
openssl x509 -req -in esp01.csr -CA ca.crt -CAkey ca.key -CAcreateserial \\
  -out esp01.crt -days 825
openssl verify -CAfile ca.crt esp01.crt      # doit afficher : esp01.crt: OK
''')}
{f1}
{table(
  ["Champ", "Valeur", "Rôle"],
  [
    ["Sujet (CN)", "<code>esp01-client</code>", "Identité cryptographique de l'objet"],
    ["Organisation (O)", "<code>IOT-LAB</code>", "Contexte de déploiement"],
    ["Émetteur", "<code>CA-Lab</code>", "Même CA que le broker : une seule ancre de confiance"],
    ["Validité", "17/11/2026 → 19/02/2029", "Expiration et renouvellement planifiés"],
    ["Clé privée", "<code>esp01.key</code>, chmod 600", "Ne quitte jamais l'objet ; jamais dans un dépôt"],
  ],
  widths=["22%", "32%", "46%"])}
{callout("warn", "Protection de la clé",
  "La clé privée est le secret le plus critique du montage. Elle est créée avec des permissions restrictives (<code>600</code>) et "
  "n'est incluse ni dans la capture ni dans les échanges. Sur un ESP8266 réel, elle est stockée en flash : un accès physique permet "
  "de l'extraire, d'où l'intérêt d'un élément sécurisé ou d'un flash chiffré pour un déploiement industriel.")}
</section>

<section>
<h1><span class="num">4</span>Partie 2 — exiger le certificat côté broker</h1>
<p>On ajoute une seule directive au listener TLS du TP2. Le mot de passe du TP1 peut rester comme second facteur ; l'identité
principale devient le certificat.</p>
{code_block("config/mosquitto.conf", (TP / "config/mosquitto.conf").read_text())}
{f2}
<h2>4.1 Sans certificat client : refus</h2>
<p>La connexion est interrompue pendant la poignée de main. Le message côté client est générique (<i>connection lost</i>) ; c'est le
journal du broker qui donne la cause exacte.</p>
{f3}
<h2>4.2 Avec le certificat : acceptation</h2>
<p>Avec <code>--cert esp01.crt --key esp01.key</code>, la poignée de main aboutit et l'abonné reçoit les mesures. C'est la preuve
que le certificat client est bien exigé et correctement vérifié.</p>
{f4}
</section>

<section>
<h1><span class="num">5</span>Partie 3 — l'objet présente son certificat</h1>
<p>Le simulateur reprend le client TLS du TP2 et ajoute le certificat et la clé du client avant la connexion. Le reste du code
applicatif est inchangé : seule la configuration TLS diffère.</p>
{code_block("esp8266_mtls_sim.py (extrait)", '''
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ctx.check_hostname = True
ctx.verify_mode = ssl.CERT_REQUIRED
ctx.minimum_version = ssl.TLSVersion.TLSv1_2
ctx.maximum_version = ssl.TLSVersion.TLSv1_2
ctx.load_verify_locations(cafile="certs/ca.crt")     # ancre de confiance (TP2)
ctx.load_cert_chain(certfile="certs/esp01.crt",
                    keyfile="certs/esp01.key")        # setClientRSACert (TP3)
client.tls_set_context(ctx)
client.connect("localhost", 8883, keepalive=30)
''')}
{f5}
{callout("ok", "Résultat",
  "Le broker accepte la connexion et la télémétrie circule. Le mot de passe est conservé dans le laboratoire comme second facteur, "
  "mais il n'est plus la preuve d'identité : celle-ci repose sur la clé privée <code>esp01.key</code>.")}
</section>

<section>
<h1><span class="num">6</span>Partie 4 — observer mTLS dans Wireshark</h1>
<p>La capture est relancée sur le port 8883. La poignée de main contient désormais un <i>Certificate Request</i> du broker, puis un
<i>Certificate</i> et un <i>Certificate Verify</i> envoyés par l'objet.</p>
{f6}
{pkt_table(rows, highlight={8, 10}, caption=(
  "Paquets de la session mTLS — reconstitués depuis <code>tshark -T fields</code>. La trame 8 demande le certificat client ; "
  "la trame 10 le présente et prouve la possession de la clé. Les données MQTT restent chiffrées."
))}
{f7}
{f8}
<h2>6.1 Sans certificat : la poignée de main échoue</h2>
<p>Une seconde capture, réalisée avec un client qui ne charge pas de certificat, montre l'échec : le serveur demande un certificat,
le client n'en fournit pas, puis le serveur émet une alerte fatale. Aucune donnée applicative n'est échangée.</p>
{f9}
{table(
  ["Observation", "Sans certificat client", "Avec certificat client"],
  [
    ["Certificate Request (serveur)", "Présent", "Présent"],
    ["Certificate (client)", "Vide", "CN=esp01-client, émetteur CA-Lab"],
    ["Certificate Verify", "Absent", "Signature vérifiée par le broker"],
    ["Résultat de la poignée de main", "Alerte fatale <i>handshake failure</i>", "Succès"],
    ["Données MQTT", "Aucune", "Chiffrées (Application Data)"],
    ["Journal broker", "<code>peer did not return a certificate</code>", "Client connecté"],
  ],
  widths=["32%", "34%", "34%"])}
</section>

<section>
<h1><span class="num">7</span>Réponses aux questions</h1>
{qa(1, "Qu'ajoute mTLS par rapport au TLS du TP2 ? Quels messages de la poignée de main en témoignent ?", """
<p>mTLS ajoute l'<b>authentification du client</b> : le broker ne se contente plus de présenter son certificat, il exige que l'objet
présente le sien et prouve qu'il détient la clé privée correspondante. L'identité de l'objet ne repose plus sur un mot de passe
partagé, mais sur un certificat propre à l'équipement.</p>
<p>Trois messages en témoignent dans la capture : le <b>Certificate Request</b> (type 13) envoyé par le broker dans sa réponse
<i>Server Hello</i> ; le <b>Certificate</b> (type 11) envoyé par l'ESP8266 avec son certificat <code>CN=esp01-client</code> ; enfin le
<b>Certificate Verify</b> (type 15), signature qui prouve la possession de <code>esp01.key</code>.</p>
""")}
{qa(2, "À quoi sert le <i>Certificate Verify</i> envoyé par le client ? Que prouve-t-il qu'un simple envoi du certificat ne prouverait pas ?", """
<p>Le certificat est public : n'importe qui peut en copier un et le présenter. Le <i>Certificate Verify</i> est une <b>signature</b>,
produite avec la clé privée du client, sur l'empreinte des messages de la poignée de main. Le serveur la vérifie avec la clé publique
du certificat.</p>
<p>Il prouve donc que le client <b>détient réellement la clé privée</b> associée au certificat, et pas seulement une copie du
certificat. Il lie aussi la preuve à cette session précise (transcript de la poignée de main), ce qui empêche de rejouer une ancienne
signature dans une autre connexion.</p>
""")}
{qa(3, "La clé privée <code>esp01.key</code> circule-t-elle sur le réseau ? Où reste-t-elle, et pourquoi est-ce essentiel ?", """
<p><b>Non.</b> Seuls le certificat (public) et la signature du <i>Certificate Verify</i> sont envoyés. La clé privée reste dans
l'objet, sur son stockage local, et n'est jamais transmise. C'est ce qui rend l'identité non usurpable : même en capturant tout le
trafic, un attaquant ne peut pas produire de signature valide sans la clé.</p>
<p>C'est aussi la limite : si un attaquant obtient un accès physique ou logique à l'objet et extrait la clé, il peut se faire passer
pour lui. D'où la protection du stockage (flash chiffrée, élément sécurisé) et la révocation du certificat en cas de compromission.</p>
""")}
{qa(4, "En quoi un certificat client est-il plus robuste qu'un mot de passe partagé (vol, rejeu, révocation) ?", """
<p>Un mot de passe partagé se capture (TP1), se devine, se réutilise et ne distingue pas deux équipements. Un certificat client
repose sur une <b>paire de clés</b> : la clé privée ne circule jamais, et chaque connexion exige une signature fraîche, donc le rejeu
ne fonctionne pas. Chaque objet peut avoir son propre certificat, ce qui permet des ACL par équipement.</p>
<p>Le certificat se <b>révoque</b> individuellement (CRL ou OCSP), expire automatiquement, et peut être renouvelé sans changer les
autres objets. Il reste toutefois sensible au vol de clé et à une mauvaise procédure de provisionnement ; ce n'est pas une baguette
magique, mais l'identité est bien plus forte qu'un secret partagé.</p>
""")}
{qa(5, "Que se passe-t-il, côté broker et dans Wireshark, si l'objet ne présente pas de certificat ?", """
<p>Côté broker, la poignée de main s'arrête : le serveur a envoyé <i>Certificate Request</i>, le client répond avec un
<i>Certificate</i> vide, puis le broker journalise <code>peer did not return a certificate</code> et ferme la connexion
(<i>Protocol error</i>).</p>
<p>Dans Wireshark, on voit le <i>Certificate Request</i> dans le <i>Server Hello</i>, puis un <i>Certificate</i> vide côté client et une
<b>alerte fatale</b> <i>Handshake Failure</i> (description 40). Aucun <i>Application Data</i> n'apparaît : MQTT ne se connecte jamais.
C'est exactement ce que montre la figure 9.</p>
""")}
{qa(6, "Avec <code>use_identity_as_username</code>, le CN du certificat devient l'identité MQTT. Quel intérêt pour les ACL du TP4 ?", """
<p>L'identité utilisée pour les ACL devient <code>esp01-client</code>, valeur <b>prouvée cryptographiquement</b> par le certificat, et
non un nom d'utilisateur déclaré avec un mot de passe. Les règles ACL peuvent donc être écrites par équipement :
<code>esp01-client</code> ne peut publier que sur ses sujets et lire que ses commandes.</p>
<p>Cela supprime le mot de passe partagé et rend l'usurpation beaucoup plus difficile : un attaquant devrait voler la clé privée de
l'objet, pas seulement un secret rejouable. C'est la base d'une autorisation fiable pour le TP4 (ACL par identité).</p>
""")}
</section>

<section>
<h1><span class="num">8</span>Barème et auto-évaluation</h1>
{table(
  ["Élément du barème", "Points", "Preuve dans ce rapport", "État"],
  [
    ["Certificat client généré et vérifié (<code>openssl verify</code> OK)", "4 / 4", "Section 3, Figure 1", badge("Fait")],
    ["<code>require_certificate</code> activé ; refus sans certificat démontré", "4 / 4", "Section 4, Figure 3", badge("Fait")],
    ["ESP8266 avec <code>setClientRSACert</code>, connexion mTLS réussie", "5 / 5", "Section 5, Figures 4 et 5", badge("Fait")],
    ["Capture mTLS commentée (Certificate Request + Certificate)", "3 / 3", "Section 6, Figures 6 à 9", badge("Fait")],
    ["Questions 1 à 6", "4 / 4", "Section 7", badge("Fait")],
    ["<b>Total</b>", "<b>20 / 20</b>", "Refus et succès tous deux prouvés", badge("Validé", "ok")],
  ],
  widths=["41%", "11%", "36%", "12%"])}
</section>

<section>
<h1><span class="num">9</span>Durcissement et transition vers le TP4</h1>
<h2>9.1 Bonnes pratiques mTLS</h2>
{table(
  ["Point", "Mesure recommandée"],
  [
    ["Unicité", "Un certificat par objet (pas de certificat partagé entre équipements)"],
    ["Provisionnement", "Générer la clé sur l'objet ou l'injecter par un canal sûr ; jamais par e-mail ou dépôt Git"],
    ["Stockage", "Clé en élément sécurisé ou flash chiffrée ; permissions minimales"],
    ["Révocation", "CRL/OCSP accessible, procédure en cas de perte ou de vol de l'objet"],
    ["Durée de vie", "Certificats courts, renouvellement automatisé avant expiration"],
    ["CA", "Clé de CA hors ligne, protégée ; une CA par environnement (labo / production)"],
    ["Identité et ACL", "<code>use_identity_as_username</code> + ACL par CN, pas de mot de passe partagé"],
    ["Version TLS", "TLS 1.2 minimum ; TLS 1.3 si l'objet le supporte"],
    ["Horloge", "NTP obligatoire avant la connexion (validité des certificats)"],
  ],
  widths=["24%", "76%"])}
<h2>9.2 Ce qui reste à faire (TP4)</h2>
<p>mTLS prouve <b>qui</b> se connecte, mais ne dit pas <b>ce qu'il a le droit de faire</b>. Un objet authentifié peut encore publier
sur n'importe quel topic si aucune ACL ne l'en empêche. Le TP4 ajoutera le contrôle d'accès par topic, idéalement indexé sur le CN
du certificat (<code>use_identity_as_username true</code>), pour que chaque objet ne puisse écrire que ses mesures et lire que ses
commandes.</p>
{callout("ok", "Chaîne de sécurité complète",
  "TP1 : le problème (tout est lisible). TP2 : confidentialité + authentification du serveur. TP3 : authentification de l'objet. "
  "TP4 : autorisation fine par topic. Chaque brique ne remplace pas les précédentes : elles se cumulent.")}
</section>

<section>
<h1><span class="num">10</span>Annexe A — script complet</h1>
{code_block("esp8266_mtls_sim.py", (TP / "esp8266_mtls_sim.py").read_text(), small=True)}
</section>

<section>
<h1><span class="num">11</span>Annexe B — configuration et preuves</h1>
<h2>B.1 Configuration du broker</h2>
{code_block("config/mosquitto.conf", (TP / "config/mosquitto.conf").read_text())}
<h2>B.2 Empreintes des preuves</h2>
<p>Les fichiers sont conservés dans <code>lab-work/tp3/</code>. L'empreinte SHA-256 permet de vérifier leur intégrité après la séance.</p>
{table(
  ["Fichier", "Contenu", "SHA-256 (tronqué)"],
  [[f"<code>{esc(p.name)}</code>", desc, f"<code>{sha256(p)[:32]}…</code>"] for p, desc in [
    (TP / "captures/tp3_mtls.pcapng", "Capture de la session mTLS réussie"),
    (TP / "captures/tp3_mtls_refus.pcapng", "Capture du refus sans certificat"),
    (TP / "certs/esp01.crt", "Certificat client"),
    (EV / "cert_verify_client.txt", "Vérification OpenSSL du certificat client"),
    (EV / "mtls_subscriber.txt", "Télémétrie reçue en mTLS"),
    (EV / "broker_mtls_errors.txt", "Journal du refus sans certificat"),
    (EV / "cert_request.txt", "Certificate Request détaillé"),
    (EV / "client_cert_in_capture.txt", "Certificat client vu dans la capture"),
    (EV / "refus_evidence.txt", "Handshake et alerte du refus"),
  ]],
  widths=["30%", "44%", "26%"])}
<h2>B.3 Reproductibilité</h2>
<p>Les commandes complètes figurent aux sections 3 à 5 : génération du certificat client, ajout de <code>require_certificate true</code>
dans la configuration, puis exécution de <code>python3 esp8266_mtls_sim.py</code>. Arrêt : <code>docker rm -f tp3-broker</code>.
Les certificats et captures restent dans le répertoire du TP.</p>
</section>
"""

    out = Path(__file__).resolve().parent.parent / "TP3_Rapport_Authentification_Mutuelle_mTLS.pdf"
    render_pdf(body, out, "TP3 — Authentification mutuelle (mTLS) · Rapport de laboratoire · 17 nov. 2026", "TP3 — mTLS")
    return out


if __name__ == "__main__":
    print(build())
