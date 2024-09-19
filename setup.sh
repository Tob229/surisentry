#!/bin/bash

# Variables
CONFIG_FILE="/etc/surisentry/surisentry.conf"
LOG_DIR="/var/log/surisentry"
SCRIPT_FILE="/etc/surisentry/suricata_alerts.py"
SERVICE_FILE="/etc/systemd/system/surisentry.service"

# Fonction d'installation
install() {
    # Créer le répertoire pour le service s'il n'existe pas
    if [ ! -d "/etc/surisentry" ]; then
        sudo mkdir -p "/etc/surisentry"
        echo "Répertoire du service créé: /etc/surisentry"
    fi

    # Créer le répertoire de logs s'il n'existe pas
    if [ ! -d "$LOG_DIR" ]; then
        sudo mkdir -p "$LOG_DIR"
        sudo chown $USER:$USER "$LOG_DIR"
        echo "Répertoire de logs créé: $LOG_DIR"
    fi

    # Copier les fichiers de configuration et de script
    sudo cp suricata_alerts.py "$SCRIPT_FILE"
    sudo cp surisentry.conf "$CONFIG_FILE"
    echo "Fichiers copiés dans les répertoires appropriés."

    # Créer le fichier de service systemd
    sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=Surisentry Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 $SCRIPT_FILE
Restart=always
User=$USER

[Install]
WantedBy=multi-user.target
EOL

    # Activer et démarrer le service
    sudo systemctl enable surisentry.service
    sudo systemctl start surisentry.service

    echo "Service Surisentry activé et démarré."

    # Permissions
    sudo chmod +x "$SCRIPT_FILE"
    echo "Permissions appliquées."

    echo "Installation terminée. Vous pouvez vérifier le statut du service avec 'sudo systemctl status surisentry.service'."
}

# Fonction de désinstallation
uninstall() {
    # Arrêter et désactiver le service
    sudo systemctl stop surisentry.service
    sudo systemctl disable surisentry.service
    echo "Service Surisentry arrêté et désactivé."

    # Supprimer les fichiers et répertoires
    sudo rm -f "$SCRIPT_FILE"
    sudo rm -f "$CONFIG_FILE"
    sudo rm -f "$SERVICE_FILE"
    echo "Fichiers supprimés."

    # Supprimer le répertoire de logs s'il est vide
    if [ -d "$LOG_DIR" ]; then
        sudo rmdir "$LOG_DIR" 2>/dev/null && echo "Répertoire de logs supprimé." || echo "Le répertoire de logs n'est pas vide."
    fi

    # Supprimer le répertoire du service s'il est vide
    if [ -d "/etc/surisentry" ]; then
        sudo rmdir "/etc/surisentry" 2>/dev/null && echo "Répertoire du service supprimé." || echo "Le répertoire du service n'est pas vide."
    fi

    echo "Désinstallation terminée."
}

# Vérification des options
if [[ $1 == "-r" ]]; then
    uninstall
else
    install
fi
