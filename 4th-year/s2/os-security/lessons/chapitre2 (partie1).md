

Sécurité des systèmes
d’exploitations
Chapitre 2 : Les attaques sur les systèmes
d’exploitations (partie 1)
2eme année second cycle : Cybersecurity
Dr. Manel BABA AHMED
## 1

Plan chapitre 2
Malwares et exploits
Élévation de privilèges et rootkits
Attaques par déni de service (DoS) et attaques par force brute
## 2

Malwares dans les systèmes d’exploitations
Botnetsmachines infectées contrôlées à distance, exploitées pour DDoS, attaques coordonnées
RAT (Remote Access Trojans)contrôle distant complet du système, accès aux fichiers, processus, périphériques,
très utilisés pour l’espionnage
Backdoors: créent un accès caché au système, contournent l’authentification, persistent après redémarrage
Kernel Rootkits: modifient directement le noyau, altèrent les appels système, désactivent les mécanismes de
sécurité
Bootkits: infectent le bootloader, s’exécutent avant le système d’exploitation, très difficiles à détecter
Rootkitsse cachent dans le système masquent fichiers, processus (peuvent agir a différents niveaux)
Logic Bombs: se déclenchent sous conditions (date, événement) peuvent viser le système de fichiers ou les services
Screenloggers: interceptent les appels aux API graphiques, prennent des captures régulières de l’écran,
Wipers: ciblent souvent les partitions système
Scarewaref: fausse alerte système, manipule l’utilisateur pour installer d’autres malwares
Fileless Malware: réside en mémoire physique uniquement, exploite les processus légitimes, très difficile à détecter
## .......etc
## 3

Malwares de démarrage : attaques contre le BIOS et
l’UEFI
•LeBIOS(Basic Input/Output System) et son successeur l’UEFI(Unified Extensible Firmware Interface)
•Constituent la première couche logicielle exécutée lors du démarrage d’un ordinateur.
•Toute compromission à ce niveau est critique, car elle s’exécute avant le système d’exploitation
•Échappe souvent aux antivirus et persiste même après un formatage du disque.
–Le BIOS/UEFI est stocké dans une mémoire flash sur la carte mère, pas sur le disque dur.
–Antivirus est installé sur le disque
–Système d’exploitation est installé sur le disque
–BIOS/UEFI est une  puce dédiée sur la carte mère
–Un formatage ne règle pas ce problème, BIOS/UEFI se trouve sur une puce SPI
(Serial Peripheral Interface) Flash
–Le malware est toujours là,  il réinfecte le système au prochain boot
Une mémoire flash : signifie qu’elle peut être écrite/réécrite
## 4

Malwares de démarrage : attaques contre le BIOS et
l’UEFI
Attaques de persistance (Firmware Rootkits)
les firmware rootkits consistent à injecter du code malveillant directement dans le firmware BIOS/UEFI
stocké dans la mémoire flash (SPI). Le malware devient alors persistant et se charge à chaque démarrage.
## Caractéristiques
–Persistance après réinstallation de l’OS
–Indépendance du disque dur
–Très difficile à détecter
## Exemples
–LoJax
–MosaicRegressor
## Impact
–Contrôle durable du système, espionnage, installation d’autres malwares...etc
## 5

Malwares de démarrage : attaques contre le BIOS et
l’UEFI
Attaques de la chaîne de démarrage (Bootkits)
Les bootkits infectent les composants de démarrage (MBR, VBR(volume boot recordou bootloader) afin
d’exécuter du code malveillant avant le chargement du noyau du système d’exploitation.
## Caractéristiques
–Exécution avant l’OS
–Capacité à contourner certaines protections de sécurité
## Exemples
–Stoned Bootkit
–Rovnix
## Impact
–Vol d’informations, élévation de privilèges, furtivité accrue (capacité renforcée à rester invisible)
## 6

Malwares de démarrage : attaques contre le BIOS et
l’UEFI
Attaques de la chaîne de démarrage (Bootkits)
Bootloader (GRUB, Windows Boot Manager)cible bootmgr, grubx64.efi, winload.efi
## Technique
•Patch du bootloader (alterer le code d’amorçage)
•Hook du chargement du noyau :  Intercepter le moment précis où le noyau est chargé en mémoire, afin
de modifier certains paramètres, injecter un module,  surveiller ou altérer le comportement du noyau
## Effet
•Injection d’un rootkit noyau
•Bypass de certaines protections (PatchGuard...)
## Exemple
•Rovnix
•BlackLotus (phase bootloader)
## 7

Malwares de démarrage : attaques contre le BIOS et
l’UEFI
Attaques de la chaîne de démarrage (Bootkits)
UEFI firmware (les pires) cible SPI Flash (puce du firmware)
## Technique
•Injection de code dans le firmware
Malware survit à :
•formatage disque
•changement d’OS et remplacement disque
## Effet
•Contrôle total du boot et recréation automatique du malware sur le disque
## Exemples
•LoJax
•CosmicStrand
Remarque: c’est le niveau ultime ou extrême de persistance
## 8

Malwares de démarrage : attaques contre le BIOS et
l’UEFI
Attaques par reflashage du BIOS :
réécrire (flasher) le firmware stocké dans la puce SPI Flash de la carte mère ces attaques remplacent le
firmware légitime par une version modifiée ou malveillante, en exploitant une absence de protection lors
de la mise à jour du BIOS.
Causes fréquentes :
•Firmware non signé
•Protection d’écriture SPI absente
•Mise à jour BIOS autorisée depuis un OS compromis
## Impact
•Compromission complète et persistante de la machine
## 9

Malwares de démarrage : attaques contre le BIOS et
l’UEFI
Attaques contre Secure Boot
secure Boot est un mécanisme UEFI qui vérifie la signature cryptographique des composants de
démarrage, les attaquants cherchent à le contourner pour charger du code non autorisé.
## Techniques
•Mauvaise gestion des clés UEFI (clés non fiables)
•Attaques par downgrade (Secure Boot bloque les bootloaders non signés (code non authentique ou non
legitime), l’attaquant installe une ancienne version signée, cette version contient une vulnérabilité, et
donc chargement de code non autorisé)
## Exemple
•BootHole (GRUB2)
## Impact
•Chargement d’un OS ou noyau modifié malgré Secure Boot.
## 10

Malwares de démarrage : attaques contre le BIOS et
l’UEFI
Attaques par mauvaise configuration du BIOS
une configuration BIOS non sécurisée facilite les attaques sans exploitation de vulnérabilité logicielle.
## Exemples
•Démarrage autorisé sur USB/CD
•Mot de passe BIOS absent
•Secure Boot désactivé
## Impact
•Démarrage d’un système d’exploitation ou outil malveillant
## 11

Malwares de démarrage : attaques contre le BIOS et
l’UEFI
Attaques via périphériques DMA (Direct Memory Access) :
certains périphériques(Thunderbolt jusqu’à 40 Gb/s pour Thunderbolt 3 et 4 utilise le connecteur USB-C)
permettent un accès direct à la mémoire (DMA), un attaquant peut exploiter cette fonctionnalité pour
contourner les protections.
## Exemples
•Attaques DMA viaThunderbolt: un attaquant branche un appareil malveillant et lit ou écrit directement
dans la RAM (vol de clés BitLocker, injection de code, etc.).
Remarque :Kernel DMA Protection limite fortement ça.
•Les périphériquesThunderboltpeuvent accéder à la RAM sans passer par le CPU
•Utile pour la performance, dangereux pour la sécurité
•Si un périphérique malveillant est branché, il peut lire ou modifier la mémoire du PC → attaque DMA
## 12

Malwares de démarrage : attaques contre le BIOS et
l’UEFI
Attaques via périphériques DMA (Direct Memory Access) :
scénario
•L'attaquant branche un petit boîtier malveillant (exemple Raspberry Pi modifié(logiciel volontairement
modifié)) sur le portThunderbolt.
•Le boîtier demande l'accès DMA (souvent accepté automatiquement ou après une vulnérabilité).
•Il lit directement la RAM :
–Récupère la clé de chiffrement du disque (même si le disque est chiffré).
–Lit les mots de passe en mémoire.
–Peut créer une backdoor ou supprimer le mot de passe de session.
–L'opération prend souvent moins de 5 à10 minutes et peut se faire sur un ordinateur verrouillé ou en
veille.
## 13

Malwares de démarrage : attaques contre le BIOS et
l’UEFI (quelques solutions)
Mise à jour BIOS (une version ancienne peut contenir des vulnérabilités) ou flasher le BIOS
Désactiver CSM (Compatibility Support Module) = mode de compatibilité ancien (Legacy BIOS). Il
permet de booter sur des disques MBR et du code non signé.
En UEFI pur (CSM désactivé), le système n’accepte que le mode UEFI moderne + partition GPT. C’est
obligatoire pour queSecure Bootfonctionne vraiment.
ActiverSecure Bootvérifie la signature numérique de tout ce qui s’exécute avant le système
d’exploitation (bootloader, pilotes UEFI, kernel).
Mettre mot de passe BIOS :un mot de passe fort sur le BIOS empêche qui conque ayant accès physique à
la machine de rentrer dans les réglages pour : désactiver Secure Boot, activer legacy, changer l’ordre de
boot
Restreindre les périphériques de boot désactiver le boot sur USB, carte SD, réseau, tant qu’on les utilise
pas, activer Kernel DMA Protection ou Pre-boot DMA protection
## 14

## Lesexploitsciblantlessystèmesd’exploitation
Exploits liés à la mémoire
•Buffer Overflowtrès fréquent dans les programmes système écrits en C/C++
•Stack OverflowExploitation de la pile d’exécution, modification du flot d’exécution du programme (appels recursifs)
•Heap OverflowExploitation du tas (heap), affecte l’allocation dynamique mémoire
•Use-After-FreeUtilisation d’une zone mémoire déjà libérée peut mener à une exécution de code arbitraire
•Double FreeLibération multiple d’une même zone mémoire, corruption du gestionnaire mémoire (si aucune
vérification bloc ajouté deux fois dans liste des espaces libres, deux pointeurs peuvent pointer vers la même zone de
mémoire après)
Exploits liés aux privilèges
•Privilege Escalation ExploitsPassage de utilisateur normal → administrateur/root cible souvent le noyau ou les
pilotes
•Exploits SUID / Permissions(SUID programme s’exécute avec les droits du propriétaire du fichier) Exploitation de
permissions mal configurées, abus de programmes exécutés avec privilèges élevés, un programme avec privilège root
peut être dangereux s’il possède des bugs
•Exploits de synchronisation et de concurrence
•TOCTOU (Time Of Check To Time Of Use)Le système vérifie une condition, puis l’utilise plus tard, l’état change
entre les deux étapes
## 15

## Lesexploitsciblantlessystèmesd’exploitation
Exploits liés au noyau (Kernel Exploits)
•Kernel Memory ExploitsCorruption de structures internes du noyau, contournement total des protections
•Driver ExploitsExploitation de pilotes vulnérables, accès direct au matériel
•System Call ExploitsAbus d’appels système mal sécurisés, mauvaise validation des paramètres
Exploits de démarrage et persistance
•Bootloader ExploitsCiblent le chargeur de démarrage, exécution avant le système d’exploitation
•Firmware / Low-level ExploitsCiblent BIOS/UEFI, très persistants et difficiles à détecter
Exploits logiques et de configuration
•Misconfiguration ExploitsServices système mal configurés, services exposés inutilement
Exploits de démarrage et persistance
•Fileless ExploitsExploitation sans fichier malveillant, abus des fonctionnalités légitimes du SE (Le code malveillant
est chargé et exécuté uniquement en RAM, rien n’est écrit sur le disque, et disparaît souvent après redémarrage,  du
code est injecté dans la mémoire d’un processus existant)
•Chain ExploitsCombinaison de plusieurs exploits, très utilisés dans les attaques avancée (enchaîner plusieurs failles
pour atteindre un objectif)
## 16

Élévation de privilèges (Privilege Escalation)
•L’élévation de privilèges est une attaque qui permet à un utilisateur ou à un programme d’obtenir des droits
supérieurs à ceux qui lui sont normalement accordés par le système d’exploitation.
Types d’élévation de privilèges :
- Élévation verticale:utilisateur standard → administrateur / root
- Élévation horizontale:accès aux ressources d’un autre utilisateur ayant le même niveau
## Causesprincipales
–Failles dans le noyau
–Bugs dans les appels système
–Mauvaise gestion des permissions
–Programmes SUID mal sécurisés
–Vulnérabilités dans les pilotes
## Impacts
–Contrôle total du système
–Installation de malwares persistants
–Désactivation des mécanismes de sécurité
## 17

Élévation de privilèges (Privilege Escalation)
- Escalade de privilèges verticale(Vertical Privilege Escalation)
Exemples: - utilisateur → root (Linux) - utilisateur → administrateur (Windows) - processus non privilégié → processus
système
Types d’escalade de privilege verticale :
- Application-based Privilege Escalation :la faille se situe dans un programme ou service déjà privilégié.
Caractéristiques : - binaire SUID mal conçu - service root vulnérable - cron jobs root modifiables
2.Configuration-based Privilege Escalationl’escalade est due à une mauvaise configuration du système.
- Kernel-based Privilege Escalationla faille se situe dans le noyau du système d’exploitation.
Exemples: Use-After-Free,  Buffer Overflow noyau, Race condition (TOCTOU)
- Credential-based Privilege Escalationl’escalade se fait par vol ou abus d’identifiants plus privilégiés.
Exemples : clé SSH administrateur exposée, hash de mot de passe accessible
- Service / Daemon Privilege Escalation: exploitation d’un service système fonctionnant avec des privilèges élevés.
Exemples :  services réseau vulnérables
## 18

Élévation de privilèges (Privilege Escalation)
6 Capability-based Privilege Escalation :exploitation d’une Linux capability mal attribuée ou corrompue.
Exemples: - CAP_SYS_ADMIN - CAP_DAC_OVERRIDE - CAP_NET_ADMIN
Les capabilités Linux sont des droits spéciaux que le noyau Linux peut donner à un processus, pour qu’il fasse certaines
actions normalement réservées au root, ces capabilités peuvent être utilisées dans des attaques si mal configurées.
•CAP_SYS_ADMINl’une des capacités les plus puissantes du noyau.
•Exemples d’actions autorisées : Monter et démonter des systèmes de fichiers (mount, umount)
•CAP_DAC_OVERRIDEDAC = Discretionary Access Control. C’est le contrôle d’accès classique basé sur les permissions
(rwx) et propriétaires de fichiers, exemples d’actions autorisées : Lire n’importe quel fichier, même si le processus
n’a pas les droits de lecture.
•CAP_NET_ADMIN(Network Administration) Permet de gérer et configurer les interfaces réseau et certaines options
réseau avancées.
•Exemples d’actions autorisées : Configurer des interfaces réseau (ifconfig, ip addr).
## •......etc
## 19

Élévation de privilèges (Privilege Escalation)
- Escalade de privilèges horizontale(Horizontal Privilege Escalation)
Exemples : - user A → user B - accès aux fichiers ou sessions d’un autre utilisateur
Types d’escalade horizontale :
- File-based Horizontal EscalationAccès non autorisé aux fichiers d’autres utilisateurs.
Causes fréquentes : fichiers temporaires partagés, répertoires personnels mal protégés
- Session-based Horizontal EscalationCompromission de sessions utilisateur.
Exemples : vol de tokens de session, accès aux sockets de session, récupération de variables d’environnement
- Process-based Horizontal EscalationAccès ou interaction avec les processus d’un autre utilisateur.
Exemples : ptrace mal restreint, lecture de la mémoire d’un autre processus
- IPC-based Horizontal EscalationAbus des mécanismes de communication inter-processus.
Exemples : files de messages partagées, segments de mémoire partagée.
- Network-based Horizontal EscalationAccès aux données réseau d’autres utilisateurs.
Exemples : écoute de ports locaux, interception de communications interne
## 20