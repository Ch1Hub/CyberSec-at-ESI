

Sécurité des systèmes
d’exploitations
Chapitre 2 : Les attaques sur les systèmes
d’exploitations
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
–BIOS/UEFI est une puce dédiée sur la carte mère
–Un formatage ne règle pas ce problème, BIOS/UEFI se trouve sur une puce SPI
(Serial Peripheral Interface) Flash
–Le malware est toujours là, il réinfecte le système au prochain boot
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
•Hook du chargement du noyau : Intercepter le moment précis où le noyau est chargé en mémoire, afin
de modifier certains paramètres, injecter un module, surveiller ou altérer le comportement du noyau
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
est chargé et exécuté uniquement en RAM, rien n’est écrit sur le disque, et disparaît souvent après redémarrage, du
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
Exemples: Use-After-Free, Buffer Overflow noyau, Race condition (TOCTOU)
- Credential-based Privilege Escalationl’escalade se fait par vol ou abus d’identifiants plus privilégiés.
Exemples : clé SSH administrateur exposée, hash de mot de passe accessible
- Service / Daemon Privilege Escalation: exploitation d’un service système fonctionnant avec des privilèges élevés.
Exemples : services réseau vulnérables
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

Que ce qu’un Rootkit ?
•C'est un ensemble de logiciels malveillants qui :
- Obtient un accès privilégié (niveau root / administrateur) sur un ordinateur ou un serveur
- Se cache extrêmement bien (fichiers, processus, connexions réseau, pilotes...)
- Permet à un attaquant de rester présent longtemps sans être vu
- Le mot vient de « root » (compte super-administrateur sur Unix/Linux) + « kit » (un ensemble de
logiciels malveillants conçu pour fournir un accès privilégié ).
Greg Hoglund, auteur de NT Rootkit, définit un rootkit comme
« un ensemble de programmes qui modifient (patchent) et détournent (trojanisent) les chemins d’exécution
existants du système ».
À quoi sert un rootkit ?
•Un rootkit est un logiciel malveillant utilisé par un attaquant pour masquer sa présence sur un système
compromis et maintenir un accès furtif. Il peut manipuler les processus, fichiers ou journaux pour éviter
la détection. Il partage certaines similitudes avec des logiciels de surveillance légitimes, comme les
spywares ou certains outils de contrôle parental.
## 21

Composants du système ciblés par les Rootkits
•Gestionnaire d’Entrées/Sorties (I/O Manager)enregistrement des frappes clavier ou de l’activité
réseau, sert à espionner ce que fait l’utilisateur (keylogging, trafic).
•Pilotes de périphériques et du système de fichiersmasquage de fichiers
Les fichiers malveillants existent, mais deviennent invisibles pour l’utilisateur et les outils classiques.
•Gestionnaire d’objets (Object Manager)masquage des descripteurs d’objets (processus / threads)
empêche les outils système de voir ou d’accéder à certains processus.
•Moniteur de référence de sécurité (Security Reference Monitor)désactivation des politiques de
sécurité qui contrôlent les accès aux objets à l’exécution
Le rootkit contourne les vérifications de permissions (qui a le droit de faire quoi).
•Gestionnaire de processus et de threadsmasquage des processus et des threads
Les programmes malveillants tournent sans apparaître dans les outils commeps, topou le
gestionnaire de tâches.
•Gestionnaire de configuration (Configuration Manager)masquage des entrées du registreregedit
(windows) les clés de configuration liées au malware sont invisibles.
## 22

Les registres dans Windowsregedit
•Le registre Windows est une base de données qui stocke les paramètres et configurations du système
d’exploitation, des logiciels et des utilisateurs.
•Il contient des clés (comme des dossiers) et des valeurs
(comme des fichiers de configuration).
Il contient :
–Les paramètres système et matériels
–Les logiciels installés
–Les préférences utilisateur
–Les services et programmes de démarrage
•Exemple :
HKEY_CURRENT_USER: la ruche qui contient les paramètres spécifiques à l’utilisateur.
Software\MonApp: le chemin du logiciel.
LicenseKey: ici, la clé de licence serait stockée en tant que chaîne
LastRun :peut stocker la date/heure du dernier lancement en format hexadécimal.
## 23

Masquage de clés dans les registres par un rootkit
•Un rootkit noyau peut intercepter les appels du système qui lisent le registre.
•Il peut filtrer ou cacher certaines clés :
•ces clés n’apparaissent pas dans le registre
•Elles sont utilisées par le malware.
Les clés de configuration liées au malware sont invisibles” signifie que le malware a caché ses entrées dans le
registre, pour ne pas être détecté par l’utilisateur ou les logiciels de sécurité, tout en restant actif.
Persistance: le malware continue de se lancer au démarrage sans être détecté
Difficulté de détection :les outils classiques ne voient pas la clé
Maintient de contrôle :le malware peut rester actif longtemps et continuer à voler ou modifier des
données
Linux utilise des fichiers textes pour stocker les configurations, répartis à différents niveaux :
## Systeme :/etc/
User : répertoire personnel
## Application :/usr/share/
## 24

Type de Rootkit (Classification par niveau)
- User mode (Application) rootkit
- Kernel mode rootkit
- Bootloader (bootkit) rootkis
- Hypervisor rootkits
- Firmware rootkits
- Memory rootkit
## 25

Type de Rootkit (Classification par niveau)
•Ring 0: accès complet à
toute la mémoire et aux instructions
– Rootkits du noyau (Kernel Rootkits)
•Ring 3: accès restreint
à la mémoire et aux
instructions disponibles.
– Rootkits utilisateur (User Rootkits)
PRELOAD lib
•La vue utilisateur / application du système est définie par ce que le système d’exploitation (OS) lui
fournit via l’interface API.
- Un rootkit se cache en interceptant et en modifiant les communications aux interfaces entre les
différents composants du système d’exploitation.
- Les rootkits sont une forme d’attaque de type “man-in-the-middle” (interception et manipulation des
échanges).
## 26

User mode Rootkit
•Un user‑mode rootkit est un rootkit qui fonctionne au niveau utilisateur (Ring 3), sans modifier le noyau. Il ne
contrôle pas directement le système, mais il ment à l’utilisateur et aux applications en falsifiant ce que l’OS leur
montre via les API.
•Un user‑mode rootkit : intercepte des appels API (open, read...etc), filtre les résultats, renvoie une version modifiée
(processus, fichiers, connexions cachés)
•Il agit donc comme un man‑in‑the‑middle
Exemple: commandeps auxappelle une API de l’OS pour lister les processus affiche tous les processus existants
Si malware existant : malware123 modifie ou hooke la fonction utilisée parpssupprime toute entrée contenant
malware123, le processus existe toujours, mais ne s’affiche pas avecps.
Remplacement de commande :
ps, ls, netstatsont remplacées par des versions modifiées , elles filtrent certains résultats
Hook de bibliothèques (ex : libc)
•Le rootkit intercepte :readdir()→ cacher des fichiers,open()→ bloquer l’accès à certains fichiers
DLL injection (Windows)
•Injection d’une DLL malveillante dans les processus, modification des API Windows retournant les infos système
## 27

Kernel mode Rootkit
•Un kernel‑mode rootkit s’exécute dans le noyau du système (Ring 0), Il a accès total à la mémoire, au matériel
et aux mécanismes internes de l’OS. Contrairement au user‑mode rootkit, il ne ment pas seulement aux
applications il modifie directement le fonctionnement du système
•Un kernel rootkit cible des composants centraux : appels système (syscalls), gestion des processus, système de
fichiers, mécanismes de sécurité (contrôles d’accès)
Hook des appels système (System Call Hooking)Les outils(ps, top)demandent au noyaula liste des
processus, cette demande passe par un appel système Le rootkit intercepte cet appel, supprime le processus
malveillant de la réponse, renvoie une liste “propre”
Module noyau :Un système Linux (ou Windows) utilise des modules noyau pour gérer le matériel :carte
réseau, disque, USB etc. Un attaquant installe un module noyau qui se présente comme par exemple :un pilote
Il peut donc cacher des fichiers, masque des connexions réseaux, ouvre des porte dérobés (backdoor) (sans
passé par des contrôles de sécurités)
Remarque : un pilote est un type de module noyau, mais un module noyau n’est pas forcement un pilote
Manipulation de structures internes :Le noyau ne “devine” pas ce qui existe il s’appuie sur des structures de
données internes, listes chaînées, tables, pointeurs, tous les outils (ps, top, gestionnaire de tâches...) lisent ces
structures. Objectif du rootkit : Faire tourner un processus malveillant sans qu’il apparaisse nulle part,retire son
processus de la liste interne
sans arrêter le processus, continue de s’exécuter, utilise CPU et mémoire, et communique sur le réseau
## 28

Bootkit ou MBR/UEFI Rootkit
•Un bootkit est un rootkit qui s’exécute au moment du démarrage, avant le système d’exploitation. Souvent considérés
comme une sous-catégorie des kernel-mode, mais beaucoup de sources les traitent à part car ils s’exécutent avant le
chargement complet de l’OS (infection MBR, bootloader, etc.).
•Il infecte la chaîne de boot : MBR (Master Boot Record), Bootloader, parfois UEFI
Résultat : Le rootkit se lance avant le noyau, donc le noyau démarre déjà compromis.
- La machine démarre
- Le MBR infecté s’exécute en premier
- Le bootkit : charge un noyau modifié ou injecte du code dans le noyau en mémoire
- Ensuite, il lance l’OS comme si de rien n’était
## Résultat :
•l’OS démarre normalement
•l’utilisateur ne voit rien
•Le noyau est déjà sous contrôle
## 29

Hypervisor rootkit (Virtualized Rootkits / VMBR)
•Les hypervisor rootkits, aussi appelés Virtualized Rootkits ou VMBR (Virtual Machine Based Rootkits),
exploitent les mécanismes de virtualisation matérielle. Ils installent un hyperviseur malveillant sous le
système d’exploitation, plaçant l’OS dans une machine virtuelle transparente, sans que celui‑ci en ait
conscience. Niveau d’exécution :Ring‑1L’OS croit avoir le contrôle total, mais tout passe par
l’hyperviseur.
•L’attaquant exploite une vulnérabilité pour charger un hyperviseur malveillant.
•Le système d’exploitation original est placé dans une VM transparente, contrôlée par l’hyperviseur.
•L’OS croit toujours qu’il a le contrôle total du matériel, mais :
•Chaque instruction qu’il exécute passe par l’hyperviseur
•Un hypervisor rootkit placé sous l’OS peut :
–Avoir un accès supérieur au noyau
–Rester indétectable pour l’OS et les antivirus
–Contrôler et filtrer tout ce que le système exécute
–Installer des backdoors et modifier le comportement du système en temps réel
## 30

Hypervisor rootkit (Virtualized Rootkits / VMBR)
•Un hyperviseur est un logiciel ou firmware qui crée et gère des machines virtuelles (VM) sur un
ordinateur physique.
•Fournir à chaque VM l’illusion d’avoir son propre matériel dédié.
•Isoler les VM les unes des autres pour que les actions d’une VM n’affectent pas les autres.
•Gérer le partage des ressources physiques : CPU, RAM, disque, réseau.
## Exemples :
•Type 1 (installé directement sur matériel physique): VMware ESXi, Microsoft Hyper-V, Xen
•Type 2 : VirtualBox, VMware Workstation
•Chaque VM croit qu’elle contrôle son propre CPU, sa RAM et son stockage, alors qu’en réalité, tout est
géré par l’hyperviseur.
•Les VM envoient leurs instructions à l’hyperviseur, qui les traduit pour le matériel physique.
•L’hyperviseur peut filtrer ou modifier les instructions, surtout si c’est un rootkit VMBR.
## 31

## Firmware Rootkit
•Un firmware rootkit est un rootkit qui infecte le firmware d’un composant matériel, par exemple : BIOS
/ UEFI, carte réseau, disque dur / SSD, contrôleur USB, carte graphique
Firmware Rootkit dans une carte réseauLa carte réseau a son propre firmware qui gère
l’envoi/réception des paquets parfois avant même que l’OS n’intervienne L’OS fait confiance à ce que lui
dit la carte réseau.
Exemple concret : espionnage réseau invisible le firmware de la carte réseau est modifié pour : copier
certains paquets réseau les envoyer vers un serveur distant et jamais les signaler à l’OS
Résultat : le trafic malveillant ne passe pas par le noyau, le matériel espionne directement le réseau.
Firmware Rootkit dans un disque dur / SSDPrincipe les disques (HDD/SSD) ont un micro‑contrôleur
interne avec un firmware : gestion des secteurs (exemple)
Exemple concret : données cachées sur le disque le firmware du disque est modifié pour : réserver une
zone secrète du disque invisible pour l’OS non accessible via partitions classiques
Résultat : aucun outil (fdisk, formatage...) ne voit cette zone le rootkit peut y stocker : du code des clés
des données volées même après formatage ou changement d’OS toujours là
## 32

## Memory Rootkit
•Un memory rootkit est un rootkit qui : réside uniquement en mémoire (RAM) n’écrit rien (ou presque
rien) sur le disque disparaît généralement au redémarragefilelessrootkit.
Exemple: kernel memory rootkit
ScénarioLe système fonctionne normalement un code malveillant est injecté directement dans la
mémoire du noyau.
Cette zone mémoire contient : structures de données du noyau : tables de processus, tables de fichiers
ouverts, .... code du noyau : fonctions système, gestion des périphériques, pilotes, modules noyau chargés
etrootkitséventuellement
Ce code intercepte des fonctions critiques, cache processus et connexions désactive certains contrôles
## Résultat :
ls, ps, antivirus→ rien aucune trace sur le disque tout est en RAM
Au redémarrage: le rootkit disparaît sauf s’il est relancé par un autre mécanisme (bootkit, firmware...)
Un memory rootkit n’a pas un ring unique, le ring dépend de l’endroit où il s’exécute
## 33

Détection des Rootkits
Détection comportementaledétecter les modifications dans les appels système, l’ordre et la fréquence des
appels système, vérifier si le flux normal d’exécution d’un programme ou du système d’exploitation a été
modifié par un rootkit.
## Inconvénients
•Peut souffrir d’un taux élevé de faux positifs
•La plupart des utilisateurs finaux n’ont pas les compétences pour filtrer ou analyser ces faux positifs
Détection par intégritédétecte les modifications non autorisées des fichiers système ou des composants du
système d’exploitation chargés en mémoire.
•Calculer un hash cryptographique (MD5, SHA256) des fichiers connus dans un état sain.
•Comparer régulièrement avec les fichiers actuels. Si le hash diffère → le fichier a été modifié → suspicion de
rootkit.
Exemple :sha256sum /bin/ls > ls.hash(création de la base de référence)
sha256sum -c ls.hash(vérification de l’intégrité)
Remarque: les vérifications d’intégrité du système de fichiers sont inefficaces contre la plupart des rootkits
modernes, car ceux-ci effectuent leurs modifications en mémoire plutôt que sur les fichiers système du disque.
## 34

Détection des Rootkits
•Détection par signature: recherche dans la mémoire ou le système de fichiers de motifs d’octets uniques
(signatures), chaîne de caractère, séquence d’instructions... présents dans le code du rootkit. Et comparer avec
une base de signature connu.
•Approche éprouvée utilisée par les antivirus depuis de nombreuses années.
Comment une signature est créée ?
•Un malware est découvert
•Des analystes l’analysent
•Ils extraient un motif unique
•Ce motif est ajouté à la base de signatures
•Les antivirus se mettent à jour
## Inconvénient
•Inefficace contre les rootkits / malwares inconnus (aucune signature existante)
•Même pour un malwareconnu, la signature peut devenir inutile en cas d’un malware polymorphe le code
change à chaque infection la signature binaire n’est jamais la même
## 35

chrootkitpour la détection des Rootkits
C’est un outil antivirus gratuit et open source, disponible surGitHub.
Il lance plusieurs dizaines de tests pour essayer de repérer les traces laissées par des rootkits connus.
Parmi les vérifications les plus importantes :
•Compare les fichiers système importants(ls, ps, netstat, top, ifconfig, login,
sshd...)avec des signatures de la base
•Cherche des processus cachés (en comparant/procet ce que ditpsaux)
•Vérifie si une interface réseau est en mode promiscuous (souvent utilisé par les sniffeurs)
•Regarde les fichiers de logs pour voir s’ils ont été trafiqués
•Détecte plus de 70 rootkits connus (et leurs variantes)
•Cherche des backdoors, des worms, des sniffeurs ou des fileless
•chkrootkitest très bon pour détecter les rootkits anciens et classiques mais est moins efficace
contre les rootkits très récents, il donne parfois des faux positifs
•Il est souvent utilisé en complément derkhunter
## 36

rkhunterpour la détection des Rootkits
Un autre outil open source très populaire sous Linux pour détecter les rootkits, backdoors, sniffers,
exploits locaux et configurations suspectes. C’est souvent comparé àchkrootkit, mais il est un peu plus
complet et plus orienté vérification d’intégrité et configurations.
Il effectue plusieurs types de contrôles :
•Comparaison des hachages (SHA-256 maintenant) des binaires système importants(ls, ps,
netstat, sshd, login, etc.)avec une base de données de versions saines (téléchargée en
ligne) pour vérifier l’intégrité et l’authenticité
•Recherche de fichiers/dossiers typiques des rootkits connus(ex. /dev/.udev/,
## /usr/sbin/...)
•Détection de permissions anormales sur des fichiers critiques (ex. un/bin/lsavecsetuid rootqui
n’est pas normal)
•Recherche de fichiers cachés ou suspects dans/dev, /tmp, /etc
•Analyse des modules kernel pour y trouver des chaînes suspectes (strings malveillantes)
•Vérification des backdoors potentielles dans les configs réseau, cron, etc.
•Scans optionnels dans le contenu des fichiers (pour chercher des signatures malware)
## 37

chrootkit VS rkhunter
## 38
## Critère
chkrootkitrkhunter (Rootkit Hunter)
Méthode de
détection
Signature + analyse comportementaleSignature + intégrité + analyse comportementale
SignatureOui (rootkits connus, fichiers infectés)Oui (rootkits connus, fichiers suspects)
## Comportement
Oui (interfaces réseau en mode
promiscuous)
## Partiel
IntégritéTrès peu
Oui (hash SHA-1/256 des fichiers système
critiques comparé à la base de référence)
CiblesRootkits connus sur fichiers et modules
Rootkits connus + modifications de fichiers
systèmes
## Limites
Ne détecte pas les rootkits fileless ou
inconnus
Plus complet, mais rootkits très furtifs en mémoire
peuvent passer inaperçus
Mise à jourBase de signatures limitée, souvent localeBase de signatures et hash téléchargée en ligne

Le déni de service (DoS)
•Une attaque DoS perturbe la disponibilité et le fonctionnement interne du système d’exploitation, en
ciblant ce que le noyau gère directement.
•Elle cible :
•Perturbation de la gestion des processus
•Perturbation de l’ordonnancement des processus (Scheduler)
•Perturbation de la gestion de la mémoire
## 39

Perturbation de la gestion des processus
La gestion des processus dans un OS (comme Linux) repose sur :
•Une table des processus (process table) limitée en taille (PID max, souvent 32 768 par défaut).
•Des ressources partagées : mémoire, CPU, descripteurs de fichiers.
•Un scheduler qui alloue le temps processeur.
La bombe fork crée une croissance exponentielle de processus :
•Un processus parent appellefork()pour créer un ou plusieurs enfants.
•Chaque enfant répète l'opération immédiatement.
Résultat : nombre de processus = 2ⁿ
En quelques secondes, le système atteint ses limites :
•Plus de PID disponibles.
•Mémoire épuisée (chaque processus consomme de la RAM).
•CPU à 100 % (le scheduler est submergé).
•Impossible de lancer de nouveaux processus (mêmeps, top, ou une session SSH).
## 40

Perturbation de la gestion des processus
•En Bash:
## :(){ :|:& };:
:()définit une fonction vide.
:|:&appelle la fonction en arrière-plan et la pipe vers
elle-même (fork implicite).
;:lance la fonction.
•En C :
## #include <unistd.h>
int main() {
while(1) {
fork();    }
return 0;}
## 41

Perturbation de la gestion des processus
Conséquences spécifiques sur la gestion des processus :
•Saturation de la table des processus : le noyau ne peut plus allouer de nouveaux PID.
•Désorganisation du scheduler : trop de processus prêts à s'exécuter → thrashing
•Création de zombies/orphelins : si le parent meurt, les enfants deviennent orphelins et consomment des
ressources.
•Impact système : même l'administrateur root peut être bloqué (sauf si des limites sont en place).
Comment s'en protéger ?
Limiter les processus par utilisateur (le plus efficace) :
ulimit -u 100   # Maximum 100 processus par utilisateur
## 42

Perturbation de l’ordonnancement des processus
Une attaque DoS peut perturber l’ordonnanceur (scheduler) du système (celui qui décide quel processus
tourne sur le CPU)
Exemple : la fork bomb
## Résultat :
•Trop de processus, la liste d’attente du scheduler devient énorme.
•L’ordonnanceur passe son temps à choisir qui passe ensuite, beaucoup de commutation de contexte
•Les vrais programmes (même un simple terminal) deviennent ultra-lents ou bloqués.
•Monopole CPU avec priorité temps réel : Un processus malveillant se met en priorité maximale
(SCHED_FIFO)et tourne en boucle sans jamais s’arrêter. Résultat : il prend 100 % d’un ou plusieurs
cœurs, l’ordonnanceur n’a plus de place pour les autres tâches,starvation (famine) totale.
En résumé : l’attaque surcharge ou monopolise le scheduler, le système devient très lent, voire
inutilisable, même pour l’administrateur.
Protection de base : limiter le nombre de processus par utilisateur(ulimit -u)et les priorités temps
réel.
## 43

Perturbation de la gestion de la mémoire
•Le noyau gère la mémoire de manière critique (allocations dynamiques, tampons réseau, structures de
données), et un attaquant peut forcer des allocations massives sans libération, entraînant un
épuisement, une fragmentation ou une corruption de la mémoire. Cela provoque un ralentissement, un
plantage ou une indisponibilité du système.
Épuisement de la RAM (memory exhaustion)alloue massivement de la mémoire (malloc, new,
mmap) et ne libère jamais (fuite volontaire)
Saturation du swap :Quand la RAM est pleine ,le noyau pousse des pages vers le swap,
thrashing(pages chargées/évacuées en boucle)
Fragmentation mémoire :allocations/désallocations agressives, blocs libres non contigus Certaines
zones nécessitent de la mémoire contiguë, notamment DMA (Direct Memory Access) pour cartes réseau
ou disque
•Activation de l’OOM Killer :quand la situation devient critique, le noyau déclenche l’Out-Of-Memory
Killer, il tue un ou plusieurs processus jugés “coupables”, Conséquence : services critiques (ssh, web)
peuvent être tués et doncdéni de service
## 44

L’attaque Brute force
- Brute force simple: tester toute les combinaisons possibles
- Attaque par dictionnaire:L’attaquant utilise des mots provenant de dictionnaires ou de listes
fréquentes, parfois modifiés avec des chiffres ou des symboles.
- Attaque hybride par brute force: consiste à combiner une attaque par dictionnaire (liste de mots
connus) avec une brute force simple (ajout automatique de chiffres, lettres ou symboles).
Exemple : mot → mot123 → mot2020 → mot!
## 45

L’attaque Brute force : John the Ripper
John the Ripper :est un outil très connu en cybersécurité utilisé pour tester la robustesse des mots de
passe.
Il sert principalement à faire du cracking de mots de passe à des fins d’audit de sécurité.
## Objectif :
–Retrouver des mots de passe à partir de hashs
–Tester la solidité des mots de passe
–Détecter des faiblesses de sécurité dans un système
Utilisé par : administrateur système, ou pentesteurs
John ne “casse” pas directement un mot de passe, Il travaille sur des hashs., exemple :
password → 5f4dcc3b5aa765d61d8327deb882cf99
John va essayer de retrouver le mot original qui produit ce hash.
## 46

L’attaque Brute force : John the Ripper
Méthode de john :
•John prend un hash de mot de passe (ex : depuis/etc/shadowsous Linux).
•Il essaie de retrouver le mot de passe original en testant des millions de combinaisons avec :
- Attaque par dictionnaire : définit une liste de mot :password, admin, azerty
- Attaque par brute force : teste des combinaison possible :a, aa, b, bb, ab, ba
- Attaque hybrid : combine dictionnaire + variantes :Password123, password@123....
- John calcule le hash :SHA-512(password123)
- Compare avec le hash cible : hash calculé et hash stocké dans/etc/shadow
- Si identique → mot de passe trouvé
## 47