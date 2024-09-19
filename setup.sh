#!/bin/bash

# Variables
CONFIG_FILE="/etc/surisentry/surisentry.conf"
LOG_DIR="/var/log/surisentry"
SCRIPT_FILE="/etc/surisentry/suricata_alerts.py"
SERVICE_FILE="/etc/systemd/system/surisentry.service"

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
