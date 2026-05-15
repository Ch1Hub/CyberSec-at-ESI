

Sécurité des systèmes
d’exploitations
Chapitre 1 : Introduction a la sécurité des systèmes
d’exploitations
2eme année second cycle : Cybersecurity
Dr. Manel BABA AHMED
## 1

## Chapitre 1
- Concepts clés de la sécurité des systèmes d’exploitation
- Menaces et vulnérabilités courantes
- Modèles et politiques de sécurité
## 2

La sécurité informatique
La sécurité informatique concerne les mesures et politiques adoptées pour protéger
l’information et les biens contre le vol, la corruption
tout en permettant à ces informations et biens de rester accessibles et utilisables par leurs
utilisateurs légitimes.
Elle inclut également la protectiondes ordinateurscontre les intrusions (par exemple, les
hackers) et les logiciels malveillants (par exemple, les virus).
## 3

Pourquoi la sécurité au niveau du système
d’exploitation est-elle nécessaire ?
Aujourd’hui, aucun système informatique n’est totalement isolé.
Grâce aux nombreuses connexions réseau, tout système peut être accessible depuis
l’extérieur.
Cette évolution est motivée par le besoin de travailler à distance, ainsi de faire des achats en
ligne, etc.
Une seule faille de sécurité dans la conception ou l’implémentation du système d’exploitation,
si elle est exploitée par un attaquant, peut causer des dommages importants.
## 4

La sécurité des systèmes d’exploitations
•La sécurité consiste à fournir un système de protection pour les ressources d’un ordinateur,
telles que :
le processeur (CPU), la mémoire, le disque,
les programmes logiciels, et
surtout les données/informations stockées dans le système.
•Ainsi, un système informatique doit être protégé contre :
l’accès non autorisé par des utilisateurs, et
l’accès malveillant au système, y compris les virus, vers (worm), etc.
## 5

Principes fondamentaux de la sécurité des systèmes
d’exploitation
Contrôle d’accès: déterminer qui peut faire quoi sur les fichiers, programmes et ressources.
Modes d’exécution :distinction entre mode utilisateur et mode système pour protéger le
noyau et les ressources critiques.
Protection de la mémoire: chaque programme ne peut accéder qu’à sa zone mémoire pour
éviter les corruptions ou fuites de données.
Gestion des processus: surveillance et contrôle de l’exécution des programmes pour éviter
les comportements dangereux.
Sécurité des fichiers: permissions pour lecture, écriture et suppression selon les droits des
utilisateurs.
## 6

Principes fondamentaux de la sécurité des systèmes
d’exploitation
Confidentialité des données: protection des informations sensibles contre les accès non
autorisés.
Intégrité du système: garantir que le système et ses logiciels ne sont pas altérés par des
erreurs ou des attaques.
Disponibilité / pérennité: le système doit rester stable et accessible, même en cas de
problème ou d’attaque.
Audit et journalisation: suivi des actions des utilisateurs et programmes pour détecter les
intrusions et anomalies.
Politiques et modèles de sécurité :règles définissant comment les ressources et informations
sont protégées.
## 7

Quelques concepts
•Vulnérabilité: c’est une faiblesse ou un défaut dans un système (logiciel, ou configuration)
qui peut être exploité.
Exemple : un mot de passe faible, un bug dans un programme (un programme qui ne vérifie
pas les droits d’accès), des permissions mal configurées.
•Méthode d’exploitation (ou exploit): c’est la manière dont un attaquant utilise une
vulnérabilité pour obtenir un effet indésirable, comme voler des données ou prendre le
contrôle du système.
Exemple : utiliserun buffer overflowpour exécuter du code malveillant, ouun script pour
deviner un mot de passe faible.
•Menace :Tout ce qui peut causer un dommage à un système, ses données ou ses utilisateurs.
## 8

Quelques concepts
•Si on depasse la taille du buffer, on écrase l’adresse de retour.
•Quand la fonction finit (return), le processeur lit cette
adresse écrasée et saute là où on as décidé (pas où le
programme voulait).
## Resultat :
•Planter le programme (DoS : déni de service)
•Prendre le contrôle du flux d’exécution :
•L’attaquant place son propre code (shellcode) dans le buffer
•Il écrase l’adresse de retour pour pointer vers ce shellcode
•Le programme exécute le code de l’attaquant
Résultat possible : ouverture d’un shell, téléchargement de malware, escalade de privilèges, etc.
## 9

Quelques concepts
•Fonction non sécurisées en C
gets(), strcpy()
char nom[20];
printf("Entre ton nom : ");
gets(nom); // AUCUNE vérification de taille !
•Fonction securisées en C
strncpy(), snprintf()
un script pour deviner un mot de passe faible en python
mots = ["password", "123456", "qwerty", "azerty", "admin", "letmein", "myname123", ...] # dictionnaire
for mot in mots:
reponse = requests.post("https://site.com/login",data={"username": "myname", "password": mot})
if "Bienvenue" in reponse.text:
print("Trouvé !", mot)
break
## 10
•Remarque :
scanf(‘’%s’’,nom) ->non sécurisé
scanf(‘’%10s’’,nom) ->sécurisé en précisant la taille

Les vulnérabilités d’un système d’exploitation
1.Failles logicielles: erreurs de programmation (bugs) pouvant être exploitées.
2.Dépassement de tampon (buffer overflow): écriture hors limites dans la mémoire.
3.Escalade de privilèges: obtention de droits administrateur sans autorisation.
4.Mauvaise gestion des permissions: accès non autorisé aux fichiers ou ressources.
5.Mots de passe faibles ou par défaut: facilitation des accès illégitimes.
6.Services inutiles actifs: augmentation de la surface d’attaque du système (exemple : SSH)
7.Failles dans les pilotes ou le noyau: vulnérabilités critiques affectant tout le système.
8.Absence de mises à jour: exposition à des failles connues non corrigées.
9.Mauvaise configuration du système: paramètres de sécurité mal définis.
10.Manque d’isolation entre processus: un programme peut perturber ou espionner unautre.
## 11

Classification des vulnérabilités des OS
Type de
vulnérabilité
DescriptionExemple
## Logicielle
Bugs ou failles dans les programmes
ou le système
Buffer overflow, faille dans un pilote
## Humaine
Erreurs ou comportements des
utilisateurs ou administrateurs
Mot de passe faible, suppression
accidentelle de fichiers
## Configuration
Paramètres du système mal définis ou
par défaut
Services inutiles activés, permissions
mal réglées
## 12

Les différentes méthodes d’exploitation
Exploitation par dépassement de mémoire (buffer overflow)
Utilisation d’une erreur de gestion de la mémoire pour perturber ou détourner le fonctionnement
d’un programme.
Escalade de privilèges
Exploitation d’une faille pour obtenir des droits plus élevés (ex. utilisateur → administrateur).
Exploitation des mauvaises configurations
Profiter de permissions incorrectes, services inutiles actifs ou paramètres par défaut.
Exploitation des mots de passe faibles
Accès non autorisé grâce à des mots de passe simples ou réutilisés.
Exploitation des services réseau vulnérables
Attaque de services ouverts ou mal sécurisés pour accéder au système.
## 13

Les différentes méthodes d’exploitation
•Injection de code
Introduction de commandes ou code malveillant via des entrées non protégées.
•Exploitation des failles du noyau ou des pilotes
Attaques ciblant des composants critiques du système d’exploitation.
•Exploitation par logiciels malveillants (malware)
Installation de programmes nuisibles pour espionner, perturber ou contrôler le système.
## 14

Exploitation des failles du noyau ou des pilotes
Faille dans les pilotes
–les données envoyées par un utilisateur ne sont pas correctement vérifiées
–le pilote fait trop confiance à l’application
–il exécute des actions sans vérifier les droits
C’est un bug au niveau du pilote
•Exemple: un ordinateur partagé (université, entreprise) avec plusieurs utilisateurs, le service
d’impression est actif, l’attaquant possède un compte user standard aucun droit administrateur, si le
pilote de l’imprimante contient un bug il accepte une requête mal contrôlée, une requête demandant
une action réservée à l’administrateur mais envoyée par un utilisateur normal, par exemple “Installer”,
“modifier”, “configurer” alors que l’utilisateur n’a pas les droits Il exécute une action avec ses privilèges
élevés résultat l’utilisateur simple obtient : des droits administrateur ou un contrôle total du système
Et donc escalade de privilège
## 15

Exploitation des failles du noyau ou des pilotes
Problème: le noyau ne valide pas correctement les données/arguments fournis par l'espace utilisateur (taille d’une
donnée, pointeur, ....etc.)
Résultat: le noyau effectue une opération privilégiée (écriture mémoire, modification de credentials (identité et
droits), appel de fonction arbitraire...) en utilisant ces données non fiables
Conséquences: l'attaquant en mode utilisateur non privilégié obtient :
•droits root / administrateur
•accès total à la mémoire physique / kernel et donc élévation de privilèges locale
## Exemple :
int fd = open("/dev/usb/lp0", O_RDWR);// lp0 représente la première imprimante USB
ioctl(fd, CMD_PRINT, user_data); // demander l'impression, le noyau associe le
fichier au pilote d’impression et donc fd identifie l’imprimante a utiliser
user_data
struct print_request {
void *buffer;   // données du fichier
size_t size;    // taille
## };
## 16

Exploitation des failles du noyau ou des pilotes
## Scenario :
L’utilisateur demande au noyau : d’envoyer les données à l’imprimante via le pilote d’impression
Le programme envoie la requête
Le noyau reçoitCMD_PRINT + user_data
Le pilote d’imprimante : copie les données et les envoie au matériel
L’imprimante imprime le fichier
## Conséquences :
•Crash du noyau ou kernel panic (Denial of Service) a cause d’un pointeur invalide, ou taille incorrecte,
ou données incohérentes, tout le système peut se bloquer ou redémarrer
•Action interdite
•Escalade de privilège
## 17

Exploitation des failles du noyau ou des pilotes
Que peut faire un attaquant après ?
Examiner ou modifier la mémoire de n’importe quel processus : lecture/écriture directe dans la
mémoire physique RAM de tout processus
Lire, écrire, supprimer ou corrompre tout fichier sur tout support de stockage persistant
accessible en écriture, y compris les disques durs et les clés USB : inclut disques durs SSD, clés
USB, même partitions chiffrées si la clé est en mémoire.
Possibilité de bypasser BitLocker (windows)/VeraCrypt(linux) (si le master key est accessible en
mémoire), corrompre les fichiers de logs
Modifier l’ordonnancement ou même arrêter l’exécution de n’importe quel processus : tuer ou
suspendre n’importe quel processus(Windows Defender...etc)(dans Linux la sécurité surtout sur le
noyau, les permissions et des services de securités)
Activer ou désactiver tout périphérique : désactiver la webcam pendant un espionnage, ou
désactiver le réseau pour empêcher des communications
## 18

Exploitation des failles du noyau ou des pilotes
Que peut faire un attaquant après ?
Donner à un processus l’accès aux ressources de n’importe quel autre processus :mémoire mappée
Retirer arbitrairement toute ressource contrôlée par un processus
un processus tente de scanner l’attaquant lui retire ses handles de fichiers (fd) : scan échoue silencieusement.
Exemple: antivirus / EDR (Endpoint Detection and Response)
Le scanner tente d’accéder au disque et certain dossiers
L’attaquant : retire les accès disque, ferme les handles
Le scanner : ne trouve rien conclut : “aucune menace”
Autre : modification bootloader, UEFI firmware (secure boot), initramfs
Secure boot Vérifie que : le bootloader, les pilotes UEFI et autres sont autorisés, ce qui bloque certain
attaques comme modifications du bootloader
## 19

Exploitation des failles du noyau ou des pilotes
Que peut faire un attaquant après ?
Répondre à tout appel système par une réponse mensongère maximisant les dommages
Appel système open() → retourne “succès” alors que le fichier n’a jamais été lu, le scanner pense avoir
analysé un fichier(faux négatif)
Un faux négatif (False Negative) se produit lorsqu’un système de sécurité ne détecte pas une menace qui est
pourtant réelle.
Appel système write() → retourne “tout écrit” données perdues silencieusement, logs incomplets
(anti‑forensic)faire en sorte qu’on ne voit rien
Appel système malloc() → indique mémoire insuffisante (indisponibilité)
## 20

Menaces dans les systèmes d’exploitation
Où un malware peut‑il se cacher ?
autoexec.bat(fichiers de démarrages)peuvent lancer un malware avant le démarrage complet de
## Windows.
Linux Services systemd (/etc/systemd/system/*.service)(service définissent quoi lancer, quand, et avec quels
privilèges)
config.sysfichiers de configuration système pouvant être modifiés pour charger des composants
(pilotes) malveillants au démarrage.
autorun.inf(que faire si un support est inséré (CD, Disque...)) peut exécuter automatiquement un
programme malveillant lors de l’insertion d’un support ou de l’accès au disque.
## Linux (/etc/udev/rules.d/)
services.msc, Boot Configuration Data, BOOT.inifichiers critiques du démarrage : leur modification
permet d’altérer la séquence de boot ou de lancer du code malveillant très tôt.
## Linux /boot/grub/grub.cfg
## 21

Menaces dans les systèmes d’exploitation
Où un malware peut‑il se cacher ?
•io.sysfichier système bas niveau servent d’interface avec le matériel ; sa modification donne un
contrôle très précoce du système.
Linux /boot/vmlinuz- ou autre
•desktop.inic’est un fichier système caché sous Windows il personnalise l’apparence d’un dossier, peut
être utilisé pour masquer des fichiers et lancer automatiquement des programmes lorsqu’un dossier est
ouvert.
Linux bashrc ou config
•hosts, lmhosts(lan manager host) en les modifiant, un attaquant peut rediriger des connexions réseau
ou usurper des noms de machines.
## Linux /etc/hosts
## /etc/resolv.conf
## 22

Menaces (threats) dans les systèmes d’exploitations
Virusclassique se colle à des fichiers ou programmes et s’exécute quand on ouvre le fichier infecté
Macros Exploite les fichiers Office (Word, Excel), se propage via pièces jointes Office malveillantes
Vers (Worms)se propage d’une manière autonome (vulnérabilité réseau)
Exemple : Mirai
cherche des appareils Linux exposés (SSH, ou services vulnérables)
exploite des mots de passe faibles ou failles connues
transforme la machine en bot
Cheval de Troie (Trojan)se fait passer pour un logiciel légitime (faux antivirus, crack, mise à jour...)
Se propage via téléchargement ou autre ( exemple RedLine, AsyncRAT....)
Trojan boot(s’installe dans le démarrage),trojan dropper(installe des fichiers systèmes malveillant),
trojan downloader(telecharge d’autre malware),trojan rootkit(masqué d’autres malware, des
processus ou des fichiers),trojan backdoor(accès sans authentification)
## 23

Menaces (threats) dans les systèmes d’exploitations
Spyware / Keylogger (enregistré les frappes du clavier)espionnent l’utilisateur, données
collectées : sites web visités, identifiants (login, mots de passe), informations personnelles
RansomwareChiffre les fichiers ou verrouille l’accès et demande une rançon LockBit, BlackCat
## 24
## Keylogger
Vol de mots de passe et sessions
Navigateurs (Chrome, Firefox, Edge...)
Web spyare
Vol de cookies
Sessions web actives
Accès à des services en ligne
## Clipboard Stealer
Vol le contenu du presse-papier
Exemples récents :
## LUMMA
RedLine
## Vidar
## Adware / Tracking Malware
Affiche des publicités non désirées
Surveille les habitudes pour profilage
Ransomware :Chiffre les fichiers ou verrouille l’accès et demande rançon LockBit, BlackCat

Menaces (threats) dans les systèmes d’exploitations
Menaces dominantes en 2026
•Ransomware « RaaS Ransomware as a service» évolués souvent avec IA pour muter ou négocier
automatiquement.
•Infostealers livrés via des logiciels piratés, mises à jour compromises ou faux installateurs.
•Malwares polymorphes / IA-assistés Changent de code en temps réel pour échapper aux signatures
antivirus classiques.
•Attaques "identity-first" Vol de tokens de session,le vol de token consiste à récupérer ce jeton
d’authentification qui dit que cet utilisateur est déjà authentifié pour usurper l’identité de l’utilisateur, sans
connaître son mot de passe.
•ClickFix / faux CAPTCHA / fausse mises à jour technique très répandue pour faire exécuter du code
malveillant.
## 25

Menaces (threats) dans les systèmes d’exploitations
Vulnérabilité système :
Exploitation de faillesbugs du noyau ou des services système ou des pilotes
Escalade de privilègesun utilisateur normal devient administrateur/root.
Débordement de mémoire (Buffer Overflow)
Use-After-Free (UAF)libération d’une zone mémoire puis réutilisation corruption ou exécution de code
contrôlé par l’attaquant.
malloc() utilisation normale
free() mémoire rendue au système après free() , le pointeur existe encore, mais la mémoire ne lui appartient plus.la mémoire peut
être réallouée à un autre objet contrôlée par un attaquant
l’attaquant réutilise la même zone mémoire ptr->f();
Race Conditions / TOCTOU (Time-of-Check to Time-of-Use)
Condition de concurrence entre vérification et utilisation bypass de contrôle(access(), open())
Out‑of‑Bounds (OOB)est tout accès hors limites, en lecture ou écriture. Tous les buffer overflows sont des OOB, mais tous
les OOB ne sont pas des buffer overflows. OOB peut toucher des structures internes comme table de descripteur de fichiers
## 26

Menaces (threats) dans les systèmes d’exploitations
Mauvaise configuration et menace interne :
Mots de passe faiblesfaciles à deviner ou à casser (brute force). es attaques combinent listes de mots de
passe + brute force intelligent (patterns prédictifs via IA).
Mauvaise gestion des permissionsaccès non autorisé à des fichiers ou processus.
Usurpation d’identitéun attaquant se fait passer pour un utilisateur légitime (exemple mot de passe volé)
par utilisateur malveillant
Menaces réseau affectant le système d’exploitation
Attaques par déni de service (DoS / DDoS)saturation et indisponibilité des services (serveur web,
messagerie, ssh,dns...). une attaque DoS vise à épuiser une ou plusieurs de ces ressources (bande
passante, cpu, ram,disque.... Etc).
Exemple : syn flood, udp flood, fork bomb.... etc
Attaques Man-in-the-MiddleDNS spoofing (redirection vers faux sites).
Scans et reconnaissancedécouverte des ports ouverts et services actifs.Port scanning
## 27

Que ce qu’un modèle de sécurité ?
•Un modèle de sécuritéest un plan ou un guide general qui montre comment protéger un système et ses
données contre toute intrusion externe ou interne
## Exemple :
•Système : mon ordinateur
•Modèle de sécurité : le système s’assure automatiquement que les comptes normaux ne peuvent pas
installer de logiciels, et que tout changement est tracé.
Bell-LaPadula (BLP) Objectif principal : Confidentialité
Biba Objectif principal : Intégrité
Clark-Wilson Objectif : Intégrité via transactions
Role-Based Access Control (RBAC) Objectif : contrôle basé sur les rôles
Modèle à compartiments (CSM) Objectif : Confidentialité et compartimenté
## 28

Les modèles de sécurités
Bell-LaPadula (BLP) Objectif principal : Confidentialité
•Empêche qu’une information “sensible” fuite vers des niveaux moins sécurisés.
•Règles principales :
No read up: un utilisateur ne peut pas lire un document d’un niveau supérieur.
No write down: un utilisateur ne peut pas écrire vers un niveau inférieur.
Biba Objectif principal : Intégrité
•Empêche que des données soient modifiées par des utilisateurs non autorisés.
•Règles principales (inverse de Bell-LaPadula) :
No read down: un utilisateur ne peut pas lire des données d’un niveau inférieur.
No write up: un utilisateur ne peut pas écrire vers un niveau supérieur.
Remarque: Confidentialité → on protège le haut (les secrets ne doivent pas descendre)
Intégrité → on protège le haut aussi, mais en empêchant le bas de modifier le haut
## 29

Les modèles de sécurités
•Bell-LaPadulaprotège la confidentialité (les secrets ne doivent pas fuiter vers le bas).
Règles : No Read Up + No Write Down → Les infos secrètes descendent (on peut lire vers le bas), mais ne
remontent jamais.
•Biba protège l’intégrité (les données fiables ne doivent pas être polluées par le bas).
Règles : No Read Down + No Write Up → (on peut lire vers le haut), mais la corruption ne monte jamais.
## 30

Les modèles de sécurités
Clark-Wilson Objectif : Intégrité via transactions
•Les utilisateurs ne manipulent pas directement les données sensibles.
•Tout accès se fait via des transactions contrôlées et validées.
•Utilisé pour les systèmes bancaires et financiers.
Role-Based Access Control (RBAC) Objectif : contrôle basé sur les rôles
•Les utilisateurs ont des rôles, et chaque rôle a des permissions spécifiques.
•Très utilisé dans les entreprises modernes et systèmes d’exploitation.
Modèle à compartiments (CSM) Objectif : Confidentialité et compartimenté
•Les données sont classées en compartiments, et un utilisateur doit avoir une autorisation explicite pour
chaque compartiment.
•Très utilisé dans les organisations militaires et gouvernementales où certaines informations sont sensibles
même pour des personnes du même niveau hiérarchique.
## 31

Les modèles de sécurités (exemples)
Bell-LaPadula (Confidentialité) :Empêche les fuites d’informations vers des niveaux moins sécurisés.
## Exemple :
•Dans unearmée, les documents classifiés “Top Secret” ne peuvent être lus que par les officiers autorisés.
•Un soldat avec un niveau “Secret” ne peut pas lire un document “Top Secret”.
•Mais un officier “Top Secret” peut lire et écrire dans tous les documents de son niveau
Biba (Intégrité) :Empêche que des données soient modifiées par des utilisateurs non autorisés.
## Exemple :
•Dans unebanque, un employé junior ne peut pas modifier les soldes des comptes d’un client important.
•Il peut consulter les données nécessaires à son travail (No write up).
•Seuls les employés autorisés (niveau supérieur) peuvent effectuer des modifications sensibles.
## 32

Les modèles de sécurités (exemples)
Clark-Wilson (Intégrité via transactions) :Les utilisateurs n’accèdent pas directement aux données
sensibles.
## Exemple :
•Dans unsystème bancaire, un employé ne peut pas modifier directement les comptes clients.
•Il doit passer par une transaction validée, comme “effectuer un virement”, qui est contrôlée par le
système pour garantir l’intégrité.
Modèle à compartiments (CSM) :Accès sélectif aux données à l’intérieur d’un même niveau de sécurité.
## Exemple :
•Dans unministère ou une agence gouvernementale, un agent du niveau “Secret” peut accéder à certains
dossiers mais pas à d’autres même si tous sont au niveau “Secret”.
•Chaque dossier est un compartiment, et il faut une autorisation spécifique pour y accéder.
## 33

Les modèles de sécurités (exemples)
•RBAC (Role-Based Access Control) :L’accès aux ressources dépend du rôle de l’utilisateur.
## Exemple :
•Dans uneentreprise,un comptable peut consulter les comptes clients mais ne peut pas modifier les
contrats.
•Un manager peut approuver les budgets mais ne peut pas modifier les transactions bancaires.
•Les rôles définissent exactement qui peut faire quoi.
## 34

Les modèles de sécurités (résumé)
## 35
ModèleBut principalExemple d’utilisation
Bell-LaPadulaConfidentialitéMilitaire
BibaIntégritéSystèmes financiers
Clark-WilsonIntégrité via transactionsBanques
Modèle à compartiments
## (CSM)
Confidentialité et
compartimentée
Organisations militaires et
gouvernementales
RBACContrôle basé sur les rôlesEntreprises, OS modernes

Que ce qu’une politique de sécurité ?
Une politique de sécuritéest un ensemble de règles formelles qui définissent les exigences de sécurité
d’un système, afin de garantir la confidentialité, l’intégrité et la disponibilité des ressources.
Un guide officiel qui définit les règles, les rôles et les actions à suivre pour protéger un système et ses
données.
Elle répond clairement aux questions :
–Qui peut accéder au système ?
–À quoi peut-il accéder ?
–Que faire en cas de violation ?
–Comment protéger les données personnelles et systèmes ?
–Comment assurer la traçabilité et l’auditabilité ?
## 36

Quelques objectifs de la politique de sécurité
Protection des ressources :
garantir la confidentialité des informations sensibles, maintenir l’intégrité des données (prévenir
modifications non autorisées), et assurer la disponibilité des systèmes et services pour les utilisateurs
légitimes.
Gestion des accès:
définir qui peut accéder à quelles ressources, mettre en place des niveaux de privilèges selon les rôles,
contrôler l’accès aux fichiers, applications et réseaux.
Prévention et détection des incidents
réduire les risques de cyberattaques et d’intrusions, détecter rapidement les violations de sécurité, définir
des procédures de réponse aux incidents.
Conformité et réglementation :
respecter les normes et régulations (ex. GDPR (règlement européen), ISO 27001(norme internationale).
## 37

Contenu d’une politique de sécurité
Une bonne politique de sécurité définit :
- Utilisation acceptable des systèmes et des données.
- Gestion des mots de passe et des comptes utilisateurs.
- Contrôles d’accès : qui peut accéder à quoi et comment.
- Sécurité réseau et protection contre les menaces externes.
- Procédures en cas d’incident (comment réagir si un problème survient).
## 38

Modèles et politique de sécurité (exemple 1)
Exemple pratique : RBAC et une politique de sécurité
•Principe théorique:L’accès aux ressources dépend du rôle de l’utilisateur dans l’organisation.
•Les rôles définissent les permissions : qui peut lire, écrire ou exécuter quelles actions.
La politique de sécurité (application concrète)
## Règlespratiquesdansuneentreprise:
•Le comptable peut consulter les comptes clients mais ne peut pas modifier les contrats.
•Le manager peut approuver les budgets mais ne peut pas modifier les transactions bancaires.
•L’administrateur système peut installer des logiciels et gérer tous les utilisateurs.
Cette politique applique le modèle RBAC en définissant clairement les permissions pour chaque rôle.
## 39

Modèles et politique de sécurité (exemple 2)
Exemple pratique : RBAC et une politique de sécuritédans les systèmes d’exploitations
/srv : contient les données utilisées par les services fournis par le système
## 40
Définition des rôles :
Admin : gère le système
Enseignant : gère les cours
Étudiant : consulte les cours
Invité : accès très limité
Ressources a protèger
Configuration système :/etc/
Dossier cours :/srv/cours/
Dossier notes :/srv/notes/
## Logs :/var/log
Création des groupes
groupadd admin
groupadd prof
groupadd etudiant
groupadd invite
Création des utilisateurs
useradd -m alice
useradd -m bob
useradd -m charlie

Modèles et politique de sécurité (exemple 2)
Exemple pratique : RBAC et une politique de sécuritédans les systèmes d’exploitations
RBAC avecsudoers(politique de sécurité de sudo « superuser do »)
#sudo cat /etc/sudoers
User_Alias ADMINS    = %admin
User_Alias PROF    = %prof
User_Alias STUDENTS  = %etudiant
## 41
Affectation aux groupes
usermod -aG admin alice
usermod -aG prof bob
usermod -aG etudiant charlie
Permissions sur les ressources
chown root:prof /srv/notes
chmod 770 /srv/notes
chown root:etudiant /srv/cours
chmod 740 /srv/cours

Modèles et politique de sécurité (exemple 2)
Exemple pratique : RBAC et une politique de sécuritédans les systèmes d’exploitations
## Commandes :
Cmnd_Alias COURSE_SVC = /usr/bin/systemctl start cours.service, \
/usr/bin/systemctl stop cours.service, \
/usr/bin/systemctl restart cours.service
Cmnd_Alias COURSE_VIEW = /usr/bin/systemctl status cours.service
Cmnd_Alias COURSE_FILES = /bin/chown -R root:prof /srv/cours, \
/bin/chmod -R 770 /srv/cours
ADMINS   ALL=(ALL) ALL :Les utilisateurs du groupe ADMINS peuvent utiliser sudo pour lancer n’importe
quelle commande, sur n’importe quelle machine, en tant que n’importe quel utilisateur.
PROFS    ALL=(root) COURSE_SVC, COURSE_FILESLes utilisateurs du groupe PROFS peuvent
utiliser sudo uniquement pour exécuter certaines commandes liées aux cours, en tant que root sans avoir tous les
droits administrateur.
STUDENTS ALL=(root) COURSE_VIEWLes utilisateurs du groupe STUDENTS peuvent utiliser sudo
uniquement pour exécuter la commande COURSE_VIEW en tant que root
## 42

Modèles et politique de sécurité (exemple 2)
Exemple pratique : RBAC et une politique de sécuritédans les systèmes d’exploitations
## Résultat :
Admin :sudo bash
## Enseignant :
–sudo systemctl restart cours.service
–sudo chown root:prof /srv/cours
–sudo bash
## Etudiant :
–sudo systemctl status cours.service
–sudo systemctl restart cours.service
## Invité :
–sudo ls
## 43

Modèles et politique de sécurité (exemple 2)
Exemple pratique : RBAC et une politique de sécuritédans les systèmes d’exploitations
Que faire âpres détection d’un incidents ?
Verrouiller un compte suspect :usermod -L charlie
Révoquer les privilèges sudo :gpasswd -d charlie sudo
Désactiver l’accès SSH :passwd -l charlie
Isoler une machine du réseau :ip link set eth0 down
Supprimer un compte suspect :userdel -r guest
Changer tout les mot de passe :passwd alice et passwd bob
Mise a jour système :apt update && apt upgrade
Redémarrer un service :systemctl restart cours.service
Restaurer depuis une sauvegarde :cp -r /backup/cours/* /srv/cours/
Examiner les log :journalctl
Vérifier les connexion :last, who
## 44

Importance de la politique de sécurité
Comportement des utilisateurs:
définit ce qu’on peut ou ne peut pas faire.
Gestion des risques:
limite la surface d’attaque numérique.
Continuité des activités:
réduit la probabilité et l’impact des cyberattaques.
Réponse aux incidents:
décrit comment réagir en cas de faille.
Conformité réglementaire:
aide à répondre aux normes comme ISO.
## 45