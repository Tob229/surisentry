# Surisentry

Surisentry est un outil de surveillance des alertes générées par Suricata, qui envoie des notifications par e-mail pour des alertes spécifiques. Ce projet inclut un script Python pour traiter les alertes et un fichier de configuration pour personnaliser le comportement du service.

## Table des matières

- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Service Systemd](#service-systemd)
- [Logging](#logging)
- [Contributions](#contributions)
- [License](#license)

## Installation

Pour installer Surisentry, clonez le dépôt GitHub et exécutez le script d'installation :

```bash
git clone <URL_DU_DEPOT>
cd <NOM_DU_REPO>
chmod +x setup.sh
sudo ./setup.sh
```

Le script copie les fichiers nécessaires, crée les répertoires de logs, configure le service et le démarre.

## Configuration

Le fichier de configuration `surisentry.conf` doit être modifié pour inclure vos paramètres SMTP et autres options. Voici un aperçu des sections disponibles :

- **SMTP** : Informations de connexion pour le serveur SMTP.
  - `smtp_server`: Adresse du serveur SMTP.
  - `smtp_port`: Port du serveur SMTP.
  - `smtp_user`: Nom d'utilisateur pour l'authentification.
  - `smtp_password`: Mot de passe pour l'authentification.
  
- **Email** : Paramètres relatifs à l'envoi des e-mails.
  - `from_email`: Adresse e-mail de l'expéditeur.
  - `to_emails`: Liste des destinataires.

- **Alertes** : Critères de filtrage des alertes.
  - `alert_priority`: Liste des priorités à surveiller.
  - `min_delay_between_alerts`: Délai minimum entre l'envoi des alertes.
  - `max_emails_per_day`: Nombre maximum d'e-mails à envoyer par jour.

## Utilisation

Une fois installé, Surisentry s'exécute en tant que service. Les alertes détectées sont envoyées par e-mail selon les critères spécifiés dans le fichier de configuration. Vous pouvez vérifier l'état du service avec la commande :

```bash
sudo systemctl status surisentry.service
```

## Service Systemd

Surisentry est configuré pour s'exécuter en tant que service systemd. Cela signifie qu'il démarrera automatiquement au démarrage de votre système. Le service peut être géré avec les commandes suivantes :

- **Démarrer le service** : `sudo systemctl start surisentry.service`
- **Arrêter le service** : `sudo systemctl stop surisentry.service`
- **Redémarrer le service** : `sudo systemctl restart surisentry.service`
- **Vérifier le statut** : `sudo systemctl status surisentry.service`

## Logging

Les événements importants, tels que l'envoi d'e-mails et les erreurs, sont enregistrés dans le fichier de log spécifié dans la configuration. Les logs incluent des informations détaillées sur les alertes envoyées, y compris leurs ID et priorités.

## Contributions

Les contributions sont les bienvenues ! Si vous souhaitez contribuer à ce projet, n'hésitez pas à soumettre une pull request.

## License

Ce projet est sous licence MIT. Veuillez consulter le fichier LICENSE pour plus d'informations.
