

Sécurité des systèmes
d’exploitations
Chapitre 3 : Les mécanismes de protections
des systemes d’exploitations
2eme année second cycle : Cybersecurity
Dr. Manel BABA AHMED
## 1

Plan chapitre 3
- Authentification et contrôle d’accès
–Authentification dans les systèmes d’exploitation
–Le control d’accès : DAC, MAC, ACL
- Protection de la mémoire et randomisation de l’espace d’adressage (ASLR)
–Les mécanismes de protection de la mémoire
–La randomisation de l’espace d’adressage ASLR/KASLR
- Chiffrement et démarrage sécurisé (secure boot)
Chiffrement dans les systèmes d’exploitations
## 2

Authentification dans les systèmes d’exploitation
•Mécanisme de vérification d’identité d’un utilisateur
•Un système peut vérifier l’identité de 3 manières :
- Ce que l’utilisateur connaît : mot de passe / PIN
- Ce que l’utilisateur possède : carte à puce (carte bancaire)
- Ce que l’utilisateur est : empreinte digitale, reconnaissance faciale, iris
Comment se fait l’authentification dans un systeme ?
•Saisie des identifiants : login + mot de passe
•Le système vérifie si l’user existe dans/etc/passwd
•Récupération du hash du mot de passe dans/etc/shadow
•Calcule du hash du mot passe saisie
•Comparaison : hash calculé et hash stocké
## 3

Authentification dans les systèmes d’exploitation
Salt: nombre aléatoire ajouté au mot de passe pour empêcher les attaques par table.
Probleme: si deux users ont le meme password, donc il y’aura deux hash similaires un attaquant possede une table de
hash : hash->password
e10adc3949... → 123456
5f4dcc3b5a... → passwordDonc il pourra cassé les deux mot de passe instantanément
## Solution :
Hash lent (bcrypt, SHA-512): ralentit les attaques brute force.
Authentification multi-facteurs (MFA): combinaison de :
–mot de passe + code SMS
–mot de passe + biométrie
## 4
## Alice
salt = AB12
## HASH(123456 + AB12)→X123
## Bob
salt = ZK89
## HASH(123456 + ZK89)→Y456
Hash rapide
SHA256("password")
→calcul en 0.000001 seconde
Hash lent (10 essaie par seconde)
bcrypt("password")
→prend ~0.1 seconde

Authentification dans les systèmes d’exploitation
•Demande de connexion (Front-end de login): Un composant affiche l’invite de connexion et collecte
les identifiants. : Terminal texte → getty / login , Interface graphique → display manager (GDM)
•Le programme de connexion :reçoit le username ainsi password
•Vérification de l’existence du user via NSS (Name Service Switch) :le programme
appelgetpwnam(username),NSS consulte/etc/nsswitch.conf
•Intervention de PAM: (phase d’authentification) le programme appelle PAM (Pluggable
Authentication Modules). PAM applique une pile de règles définie dans :/etc/pam.d/
•PAM lance différents modules selon la configurationpam_unix→ vérifie le mot de passe local
pam_faillock→ anti brute force
•Phase d’ouverture de session (PAM session)si l’authentification réussit, PAM ouvre la session. cela
inclut la création d’environnement utilisateur
•Enregistrement de la session par systemd-logindPAM communique avec systemd-logind (service
lancé par systemd) pour gérer la session user (login, logout, TTY....)
## 5

Le control d’accès
•Mécanismes utilisés par les systèmes d’exploitation pour contrôler l’accès pour répondre a la question :
Qui peut accéder à quoi ? et comment ?
- DAC : Discretionary Access Control
- MAC : Mandatory Access Control
- ACL : Access Control Lists
## 6

Le control d’accès : DAC : Discretionary Access
## Control
Le propriétaire d’une ressource décide lui-même qui peut y accéder et avec quels droits.
–Chaque fichier appartient à : un utilisateur (owner), un groupe
–Les trois catégories d’utilisateurs : user, group, owner
–Les types de permissions : r,w,x
•Lorsqu’un programme veut ouvrir un fichier, le processus fait un appel système (open())
•Le noyau vérifie :
–UID du processus
–permissions du fichier
•Décision : autorisé → accès accordé ou refusé → "Permission denied"
Problème: Un utilisateur peut partager un fichier sans contrôle ou mauvaise configuration
## 7

Le control d’accès : MAC : Mandatory Access Control
Le système d’exploitation impose lui-même les règles d’accès, et les utilisateurs ne peuvent pas les modifier.
Étiquettes de sécurité (Security Labels) chaque objet du système possède un niveau : fichiers, processus,
mémoire, Périphériques
Niveaux d’habilitation des utilisateurs, chaque utilisateur possède aussi un niveau :Public, confidentiel, Secret,
## Top Secret
Le système applique des règles strictes comme :No Read Up No Write Down (Bell-LaPadula)
•Lorsqu’un programme veut ouvrir un fichier :
•Le processus fait un appel système (open())
•Le noyau vérifie :
–UID du processus
–label de sécurité du processus
–label de sécurité du fichier
•Décision : autorisé → accès accordé ou refusé → accès bloqué par la politique MAC
Problème :complexité et configuration difficile pour administrateurs
## 8

Le control d’accès : MAC : Mandatory Access Control
•Un label linux est de cette forme : USER : ROLE : TYPE : LEVEL
Exemple :system_u(processus système):system_r(exécute une tache système):httpd_t:s0
## USERROLE
TYPE (processus)LEVEL
## 9
LabelSignification
system_uprocessus système (4)
user_uutilisateur normal (1)
root_uroot (3)
staff_uadministrateur (2)
LabelSignification
system_rrôle système
user_rrôle utilisateur
staff_rrôle admin
object_rrôle d’objet (fichier,rep,...)
TypeExemple
httpd_tserveur web Apache
sshd_tserveur SSH
init_tsystemd
user_tsession utilisateur
NiveauSignification
s0public
s1confidentiel
s2secret
s3top secret

Le control d’accès : MAC : Mandatory Access Control
–Exemple Apache :
–Fichier que Apache doit envoyer au navigateur :/var/www/html/index.html(serveur distant)
–Le programme appelle :open("index.html")
–Le programme appache (processus ou sujet)system_u:system_r:httpd_t:s0
–Fichier HTML :system_u:object_r:httpd_sys_content_t:s0(fichier web)
–Question : est ce quehttpd_tpeut accéder àhttpd_sys_content_t ??
–Linux compare type du programme :httpd_ttype du fichier :httpd_sys_content_t
–Linux cherche une regle :allow httpd_t httpd_sys_content_t read;
–Linux compare : TYPE processus == TYPE fichier
–Si une regle ditaccès autorisé
–Permission OK, Apache peut lire
Remarque: dans la plupart des système Linux le level utilisé est s0
## 10

Le control d’accès:ACL : Access Control Lists
une liste détaillée qui précise exactement quels utilisateurs peuvent accéder à une ressource et avec
quels droits.
•Dans une ACL : chaque entrée = un utilisateur + des permissions
•Les ACL sont enregistrées comme métadonnées du fichier.
## Exemple :
Autoriser ali a lire :setfacl -m u:ali:r fichier.txt
Afficher les ACL :getfacl fichier.txt
•Différence clé avec DAC : DAC utilise 3 catégories seulement (user, group, others) ACL : nombre illimité
d’utilisateurs spécifiques
•Différence clé avec MAC : MAC est basé sur niveaux de sécurité imposés, ACL : basé sur permissions
détaillées décidées par le propriétaire
Problème :complexité de gestion des ACL, les ACL peuvent contredire les permissions classiques.
## 11

Les mécanismes de protection de la mémoire
Isolation mémoire
NX (No eXecute)
Stack Canary
## SMEP/SMAP
Guard page
ASLR Address Space Layout Randomization
## 12

Les mécanismes de protection de la mémoire
Isolation mémoire :
- Mémoire virtuelle :un processus ne voit pas les adresses physiques, il voit des adresses virtuelles, la
traduction se fait grâce à :
–MMU (Memory Management Unit, matériel du CPU)
–Tables de pages (gérées par le noyau) : chaque processus a sa table de page impossible d’accéder à la
mémoire d’un autre processus
–Si un processus essaie d’accéder ailleurs -> Segmentation Fault (SIGSEGV)
2.Modes de privilèges CPU (User Mode / Kernel Mode): un programme ne peut jamais lire
directement la mémoire du noyau.
- Bits de protection dans les pages mémoire: chaque page mémoire possède des permissions (R,W,X)
Isolation entre processus :processus A ne voit que ses pages et processus B ne voit que ses pages
Remarque :Cas particulier : mémoire partagé (IPC)
## 13

Les mécanismes de protection de la mémoire
NX (No eXecute)un mécanisme qui empêche l’exécution de code dans les zones mémoire destinées aux
données.
–Une zone mémoire peut être soit exécutable soit non exécutable.
–Historiquement, toutes les zones mémoire pouvaient être exécutées.
–Résultat : attaques très faciles.
–Avec NX activé : Quand le CPU tente d’exécuter du code dans la stack -> exception immédiate, crash du
programme
–1 Un bit spécial dans la table des pages dans chaque entrée de page mémoire existe :
–NX bit (ou XD bit chez Intel) NX=0 page exécutable, NX=1 page non exécutable
–Stack,heap et données sont protégés par le NX bit
–Sous windows : DEP = Data Execution Prevention
## 14

Les mécanismes de protection de la mémoire
Stack Canary = valeur placée dans la pile
–C’est une valeur spéciale que le système place dans la stack pour détecter si un buffer overflow a
modifié la pile.
–Son rôle est de détecter une attaque avant que le programme ne saute vers du code malveillant.
–Le système insère une valeur entre le buffer et l’adresse de retour, donc si un overflow se produit ->le
canary sera écrasé le programme détecte l’attaque immédiatement
–Le loader demande au noyau : un nombre aléatoire.random_bytes = get_random_bytes()
–Stock la valeur dans TLS (Thread Local Storage : zone mémoire privé pour chaque
thread)__stack_chk_guard = random_value
–Le compilateur ajout au debut :stack_canary_local = __stack_chk_guard
–Et place avant le return :if stack_canary_local != __stack_chk_guard  call
## __stack_chk_fail()
–La fonction : affiche message*** stack smashing detected ***et tue le programme
immédiatement
## 15

Les mécanismes de protection de la mémoire
SMEP/SMAPce sont des protections CPU (Intel/AMD) qui protègent le noyau contre les attaques venant
de l’espace utilisateur.
SMEP = Supervisor Mode Execution Prevention: empêche le kernel d’exécuter du code situé en
mémoire user.
–Un attaquant place du code malveillant en mémoire utilisateur
–Il exploite une faille kernel
–Il fait sauter le noyau vers son code user
AvecSMEP activé: si le noyau tente d’exécuter du code situé dans une page marquée "user" alors ->
exception CPU immédiate
Chaque page mémoire a un bit :
•User (page accessible en mode User, U=1)
•Supervisor (page résérvé au kernel, U=0)
•Quand le CPU est en mode supervisor (ring 0) -> SMEP dit : Interdit d’exécuter des pages marquées User
## 16

Les mécanismes de protection de la mémoire
SMAP = Supervisor Mode Access Preventionempêche le kernel d’accéder (lire/écrire) à la mémoire
user.
•Quand le noyau essaie de lire ou d’écrire dans une page marquée User -> Exception CPU
Comment le kernel lit les arguments des programmes ?
Exemple :read(fd, buffer_user, size);// le buffer est en espace user.
–Donc : Le programme fait un appel système, le CPU passe en Ring 0, le kernel doit copier les arguments
depuis la mémoire user
–Mais SMAP dit normalement :Ring 0 + page U=1 → accès interdit
–Le CPU fournit deux instructions spéciales :
stac   ; Set AC flag (autorise accès user)(Alignment Check flag)
copy_from_user()
clac   ; Clear AC flag (réinterdit accès user)
L’accès est autorisé uniquement pendant ce court moment.
## 17

Les mécanismes de protection de la mémoire
Guard pageest une page mémoire marquée comme non accessible pour détecter un dépassement
mémoire (overflow) elle agit comme un mur invisible, cette page est : No READ, No WRITE, No EXECUTE,
toucher la guard page provoque SIGSEGV
## Problème :
•La stack peut grandir dynamiquement, si un programme alloue trop de mémoire et fait une récursion
infinie, cela provoque un stack overflow, il pourrait écraser d’autres zones mémoire.
Solution :mettre une page interdite, le système place une page spéciale, si la stack dépasse sa limite :
–accès à la guard page
–Page Fault
–crash immédiat
## Remarque :
–Canary protège l’intérieur d’une fonction
–Guard page protège la limite de la stack (empêcher la stack de dépasser sa taille autorisé)
## 18

Randomisation de l’espace d’adressage : ASLR/KASLR
ASLR Address Space Layout Randomization
•ASLR agit au niveau de l’espace d’adressage virtuel du processus
•Lors de l’appelexecve(), le noyau :
–Crée l’espace virtuel
–Choisit des adresses aléatoires
–Fait des mappings viammap()(lib,fichier...)
•Donc ASLR est : un mécanisme du Virtual Memory Manager du noyau
•Un mécanisme qui opère au niveau de la mémoire virtuelle du processus car les attaques exploitent des
adresses virtuelles, et que seul le noyau contrôle ces adresses lors du mapping mémoire.
Remarque :historiquement, le chargeur copiait réellement le programme en RAM, avec la mémoire
virtuelle, il ne copie plus tout : il crée des mappings virtuels, et le chargement physique se fait à la
demande.
Le noyau ensuite décide de l’espace d’adressage physique du processus via le gestionnaire de mémoire
## 19

Randomisation de l’espace d’adressage : ASLR/KASLR
•Lors de l’exécution d’un programme : ./program, le fichier ELF contient des segments
(.code, .données, .bss....etc) avec leurs adresse logique prevu ainsi des permissions
•Le kernel appelle :execve ()pour charger le programme lancé
•Le noyau appelle son générateur d’offset :get_random_bytes()
•Il génère plusieurs offset :stack_random, mmap_random, heap_randomqui sont stocké dans
une structure qui décrit la mémoire du processus(struct mm_struct)
•L’appel systèmemmap()(memory mapping) permet de :
–charger les bibliothèques (libc, etc.)
–mapper une zone de mémoire dans l’espace d’adressage d’un processus (MAP_PRIVATE)
–allouer de la mémoire (MAP_ANONYMOUS) (ex : heap)
–Les grandes allocations heap sont créer avecmmap()
Remarque: il existe deux types de heap : heap principal créer initialement parbrk(), et heapmmap().
ASLR agit principalement au moment des appelsmmap()
## 20

Randomisation de l’espace d’adressage : ASLR/KASLR
Randomisation lors d’un appel mmap ()
Le kernel appelle :
unsigned long arch_mmap_rnd() {
unsigned long rnd;
rnd = get_random_long();     // utilise get_random_bytes
rnd &= mmap_rnd_mask;        // limite la taille
return rnd << PAGE_SHIFT;  }  // alignement page
Generer un nombre aléatoire 64 bits
get_random_long() = 0x9F2A6C3D78B4E912
•le masquemmap_rnd_masklimiter la taille de l’offset aléatoire.les adresses doivent rester dans une zone
valide l’espace mémoire est limité
Exemple : le masque correspond a 22bits de randomisation
•L’opération & garde uniquement les bits autorisé
•rnd= un offset aléatoire valide pour mmap
•Kernel calcule de l’adresse finale :mmap_base = base + rnd;
## 21

Randomisation de l’espace d’adressage : ASLR/KASLR
Randomisation lors de la création du heap principal
Heap créer par l’appel brk ()
unsigned long randomize_brk(unsigned long brk)
{    unsigned long random_offset;
// brk valeur initiale calculé par kernel
if (current->flags & PF_RANDOMIZE) {
//verifier si l’ASLR est activé pour ce processus
random_offset = get_random_long() & BRK_RND_MASK;
brk += random_offset; //Le heap grandit vers le haut
(adresses croissantes)// brk program break déplace la limite du heap
## }
return PAGE_ALIGN(brk);
## }
## 22

Randomisation de l’espace d’adressage : ASLR/KASLR
Randomisation lors de la création de la stack
La pile d’un processus est creer par le noyau lui même, la fonction de la randomisation suivante est
appelée
unsigned long randomize_stack_top(unsigned long stack_top)
{ unsigned long random_offset; // stack_top valeur initiale de la stack
if (current->flags & PF_RANDOMIZE) {// Vérifie si l’ASLR est activé
pour ce processus, PF_RANDOMIZE est un flag dans current->flags
// Si ASLR est désactivé (randomize_va_space = 0), ce bloc ne s’exécute
pas
random_offset = get_random_long() & STACK_RND_MASK;
stack_top -= random_offset;//soustraire l’offset au sommet de la
stack
// Parce que la stack grandit vers le bas (adresses décroissantes)
## }
return PAGE_ALIGN(stack_top);// Aligne l’adresse finale sur la taille
d’une page mémoire (ex: 4 KB) }
## 23

Randomisation de l’espace d’adressage : ASLR/KASLR
Randomisation avec Position Independent Code (PIE)
•Un programme compilé avec : –fPIE peut être chargé à n’importe quelle adresse mémoire
•Donc son code.textlui-même peut être randomisé.
•Sans PIE le code principal a une adresse fixe
•Le kernel détecte que le binaire est PIE dans ELF :
if (elf_executable_is_pie) {
unsigned long random_offset;
random_offset = arch_mmap_rnd();
load_bias = random_offset << PAGE_SHIFT;}// PAGE_SHIFT combien de bits
faut il pour coder une page (<< est un décalage qui signifie offset *
taille page)
// pour que l’adresse soit aligné sur une frontière de page
Unsigned long arch_mmap_rnd(){return get_random_long() & mmap_rnd_mask;}
•Le loader : ld_linux.so applique le load_bias et fait les relocations
## 24

Randomisation de l’espace d’adressage : ASLR/KASLR
## Résumé :
Calcule d’adresse virtuelle finale :
Heap : le noyau calcule l’adresse de base brk initial et lui ajoute random_offset
adresse_heap = brk_initial + random_offset
Stack : le noyau calcule l’adresse de base (stack top) et lui soustrait random_offset
adresse_stack = stack_top - random_offset
PIE :adresse de .text = load_bias + p_vaddr(avec p_vaddr souvent 0 ou 0x1000), ou
p_vaddr est définit par le linker
## 25

Randomisation de l’espace d’adressage : ASLR/KASLR
Randomisation avec KASLR
•Sert à randomiser l'adresse de base où le noyau (kernel) est chargé en mémoire au démarrage du
système.
•Concrètement, sans KASLR, le kernel est toujours chargé à la même adresse prévisible(ex:
0xffffffff81000000 sur x86-64), un attaquant qui connaît cette adresse fixe peut facilement
construire des exploits qui pointent directement vers des fonctions ou structures du kernel.
•Avec KASLR, à chaque boot, le kernel est placé à une adresse aléatoire, donc l'attaquant ne sait plus où
se trouvent les fonctions qu'il veut cibler
•Ce qui est randomisé précisément :
•L'adresse de base du code kernel (.text)
•Les modules kernel (avec KASLR aussi)
## •...
## 26

Randomisation de l’espace d’adressage : ASLR/KASLR
Randomisation avec KASLR
•Sur Linux par exemple, c'est le code de décompression du kernel
(arch/x86/boot/compressed/kaslr.c)qui choisit un offset aléatoire avant que le kernel se
charge vraiment
•Le noyau est compressé lors de son chargement en mémoire
•kaslr.c calcule un offset en combinant plusieurs paramètres : paramètres du boot, ..etc
•kaslr.c choisi une base possible et ajoute un l’offset :phys_addr =
adresse_physique_possible + offset_aléatoire
Phys_addr :c’est la ou le noyau sera décompressé
•Il doit respecter : alignement , zones libres, taille du kernel
•Lorsque le noyau est décompressé un espace virtuel du kernel sera créer
•La base virtuelle ainsi la mémoire du kernel est randomisé
•Cela évite les attaques
## 27

Chiffrement dans les systèmes d’exploitation
Les ressources devant être protéger par un chiffrement
- Disque dur
- fichiers/répertoire
- Mot de passe
- Communication réseau
- Mémoire physique
- Intégrité du système (secure boot)
## 28

Chiffrement dans les systèmes d’exploitation
- Disque dur :
Sous linux :LUKS = Linux Unified Key Setup
## Exemple :
cryptsetup luksFormat /dev/sda1
cryptsetup open /dev/sda1 disque_secure
Ou/dev/mapper/disque_secureest un device virtuel créer par le noyau qui contient les données
déchiffrés
Algorithme utilisé : AES-XTS (le plus courant) Advanced Encryption Standard XTS = XEX-based Tweaked-
codebook mode with Ciphertext Stealing
Sous windows :BitLocker
Utilise aussi AES-XTS
## 29

Chiffrement dans les systèmes d’exploitation
## 2. Fichiers/répertoire
Protection des données sensibles sans chiffrer tout le disque il existe deux méthodes :
Méthode 1: chiffrement au niveau du système de fichiers File-system level encryption (user écrit sur
disque le noyau chiffre automatiquement)
Méthode 2: chiffrement au niveau application : l’utilisateur lui même chiffre ces fichiers
Exemple sous linux :
Chiffrer un dossier (méthode 1)
sudo fscrypt setup
fscrypt encrypt /home/user/secret
AES-XTS utilisé
Méthode 2 :openssl enc -aes-256-cbc -in secret.txt -out secret.enc
Sous windows : clic droit -> 7-Zip -> Add archive, entrer mot de passe, choisir AES-256
## 30

Chiffrement dans les systèmes d’exploitation
- Mot de passe
les mots de passes dans les systèmes sont hachés :
–le chiffrement peut être inversé (avec la clé)
–le hachage ne peut pas être inversé
Sur linux les hashs sont stocké dans /etc/shadow
$y$ = yescrypt
## $6$ = SHA-512
## $5$ = SHA-256
$1$ = MD5 (ancien)
Windows utilise NTLM hash et les stocke dans SAM (Security Account Manager)
## 31

Secure boot (démarrage sécurisé) : définition
Quelques notions :
•BIOS utilisé la CMOS pour stocké certains paramètres de réglages principaux (mémoire limité)
•UEFI utilise la mémoire NVRAM
•La flash est partitionnée en zones :
- Firmware UEFI (secure boot)
- Région NVRAM / EFI Variables
•La NVRAM contient :
–Variables de démarrage (boot variables) exemple :
boot order
–Variables secure boot : les clés cryptographiques utilisées pour vérifier le boot.
–Variables de configuration firmware (UEFI
–Exemple : afficher les variables NVRAM avec :ls /sys/firmware/efi/efivars
## 32

Secure boot (démarrage sécurisé) : définition
•Le Secure Boot est une fonctionnalité du firmware Unified Extensible Firmware Interface (UEFI) qui
empêche le démarrage d’un système si le code exécuté n’est pas signé numériquement et approuvé.
•Objectif :
Empêcher le chargement de bootkits ou rootkits avant le démarrage du système d’exploitation.
•Principe:
–Seul un logiciel signé par une clé autorisée peut être exécuté pendant la phase de boot.
–Sans Secure Boot, un attaquant peut modifier :le bootloader, le kernel, les drivers
–Le Secure Boot utilise une chaîne de confiance cryptographique.
–Firmware UEFI (secure boot activé)-> Bootloader signé -> Kernel signé -> Modules kernel signés
–Chaque étape vérifie la signature de la suivante (mécanisme de vérification)
## 33

Secure boot(démarrage sécurisé) : variables
•UEFI utilise 4 variables principales stockées dans la NVRAM pour gérer la confiance des programmes
qui démarrent la machine.
DB (Allow Database)est la liste blanche des programmes autorisés à démarrer.
Elle contient :
–des certificats de confiance
–des hash de programmes autorisés
Exemple : certificat Microsoft
DBX (Deny Database)est la liste noire des programmes interdits au démarrage.
Elle contient :
–des certificats révoqués
–des hash de fichiers interdits
Si un programme correspond à un élément de la DBX -> le boot est bloqué immédiatement.
## 34

Secure boot(démarrage sécurisé) : variables
KEK (Key Exchange Key)est la clé qui autorise la modification des bases DB et DBX et permet de dire si
cette entité a le droit d'ajouter ou retirer des clés dans DB ou DBX
•Remarque :KEK ne sert pas à vérifier les bootloaders elle sert uniquement à gérer les mises à jour de
DB et DBX
PK (Platform Key)est la clé racine du Secure Boot, elle définit qui contrôle la plateforme.
Elle sert à :
–autoriser la modification des KEK
–autoriser les modifications de la configuration Secure Boot
–contrôler la configuration Secure Boot
## –.....
Remarque :sans PK n’importe quel firmware ou attaquant pourrait modifier ces clés
## 35

Secure boot(démarrage sécurisé) : Rappel
–Calcule hash d’un fichier :hash =hash(file)
–Ce hash est signé avec la clé privée
–signature = signer(hash, clé_privée)
–La signature est attaché au fichier
–Vérification :
–hash1 = hash(file)
–Vérification de la signature avec clé publique
–hash2 = verify(signature, clé_publique)
–hash1 == hash2
## 36

Secure boot(démarrage sécurisé) : chaîne de
confiance
Propriétaire initiale: a la sortie de l’usine le constructeur de la machine (Dell, HP, Asus...) installe la
Platform Key (PK)
•Cela signifie que le constructeur contrôle la configuration Secure Boot initiale.
•Il décide :
–quelles KEK sont installées
–quelles clés de confiance (DB) sont présentes
–quelles clés révoquées (DBX) sont présentes.
Il ajoute : KEK -> Microsoft
Donc Microsoft peut :
–autoriser des bootloaders
–révoquer des bootloaders vulnérables.
Et donc le role de PK est seulement de contrôler qui peut modifier la configuration Secure Boot.
## 37

Secure boot(démarrage sécurisé) : chaîne de
confiance
•Ensuite viennent lesKEK (Key Exchange Keys): autoriser la modification des bases DB et DBX
Par exemple :
•Une mise à jour Secure Boot peut :
–ajouter un certificat dans DB
–ajouter un hash dans DBX
Et donc PK -> autorise modification KEK
KEK -> autorise modification DB et DBX
•Base de confiance et de révocation (DB et DBX)Ces deux bases servent pendant le démarrage.
•DBX (deny list)est la liste noire.
•Elle contient :
–L’empreinte (hash) du programme vulnérable est ajoutée à la DBX pour empêcher son exécution
–hash de programmes interdits
Remarque :UEFI vérifie DBX en premier.
## 38

Secure boot(démarrage sécurisé) : chaîne de
confiance
•DB (allow list)Contient :
–certificats autorisés
–hash de programmes autorisés
Verification du bootloader :
UEFI doit chargé le premier programme du démarrage (Bootloader)
Il verifie sa signature en cherchant dans la DBX
UEFI compare : le hash du programme et le certificat de signature
Si ça correspond à un élément de DBX : boot bloqué immédiatement
Si le programme n'est pas dans DBX : UEFI vérifie dans DB. Est-ce que la signature est autorisée ?
UEFI regarde : le certificat utilisé pour signer le programme ou le hash du programme
Si trouvé dans DB : boot autorisé Sinon : boot bloqué
## 39

Secure boot(démarrage sécurisé) : chaîne de
confiance
UEFI execute le Bootloader
Ensuite le bootloader continue la chaîne de confiance.
Le bootloader verifie la signature du kernel
Et le kernel vérifie la signature de ses modules (.ko)
## 40

Secure boot(démarrage sécurisé) : chaîne de
confiance Linux
le firmware UEFI cherche le programme de démarrage dans la partition EFI System Partition , exemple :
/EFI/ubuntu/shimx64.efi
•Avant de l’exécuter, UEFI fait une vérification de signature :
•il lit la signature numérique du fichiershim
il regarde si le certificat utilisé pour signer shim est dans DB, car shim est signé par Microsoft, et le
certificat Microsoft est dans DB.
•Si oui -> le programme est autorisé.
•Une fois exécuté, shim devient le programme qui contrôle la suite du boot.
•Son rôle principal est de vérifier GRUB.
Pourquoi shim ?
•Parce que Linux ne peut pas signer directement GRUB avec la clé Microsoft.
•Shim contient une clé appelée MOK (Machine Owner Key)
## 41

Secure boot(démarrage sécurisé) : chaîne de
confiance Linux
•Ensuite shim charge : grubx64.efi
•Avant de le lancer : shim vérifie sa signature numérique.
•Si la signature est valide-> GRUB est exécuté.
•Lorque le GRUB s’exécute, il va charger le kernel Linux : vmlinuz
•Mais si Secure Boot est actif, GRUB doit vérifier : la signature du kernel ou son hash.
•Si la signature est valide -> le kernel est chargé en mémoire.
•Une fois lancé, le kernel Linux continue la chaîne de confiance.
•Quand un module est chargé :module.ko
•Le kernel vérifie sa signature.
## 42

Secure boot(démarrage sécurisé) : BlackLotus
Bootkit UEFI découvert en 2022/2023
S’exécute très tôt dans le processus de démarrage
Malware capable de contourner le secure boot
BlackLotus exploite une vulnérabilité appelée :CVE-2022-21894
Cette faille permet d’utiliser un ancien bootloader Windows vulnérable pour contourner Secure Boot.
Le problème est que :
–les anciens bootloaders restent souvent acceptés par Secure Boot tant qu’ils ne sont pas révoqués dans
## DBX.
BlackLotus utilise un bootloader signé mais vulnérable
## 43

Secure boot(démarrage sécurisé) : BlackLotus
Fonctionnement de l’attaque
Accès administrateur
•L’attaquant doit déjà avoir : accès administrateur ou accès physique à la machine.
Installation du bootkit un bootloader malveillant
•BlackLotus modifie la partition : EFI System Partition (ESP)
Exploitation de la vulnérabilité Secure Boot
Le bootloader vulnérable est lancé : bootloader signé mais vulnérable
BlackLotus injecte son code
Chargement du bootkit
•BlackLotus charge un composant EFI qui : s’exécute avant Windows ou meme linux et injecte du code
dans le kernel.
•Unefoisactif,lemalwarepeut:désactiverdesprotectionsWindows
•Lemalwarepeut:téléchargerd’autresmalwares,espionnerlamachine,persistermêmeaprès
redémarrage.
## 44