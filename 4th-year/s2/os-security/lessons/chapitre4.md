

Sécurité des systèmes
d’exploitations
Chapitre 4 : Méthodes d’analyse et d’évaluation
de la sécurité des systèmes d’exploitation
2eme année second cycle : Cybersecurity
Dr. Manel BABA AHMED
## 1

Plan chapitre 4 :Méthodes d’analyse et évaluation de la
sécurité des OS
–Méthodes d’analyse de la sécurité des OS
–Méthodes d’évaluation de la sécurité des OS
- Analyse des vulnérabilités et le test d’intrusions
–Analyse des vulnérabilités : manuelle
–Analyse des vulnérabilités : automatique
–Test d’intrusion (pentesting)
- Audit de sécurité et analyse des logs
Analyse de logs de sécurité : étapes (selon IBM), ce qu’il faut analyser, types d’attaques détectable
- Système de détection d’intrusion : HIDS (basé sur l’hôte) : définition, Types des HIDS, composants et
capacités, Limites/avantages des HIDS, fausses idées sur les HIDS, cas d’utilisation d’un HIDS, HIDS/HIPS, HIDS
pour le cloud,
–Wazuh (SIEM & HIDS) : définition et fonctionnement, quelques fonctionnalités, cas d’usage, analyse du
manager, indexation, scénario, rules (règles), brute force
## 2

Méthodes d’analyse de la sécurité des OS
Objectif de l’analyse de sécurité
L’analyse de sécurité consiste à :
Identifier les vulnérabilités
Comprendre les menaces
Évaluer les mécanismes de protection
Détecter les failles exploitables
Autrement dit :
“Est-ce que mon système peut être attaqué ? Et comment ?”
## 3

Méthodes d’analyse de la sécurité des OS: analyse
statique
•On distingue deux grandes approches :analyse statiqueet analyse dynamique
•Analyse statique: analyse du système sans exécution de code (analyser ce qui existe déjà)
## Exemple :
–Analyse du code source
–Vérification des permissions voir qui a accès à quels fichiers
–Inspection des configurations vérifier si les paramètres sont sécurisés (sudo, ssh....)
## Avantages :
–Pas de risque pour le système (on exécute rien)
–Détection précoce des erreurs (avant l’exécution)
## Limites :
–Ne détecte pas les comportements en temps réel
## 4

Méthodes d’analyse de la sécurité des OS: types
d’analyse statique
- Analyse basée sur les vulnérabilités :trouver les failles connues
–Scan du système
–Comparaison avec bases de données de vulnérabilités (CVE)
–Outils : searchsploit, Lynis
–Voir si le kernel est vulnérable :searchsploit $(uname -r)
- Analyse des permissions et privilèges
–analyser : fichiers SUID, droits utilisateurs, groupes
–Exemple :find / -perm -4000 2>/dev/null :détecter les fichiers SUID dangereux
- Analyse des mauvaises configuration
–mauvais sudoers, PATH modifié, services ouverts inutilement
–Exemple :export PATH=.:$PATH: permet une attaque PATH hijacking
## 5

Méthodes d’analyse de la sécurité des OS :analyse
dynamique
•Analyse dynamique: analyse du système pendant le fonctionnement
Exemple:strace ls, top, htop
On observe :
–appels système (execve, open, etc.)
–accès mémoire
–comportement des processus
## Avantages :
–Détection des attaques réelles
–Observation du comportement
## Limites :
•Plus complexe car c’est au temps réel, volumineuse (stracepeut affiché plusieurs appels systèmes)
Remarque: l’analyse dynamique contient plusieurs types
## 6

Méthodes d’analyse de la sécurité des OSanalyse
dynamique
- Analyse des logs système :permet de détecter les traces d’attaque (journalctl)
–Exemple :journalctl -u ssh
–Détecter : connexions suspectes
- Analyse du comportement (approche comportementale) :observer ce que fait un programme
–Exemple : accès inhabituel à/etc/passwd,un script ou un programme qui ne devrait pas acceder a
passwd fera :open("/etc/passwd", O_RDONLY)
–création de processus anormaux
–Outils : strace, ltrace (appels aux bibliothèques)
## 7

Méthodes d’évaluation de la sécurité des OS
Objectif de l’évaluation
•Après l’analyse (trouver les failles), l’évaluation sert à :
•Mesurer le niveau de sécurité
•Estimer les risques
•Prioriser les corrections
•Vérifier l’efficacité des mécanismes de protection
Question : À quel point mon système est sécurisé ?”
Différence analyse/évaluation
## 8
AnalyseÉvaluation
Trouver les faillesMesurer leur impact
Observer et manipuler le systèmePrendre une décision/donner un jugement
Ex: détecter SUIDEx: est-ce critique ?

Méthodes d’évaluation de la sécurité des OS
a) Audit de sécurité :examen complet et structuré du système, Analyse sans attaquer
•Audit interne : vérifier ce qu’un utilisateur interne (ou attaquant déjà présent) peut faire
•Audit externe : voir ce qui est visible et exploitable depuis l’extérieur
•ce qu’on vérifie configurations, permissions, services, et mises à jour
Exemple:sudo lynis audit system
Question: Est-ce que le système est bien sécurisé ?
b) Test d’intrusion (Pentesting)
•Analyser et exploiter les vulnérabilités
•Vérifier si une attaque est possible
Question :est-ce que je peux compromettre ce système ?
Remarque :Le pentest ne s’arrête pas à analyser, il va jusqu’à prouver si le système est vulnérable ou
non
## 9

Méthodes d’évaluation de la sécurité des OS
## 10
CritèreAuditPentest
TypePassifActif
AttaqueNonOui
ObjectifTrouver les faillesExploiter les failles
RisqueAucunPeut impacter le système
RésultatRecommandationsPreuve d’attaque

Méthodes d’évaluation de la sécurité des OS
c) Évaluation des risques :le risque dépend de :Probabilité d’attaque Impact de l’attaque
Formule classique :Risque = Probabilite × ImpactRisque
Exemple : un serveur Linux présente les problèmes suivants : service SSH ouvert sur Internet, mot de
passe faible , aucun blocage après plusieurs tentatives
•Probabilité d’attaque accessible depuis Internet, attaque brute force facile, rendue facile par l’absence
de limitation des tentatives.Probabilité = 5/5 (très élevée)
•Impact de l’attaque si l’attaque réussit : accès au compte utilisateur, possibilité d’élévation de privilèges,
accès aux données sensibles,Impact = 4/5 (élevé) (ne contrôle pas tout)
Calcul du risque Risque = 5 × 4 = 20
•Interprétation 20 =RISQUE CRITIQUE =>ce problème doit être corrigé en priorité
## 11

Méthodes d’évaluation de la sécurité des OS
## 12
ValeurNiveauDescription (probabilité)
1Très faibleTrès difficile à attaquer (très sécurisé)
2FaiblePeu probable (accès limites, protections actives)
3MoyenPossible (quelques failles exploitables)
4ÉlevéFacile à attaquer (service exposé, faibles protections)
5Très élevéTrès facile
ValeurNiveauDescription (Impact)
1NégligeableAucun effet important
2FaibleImpact limité (petit service affecté)
3MoyenImpact sur un service ou utilisateur
4ÉlevéImpact important (plusieurs services)
5CritiqueContrôle total (ex : root, perte de données)
ScoreNiveau de risque
1 – 5Faible
6 – 10Moyen
11 – 15Élevé
16 – 25Critique
Probabilité = facilité d’attaque
si c’est très difficile → 1 ou 2
si c’est possible → 3
si c’est facile → 4 ou 5
Impact = gravité des conséquences
si les conséquences sont faibles → 1 ou 2
si elles sont moyennes → 3
si elles sont graves → 4
si c’est catastrophique (contrôle total) → 5

Méthodes d’évaluation de la sécurité des OS
d) Évaluation des mécanismes de sécurité :vérifier si les protections fonctionnent
•Exemples : ASLR activé ?, Pare-feu actif ?
e) Conformité et standards :vérifier si le système respecte des normes :
–CIS Benchmarksensemble de recommandations techniques qui indiquent comment configurer un
système de manière sécurisée (Linux, Windows, réseaux...).
–politiques internesrègles définies par l’organisation pour encadrer la sécurité (mots de passe, accès,
sauvegardes...), adaptées à ses propres besoins et contraintes.
Objectif : garantir un niveau de sécurité reconnu
f) Évaluation continue (monitoring) :la sécurité n’est pas statique
Outils :Wazuh (HIDS), auditd, SIEM (Security Information and Event Management)
Permet : détection en temps réel et alertes
## 13

Analyse des vulnérabilités : manuelle
Analyse des comptes utilisateurs :vérifier les comptes existants, identifier les comptes inutiles ou
suspects
Analyse des fichiers sensibles :examiner les fichiers contenant des informations critiques et qui peut
accéder a ces fichiers
Vérification des permissions :contrôler les droits d’accès (lecture, écriture, exécution)
Recherche de configurations dangereuses :identifier des programmes avec privilèges élevés
Analyse des services et applications :identifier les services actifs
Analyse des journaux (logs) :examiner les connexions, détecter des tentatives d’accès suspectes
## 14

Analyse des vulnérabilités : automatique
- Lynisun outil d’audit de sécurité pour les systèmes Linux et Unix
•Il analyse automatiquement la machine
•Analyse le système, comptes utilisateurs, permissions des fichiers, services actifs, configuration
réseaux..... etc
•Il détecte les vulnérabilités et mauvaises configurations
•Il aide à améliorer la sécurité
ObjectifRépondre à la question :Est-cequemonsystèmeestbiensécurisé?”
•Lynis fournit : des avertissements (warnings) et des suggestions (recommandations)
## Limites :
–ne réalise pas d’attaque
–ne prouve pas l’exploitation
–nécessite une interprétation
## 15

## 16
Catégorie (Lynis)Explication simple
Initializing programDémarrage de Lynis : préparation de l’audit (vérifie l’environnement et les droits)
System toolsVérifie la présence des outils Linux nécessaires (ps, grep, etc.)
Debian testsTests propres aux systèmes Debian/Ubuntu (mises à jour, dépôts)
Boot and servicesAnalyse du démarrage et des services actifs (systemd)
KernelVérifie le noyau Linux (version, sécurité, vulnérabilités)
Memory and processesAnalyse mémoire + processus (processus suspects, protections mémoire)
Users, groups and authenticationComptes utilisateurs, groupes, mots de passe, authentification
ShellsVérifie les shells disponibles et leur configuration
File systemsAnalyse des systèmes de fichiers et options de montage (noexec, nosuid...)
USB devicesVérifie les périphériques USB (risque d’accès non autorisé)
StorageAnalyse du stockage (disques, partitions, chiffrement)
Ports and packagesPorts ouverts + paquets installés (logiciels vulnérables)
NetworkingConfiguration réseau (interfaces, firewall, services réseau)
Printers and spoolsServices d’impression (peu utilisés mais parfois vulnérables)

Analyse des vulnérabilités : automatique
## 17
TypeSignification
WarningsProblèmes importants à corriger (risque réel de sécurité)
SuggestionsAméliorations recommandées (bonnes pratiques)
SoftwareVérifie les logiciels installés et leurs versions
SSH supportAnalyse de la configuration SSH (port, root login, sécurité)
Logging and filesVérifie les logs système (journalisation activée ou non)
Insecure servicesDétecte les services non sécurisés (ex: telnet, ftp)
CryptographyVérifie les mécanismes de chiffrement utilisés
Security frameworks
Analyse des protections (AppArmor : control ce qu’un programme ne peut
faire)
File permissionsVérifie les droits des fichiers sensibles
Kernel hardeningVérifie le renforcement du kernel (ASLR, protections mémoire)

Analyse des vulnérabilités : automatique
- linPEAS: outil de pentesting automatique orienté exploitation, linPEAS analyse automatiquement
plusieurs éléments du système :
## 1.
Informations système : version du noyau (kernel), distribution Linux architecture
## 2.
Utilisateurs et privilèges : utilisateurs présents, groupes sudo mal configuré
3.Permissions dangereuses : fichiers SUID/SGID, fichiers accessibles en écriture, dossiers sensibles mal
protégés
4.Tâches planifiées : cron jobs scripts exécutés automatiquement
## 5.
Variables d’environnement : PATH dangereux (PATH Hijacking), LD_PRELOAD exploitable
6.Services et processus : services vulnérables, programmes lancés avec privilèges élevés
7.Recherche de vulnérabilités : comparaison kernel ↔ CVE connus
## 18

Analyse des vulnérabilités : automatique
linPEAS :
–cherche des failles exploitables
–il propose des attaques possibles
–il aide à compromettre le système
Quelques limites :
–beaucoup d’informations
–nécessite une analyse humaine
–ne fait pas l’attaque lui-même (il suggère)
Différence Lynis/LinPEAS
## 19
OutilRésultat / Vision
LynisLe fichier est mal protégé” , Il faut corriger les permissions”
LinPEASCe fichier est exploitable” , “Tu peux devenir root avec ça”

Remarque : LinPEAS ne génère pas de Rapport de pentest, il existe d’autre outils pour ca Nessus,
OpenVAS
## 20
PartieObjectif sécuritéMoment exploitationExemple
Utilisateurs & privilègesvoir qui peut devenir rootsi user dans sudo groupescalade privilèges
## SUDO
commandes exécutables en
root
si NOPASSWDsudo vim → shell root
Processus & services
détecter services
exploitables
script root modifiableinjection code
Cron jobsexécution automatiquescript cron writableecho "bash" >> script.sh
Fichiers & permissions
détecter erreurs de
configuration
fichier root writablemodification fichier
SUIDexécution en rootSUID dangereuxfind → shell root
Variables d’environnementattaques indirectesPATH writablePATH hijacking
Protections systèmeniveau de sécuritéprotections désactivéesexploitation facilitée

Le test d’intrusion : Pentesting
Test d’intrusion: exploiter les failles pour prouver leur impact
- Reconnaissance (Analyse)collecter des informations sur la machine cible
- Scan et énumérationIdentifier les points faibles services actifs versions vulnérables comptes
utilisateurs
- ExploitationLancer des attaques brute force exploitation de vulnérabilités, injection , objectif :obtenir
un accès
- Élévation de privilègesPasser d’un utilisateur normal à root exploitation SUID mauvaise
configuration sudo PATH hijacking
- Maintien d’accès (optionnel)Garder l’accès au système création d’utilisateur backdoor
- Rapport (très important)vulnérabilités trouvées, impact, recommandations
## 21

Le test d’intrusion : Pentesting
•Types du pentesting :
- Pentest externe :
–voir ce qui est visible de l’extérieur, services exposés par exemple, sans accès au départ
–consiste à simuler une attaque depuis Internet afin de vérifier si un attaquant peut accéder au système
sans disposer d’aucun accès préalable.
- Pentest interne :
–un test d’intrusion réalisé depuis l’intérieur du réseau avec un accès utilisateur
## 22

Le test d’intrusion : Pentesting (rapport)
- Informations générales:
–Client : Entreprise X
–Type de test : Test d’intrusion interne
–Périmètre : Machine Linux (192.168.1.10)
–Date : 10 Avril 2026
–Équipe : Pentester
- Objectif :évaluer le niveau de sécurité du système cible en simulant une attaque réelle afin d’identifier
les vulnérabilités exploitables et mesurer leur impact.
- Méthodologie :le test a été réalisé selon les étapes suivantes :
–Phase de reconnaissance
–Scan et identification des services
–Exploitation des vulnérabilités
–Élévation de privilèges
–Analyse des impacts
## 23

Le test d’intrusion : Pentesting (rapport)
- Résumé exécutif :le test a permis d’identifier plusieurs vulnérabilités critiques permettant à un
attaquant d’obtenir un accès non autorisé au système et d’élever ses privilèges jusqu’au niveau
administrateur.
•Le niveau de risque global est évalué comme :Élevé
- Résultats détaillés
Vulnérabilité 1 : Authentification faible
–Description : Utilisation de mots de passe faibles
–Impact : Accès non autorisé au système
–Preuve : Accès utilisateur obtenu
–Niveau : Critique
## 24

Le test d’intrusion : Pentesting (rapport)
Vulnérabilité 2 : Mauvaise configuration sudo
–Description : Exécution de commandes avec privilèges élevés sans authentification
–Impact : Élévation de privilèges
–Preuve : Accès root obtenu
–Niveau : Critique
Vulnérabilité 3 : Permissions incorrectes
–Description : Fichier sensible accessible en lecture
–Impact : Divulgation d’informations
–Niveau : Moyen
- Exploitation :les actions suivantes ont été réalisées avec succès :
–Accès initial obtenu via authentification faible
–Escalade de privilèges via mauvaise configuration sudo
–Accès complet au système (root)
## 25

Le test d’intrusion : Pentesting (rapport)
- Impact :un attaquant pourrait :
–accéder aux données sensibles
–modifier le système
–installer des logiciels malveillants
–compromettre l’intégrité du système
## 8. Recommandations
–Mettre en place des mots de passe robustes
–Corriger la configuration sudo
–Restreindre les permissions des fichiers sensibles
–Mettre à jour le système
–Désactiver les services inutiles
- Conclusion :le test d’intrusion a démontré que le système présente des vulnérabilités critiques
permettant une compromission complète. Une correction immédiate est recommandée afin de réduire les
risques de sécurité.
## 26

Analyse des Logs de sécurité : types(selon IBM)
Logs d’accès (Access logs)enregistrent : les adresses IP et les requêtes utilisateurs (pages web)
•Suivre le comportement des utilisateurs
•Détecter des activités suspectes (ex : brute force)
Logs d’erreurs (Error logs)contiennent les erreurs système ou applicatives, aide a :
–Identifier des incidents de sécurité : repérer des comportements suspects
–Aider au dépannage : comprendre pourquoi un service ne fonctionne pas et corriger le problème (crash)
–Réduire les pannes futures
Logs d’événements (Event logs)enregistrent : démarrage / arrêt du système, connexions /
déconnexions, modifications de configuration
•Comprendre ce qui s’est passé sur le système
•Analyser une attaque après incident (forensics)(comment l’attaque a eu lieu, qui est le responsable...etc)
## 27

Analyse des Logs de sécurité : étapes(selon IBM)
- Collecte des données (Data collection) :récupération des logs depuis :
## –serveurs
## –applications
–équipements réseau
2.Traitement des données (Data processing)transformation des logs bruts rendre les logs structurés
et exploitables
–indexation (recherche rapide)
–normalisation (parsing) (format structuré des logs), ex : JSON)
–organisation selon : date (timestamp), source, type d’événement
- Analyse des données (Data analysis)Recherche :
## –anomalies
–causes de panne
–activités suspectes
•Aujourd’hui : utilisation de l’IA pour détecter des patterns
## 28

Analyse des Logs de sécurité : étapes(selon IBM)
- Visualisation des données (Data visualization) :présentation via :
–tableaux de bord (dashboards)
Permet de voir :
–état du système en temps réel
–métriques (CPU, réseau, etc.)
## Objectif :
–faciliter la prise de décision rapide
## 29

Analyse des Logs de sécurité : ce qu’il faut analyser
## Exemple :
Les éléments clés
–Timestamp → quand ?
–Utilisateur → qui ?
–IP source → d’où ?
–Action → quoi ?
–Résultat → succès ou échec ?
Apr 10 10:20 sshd[1234]: Failed password for root from 192.168.1.10
## Analyse :
–Date : Apr 10
–Service : SSH
–Action : login
–Résultat : échec
–IP : suspecte
## 30

Analyse des Logs de sécurité : types d’attaques
détectable
•Brute force
Failed password for root
Failed password for root
Failed password for root
•Scan réseau / reconnaissance : lecture de fichiers sensibles
GET /.env -> contient souvent les mot de passes
GET /config.php -> configuration du site
GET /db.sql -> base de données
•Élévation de privilèges
sudo: user1 : command not allowed
•Malware / comportement anormal
Unknown process started
## 31

Système de détection d’intrusion (IDS)
HIDS (Host-based IDS)installé sur une machine spécifique
•Analyse : logs système, fichiers, activités locales
•Exemples :OSSEC, Wazuh
NIDS (Network-based IDS)placé sur le réseau (switch, routeur) ou autre
•Analyse : paquets réseau, trafic entrant/sortant
•Exemple :Snort, Suricata
IDS basé sur les signatures (Signature-based)compare les activités avec une base de signatures
connues
IDS basé sur les anomalies (Anomaly-based)détecte les comportements anormaux
•Utilise : statistiques, machine learning
IDS hybrideCombine : signatures + anomalies
Application-based IDS (ABIDS) :surveille une application spécifique
Hybrid IDS (HIDS + NIDS) :combine : surveillance réseau + machines
## 32

Système de détection d’intrusion (IDS): Definition
•Un HIDS (Host-Based Intrusion Detection System)surveille un système (serveur, PC...)
en collectant et analysant différentes données pour détecter des activités suspectes
ou anormales. Il s’appuie sur plusieurs sources comme les journaux d’authentification,
système et applicatifs.
•Même si certains logs ne sont pas directement liés à la sécurité, des comportements
inhabituels peuvent révéler une attaque
•Pour être efficace, le HIDS corrèle plusieurs sources de données (réseau +
application + système) afin de mieux comprendre le contexte. Cela permet de
distinguer :
–une simple tentative d’attaque
–d’une compromission réelle du système
## 33

Système de détection d’intrusion (IDS): Types des
## HIDS
•HIDS basé sur un agent :
•Ce type de HIDS utilise un agent logiciel installé sur chaque hôte pour collecter les informations locales.
Il offre une surveillance détaillée, mais consomme davantage de ressources système.
•HIDS sans agent ‘’Agentless ‘’
•C’est une méthode de surveillance où aucun logiciel n’est installé sur les machines. le système de
sécurité (ex : HIDS) récupère les informations à distance en utilisant :des connexions réseau (SSH) ou
des APIs (interfaces qui permettent d’interroger un système ou un service) Cette approche consomme
moins de ressources, mais elle est souvent plus complexe à mettre en place et peut donner accès à
moins de données.
## 34

Système de détection d’intrusion (IDS):
Composants/capacités d’un HIDS
Un HIDS repose généralement sur troiscomposantsprincipaux :
•Collecte de données: des agents (ou sans agent) récupèrent les informations depuis les hôtes.
•Stockage: les données sont centralisées et conservées pour analyse et éventuellement pour
consultation ultérieure.
•Moteur d’analyse: il traite les données afin de détecter des anomalies ou comportements suspects liés
à des attaques.
Un HIDS dispose de troiscapacitésprincipales après la détection d’une menace :
•Alerte: il informe les équipes de sécurité des incidents détectés, en indiquant leur niveau de gravité
(faible, moyen, élevé).
•Rapports: il génère des rapports sur l’état de sécurité (types d’attaques, évolution dans le temps,
comparaison entre systèmes).
•Réponse: il peut réagir automatiquement, par exemple en bloquant une adresse IP ou en appliquant
des règles de sécurité.
## 35

Système de détection d’intrusion (IDS):
Limites/avantages d’un HIDS
## 36
AvantagesInconvénients
surveille les logs, les modifications de certain fichiers et
les tentatives d’accès.
Portée limitée ne surveille que l’hôte sur lequel il
est installé, sans détecter les attaques multi-
systèmes.
Utilise une détection comportementale pour identifier
des activités suspectes au-delà des signatures connues.
Génère un grand volume d’alertes, entraînant des
faux positifs et une fatigue des alertes.
Permet de détecter précocement des signes de
compromission avant que les menaces ne se propagent.
Peut entraîner une baisse des performances des
machines si mal configuré.

Système de détection d’intrusion (IDS): Fausses idées
sur les HIDS
## 37
•Un HIDS empêche les attaquesFaux
Le HIDS détecte, mais ne bloque pas.
Le blocage nécessite un HIPS (système de
prévention).
•Un HIDS peut fonctionner seulFaux
Utilisé seul, il laisse des failles.
Il faut aussi : un NIDS pour le réseau
des solutions de sécurité cloud (ex : email)
•Le HIDS est comme un antivirusFaux
Ce sont des outils différents :
Antivirus → détecte les signatures de malware
HIDS → surveille les logs et les fichiers
•Le HIDS se déploie facilement à grande échelle
## Faux
Plus il y a d’hôtes :plus la charge augmente , plus
les alertes se multiplient
Résultat :beaucoup de faux positifs, fatigue des
alertes (problème majeur dans les SOC)

Système de détection d’intrusion (IDS): Cas
d’utilisation d’un HIDS
•Surveillance de l’intégrité des fichiers (FIM) File Intergrity Monitoring (mécanisme de surveillance)
Surveille les fichiers critiques pour détecter toute modification. C’est le moyen le plus simple de savoir si
un fichier a été altéré/etc/passwd
•Analyse des logs
L’analyse des journaux permet de détecter des comportements anormaux. Elle aide à reconstituer une
attaque dans le temps (forensics).
•Détection comportementale
Se base sur le comportement normal des processus. Si un comportement devient anormal → alerte
•Détection par signature
Comparaison avec des modèles d’attaques connus
## 38

Système de détection d’intrusion (IDS): HIDS/HIPS
HIPS (Host-Based Intrusion Prevention System)
–agit en temps réel, Il bloque :
–comportements malveillants
–trafic suspect
–activités anormales
## Inconvénient :
•peut impacter les performances de la machine
Intercepte et surveille tout
HIDS (Host-Based Intrusion Detection System)
n’intervient pas, il observe, il surveille :
## –logs
–modifications de fichiers
–tentatives d’accès
## 39

Système de détection d’intrusion (IDS): HIDS pour le
## Cloud
Le HIDS est efficace au niveau des postes (endpoints), mais dans le cloud et les emails, ses limites
apparaissent.
•Surcharge de données :les e-mails dans le cloud génèrent un volume énorme de données, le HIDS peut
être submergé : beaucoup de faux positifs , difficulté à distinguer les vraies alertes du bruit
•Déploiement complexe :installer un HIDS dans des environnements cloud est difficile, cela nécessite
des configurations spécifiques
•Menaces adaptatives :les attaques modernes par e-mail utilisent : l’intelligence artificielle, des
techniques d’usurpation d’identité (liens vers site frauduleux), elles ne reposent plus uniquement sur
des malwares (détectable par signature), un HIDS ne les détecte pas toujours
Aretenir:HIDSestefficacesurlesmachineslocales,maislimitédanslecloudetlesemails
## 40

Wazuh (SIEM & HIDS): Définition et fonctionnement
•Wazuh est une plateforme Open Source de sécurité qui permet de :
–détecter les menaces
–surveiller les systèmes
–analyser les logs
–répondre aux incidents
•C’est à la fois :
–un HIDS (détection au niveau des hôtes)
–un SIEM (analyse centralisée des logs)
•Wazuh utilise :
–Agents → installés sur les machines
–Serveur (Manager) → analyse les données
–Dashboard → visualisation des alertes
•Les agents : collectent les logs, surveillent les fichiers, et détectent les anomalies
## 41

Wazuh (SIEM & HIDS): Quelques fonctionnalités
## 42
Security Monitoring (Surveillance de sécurité)
Wazuh collecte et analyse les données de sécurité
provenant des endpoints
permet de détecter les activités suspectes en temps
réel
Log Data Analysis (Analyse des logs)
Centralisation et analyse des journaux
corrélation des événements pour identifier les
incidents
File Integrity Monitoring (FIM)
Surveillance des modifications de fichiers critiques
détection des changements non autorisés (altération
système)
## Vulnerability Detection
Détection des vulnérabilités connues (CVE)
comparaison des systèmes avec des bases de
données de failles
Security Configuration Assessment (SCA)
Vérification de la conformité des systèmes
(exemple, mot de passe avec longueur de 12)
Threat Detection (Détection des menaces)
Analyse des comportements suspects
détection d’activités malveillantes ou anomalies
Incident Response (Réponse aux incidents)
Actions automatiques ou manuelles :
blocage d’IP
désactivation de comptes
## Cloud Security Monitoring
Surveillance des environnements cloud
collecte et analyse des logs

Wazuh (SIEM & HIDS): Cas d’usage
- Collecte des données : Les agents récupèrent les logs, événements système et activités des machines
- Envoi au Manager: Les données sont envoyées au serveur central Wazuh pour traitement
## 3. Analyse
: Le Manager applique des règles pour détecter anomalies et attaques
## 4. Stockage
: Les données sont stockées dans l’Indexer (OpenSearch) pour recherche et historique
- Génération d’alertes: Une alerte est créée si une activité suspecte est détectée
- Visualisation : Le Dashboard affiche les alertes, logs et statistiques
- Réponse : Wazuh peut bloquer ou réagir automatiquement à une attaque
## 43

Wazuh (SIEM & HIDS): Analyse du manager
•Décodage: transformer le log brut en infos
–Exemple :Failed password for root from 192.168.1.10
–Wazuh extrait :utilisateur = root, IP = 192.168.1.10, action = échec login
•Normalisation :mettre dans un format standard
–Exemple :Tous les logs deviennent :type=auth_failure user=root src_ip=192.168.1.10
•Application des règles :détecter comportement suspect
–Exemple : Règle :“si échec login SSH”
–Wazuh déclenche une alerte niveau faible
•Corrélation :relier plusieurs événements
–Exemple : 10 échecs login depuis la même IP
–Wazuh détecte une attaque brute force
## 44

Wazuh (SIEM & HIDS): Indexation
L’indexer (OpenSearch : un moteur spécialisé pour gérer les logs) sert à :
–stocker les logs (événements de sécurité)
–indexer les données (les organiser pour recherche rapide)
–permettre les requêtes (ex: trouver toutes les attaques SSH)
L’indexer ne stocke pas “comme un fichier classique”, mais sous forme de :
- Index = base de données (ex: wazuh-alerts-2026.04.19)
- Documents = chaque log = 1 enregistrement (JSON)
- Champs = attributs du log (IP, user, action...)
## 45

Wazuh (SIEM & HIDS): Scénario
Sur la machine agent (Kali), une attaque brute force SSH est détectée.
L’agent envoie un log en texte brute au serveur Wazuh Manager, et celui ci le transforme en JSON :
## {
"timestamp": "2026-04-19T10:30:00",
## "agent.name": "kali",
"rule.id": "5710",//échecs d’authentification SSH
"rule.description": "Multiple SSH authentication failures",
## "srcip": "192.168.1.100",
## "user": "root",
"event": "failed login",
## "level": 12
## }
## 46

Wazuh (SIEM & HIDS): Scénario
Traitement par le Manager :le Manager fait plusieurs choses :
•Analyse du log (décodage + règles)
•Associe une règle (rule.id = 5710)
•Détermine la gravité (level = 12 → critique)
•Wazuh comprend :attaquebruteforceSSHdétectée
Action automatique (optionnelle) :si on a configuré une action (comme firewall-drop ou disable
account) :
•Blocage de l’IP 192.168.1.100
•Désactivation du user root (selon config)
•Sinon : Il passe juste à l’étape suivante (stockage)
## 47

Wazuh (SIEM & HIDS): Scénario
L’indexer :le Manager envoie le log (JSON) vers l’indexer
•L’indexer : Stocke le log comme document JSON
•Dans un index :wazuh-alerts-2026.04.19
•Indexe les champs : srcip, user, rule.description, level
Visualisation dans le Dashboard
•Le Dashboard Wazuh interroge l’indexer :
•Exemples :“toutes les attaques SSH”, “toutes les alertes level > 10”
•Résultat affiché :Alerte critique ; IP attaquante : 192.168.1.100, utilisateur ciblé : root
## 48

Wazuh (SIEM & HIDS): Rules (règles)
•Une règle = SI je vois ce comportement → ALORS alerte”
•Exemple simple :SI quelqu’un échoue 5 fois à se connecter en SSH ALORS alerte brute force
•Wazuh utilise des fichiersXMLpour définir ces règles.
•Exemple :
<rule id="100001" level="10">
## <if_sid>5710</if_sid>
<match>Failed password</match>
<description>Détection tentative brute force SSH</description>
## </rule>
•<rule id="100001" level="10"> id = identifiant unique
•<if_sid>5710</if_sid> se base sur une règle existante (log SSH détecté)
•<match>Failed password</match> cherche ce texte dans les logs
•<description> message affiché dans Wazuh
## 49

Wazuh (SIEM & HIDS): Brute force
•Simulation d’une attaque depuis Kali :
hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.10
•Vérifier les logs pour la machine victime avecsudo journalctl -u ssh
•Resultats :Failed password for root from 192.168.1.20 port 22 ssh2
•Ajouter une regle wazuh dans :
sudo nano /var/ossec/etc/rules/local_rules.xml
•Ajouter :
<group name="ssh,bruteforce">
<rule id="100002" level="12" frequency="5" timeframe="60">
## <if_matched_sid>5710</if_matched_sid>
<same_source_ip /> //si la regle se produit plusieurs fois depuis la même
## IP
<description>Brute force SSH détecté depuis une même IP</description>
## </rule>
## </group>
## 50

Wazuh (SIEM & HIDS): Brute force
•Après ajoutsudo systemctl restart wazuh-manager
•Lancer hydra
•Ensuite vérifier les logs dansjournalctl
•Résultats attendu :Brute force SSH détecté depuis une même IP
•Ajout d’une action :sudo nano /var/ossec/etc/ossec.conf
## <active-response>
## <command>firewall-drop</command>
## <location>local</location>
## <rules_id>100002</rules_id>
## <timeout>600</timeout>  //secondes
## </active-response>
•Vérifier que la commande existe :ls /var/ossec/active-response/bin/
•Résultat attendu :firewall-drop
•Redémarrer wazuh :sudo systemctl restart wazuh-manager
•Relancer l’attaque avec hydra, verifier les logs avec journalctl
## 51

Wazuh (SIEM & HIDS): Brute force
•Vérifier dans le firewall :sudo iptables -L -n // afficher les regles du parfeu
•Résultats attendu : l’IP de l’attaquant bloqué
## Travailafairesurwazuh
•Wazuhdoit unetentatived’escaladedeprivilègesvial’utilisationdesudo.
•Aprèsavoirgénérédeslogsenexécutantunecommandecommesudovim,vousdevezcréerunerègle
## Wazuhpermettantd’identifiercecomportementsuspect.
•Ensuite,configurezuneactionautomatique(disable-account)afindedésactiverl’utilisateurconcerné.
•RedémarrezWazuh,lancezl’attaque,puisvérifiezlesalertesdansleslogsainsiqueladésactivation
effectiveducompteutilisateur.
## 52