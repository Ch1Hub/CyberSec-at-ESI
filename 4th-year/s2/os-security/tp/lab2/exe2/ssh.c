#include <libssh/libssh.h> // bibliothèque libssh pour gérer les connexions SSH
#include <stdlib.h> // pour exit(), malloc(), free(), etc.
#include <stdio.h> // pour printf, fprintf, fwrite, etc.
int main() {
ssh_session my_ssh_session; // variable pour représenter une session SSH
int rc; // code de retour des fonctions SSH
// creer une session ssh
my_ssh_session = ssh_new(); // initialise une nouvelle session SSH
if (my_ssh_session == NULL) // vérifie si l'allocation a échoué
exit(-1);
// configuration de l'hôte et de l'utilisateur
ssh_options_set(my_ssh_session, SSH_OPTIONS_HOST, "127.0.0.1"); // adresse IP ou hostname
du serveur
ssh_options_set(my_ssh_session, SSH_OPTIONS_USER, "labuser"); // nom de l’utilisateur SSH
//connexion au serveur ssh
rc = ssh_connect(my_ssh_session); // tentative de connexion
if (rc != SSH_OK) { // si la connexion échec
fprintf(stderr, "Erreur de connexion: %s\n", ssh_get_error(my_ssh_session));
ssh_free(my_ssh_session); // libère la session
exit(-1);
}
// s'authentifier par mot de passe
rc = ssh_userauth_password(my_ssh_session, NULL, "REDACTED_SSH_PASSWORD"); // mot de passe de l’utilisateur
if (rc != SSH_AUTH_SUCCESS) { // si échec
fprintf(stderr, "Erreur d’authentification: %s\n", ssh_get_error(my_ssh_session));
ssh_disconnect(my_ssh_session);

4

ssh_free(my_ssh_session);
exit(-1);
}
// creer un canal pour executer une commande
ssh_channel channel = ssh_channel_new(my_ssh_session); // nouveau canal
ssh_channel_open_session(channel); // ouverture de la session
ssh_channel_request_exec(channel, "uptime"); // exécution de la commande "uptime" sur
le serveur
// lecture sortie de la commande
char buffer[256]; // tampon pour stocker la sortie
int nbytes;
while ((nbytes = ssh_channel_read(channel, buffer, sizeof(buffer), 0)) > 0) {
fwrite(buffer, 1, nbytes, stdout); // affiche la sortie sur le terminal local
}
//fermer la session et liberer les ressources
ssh_channel_send_eof(channel); // indique la fin de lecture
ssh_channel_close(channel); // ferme le canal
ssh_channel_free(channel); // libère le canal
ssh_disconnect(my_ssh_session); // déconnecte la session
ssh_free(my_ssh_session); // libère la session
return 0; // termine le programme
}
