import os
import smtplib
import time
import logging
import argparse
from configparser import ConfigParser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import defaultdict

# Configuration
config_file = '/etc/surisentry/surisentry.conf'
log_file = '/var/log/surisentry.log'
alert_log_file = '/var/log/suricata/fast.log'

# Gérer les arguments de ligne de commande
parser = argparse.ArgumentParser(description="Surisentry - Alerte Suricata")
parser.add_argument('-v', '--verbose', action='store_true', help='Activer le mode verbeux')
args = parser.parse_args()

# Configurer le logging
if args.verbose:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Charger la configuration
config = ConfigParser()
config.read(config_file)

# Paramètres SMTP
smtp_server = config.get('SMTP', 'smtp_server')
smtp_port = config.getint('SMTP', 'smtp_port')
smtp_user = config.get('SMTP', 'smtp_user')
smtp_password = config.get('SMTP', 'smtp_password')
use_ssl = config.getboolean('SMTP', 'use_ssl')
from_email = config.get('Email', 'from_email')
to_emails = config.get('Email', 'to_emails').split(',')

# Critères de filtrage des alertes
alert_priority = list(map(int, config.get('Alertes', 'alert_priority').split(',')))
min_delay_between_alerts = config.getint('Alertes', 'min_delay_between_alerts')
max_emails_per_day = config.getint('Alertes', 'max_emails_per_day')
max_alert_repeats = config.getint('Alertes', 'max_alert_repeats')

# Récupérer l'ID de l'instance
instance_id = config.get('Instance', 'instance_id')

last_sent_time = 0
sent_alerts_today = []
alert_repeat_count = defaultdict(int)

# Fonction pour envoyer un email
def send_email(subject, body, alert_ids_priorities):
    try:
        # Création du message
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = ', '.join(to_emails)
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Connexion au serveur SMTP
        if use_ssl:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()

        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, to_emails, message.as_string())
        server.quit()

        # Logging des alertes envoyées (avec leurs IDs et priorités)
        logging.info(f"Email envoyé avec succès: {subject} - Instance: {instance_id}")
        logging.info("Détails des alertes envoyées :")
        for alert_info in alert_ids_priorities:
            logging.info(f"    - {alert_info}")
        
        if args.verbose:
            print(f"L'e-mail a été envoyé avec succès : {alert_ids_priorities}")

    except Exception as e:
        logging.error(f"Erreur lors de l'envoi de l'e-mail : {e}")
        if args.verbose:
            print(f"Erreur lors de l'envoi de l'e-mail : {e}")

# Filtrer les alertes en fonction de la priorité
def filter_alerts():
    try:
        with open(alert_log_file, 'r') as file:
            alerts = file.readlines()
    except FileNotFoundError:
        logging.error(f"Fichier de log non trouvé : {alert_log_file}")
        if args.verbose:
            print(f"Fichier de log non trouvé : {alert_log_file}")
        return []
    except Exception as e:
        logging.error(f"Erreur lors de la lecture du fichier de log : {e}")
        if args.verbose:
            print(f"Erreur lors de la lecture du fichier de log : {e}")
        return []

    filtered_alerts = []
    for alert in alerts:
        for p in alert_priority:
            if f'[Priority: {p}]' in alert:
                # Ne pas ajouter l'alerte si elle a été envoyée plus de max_alert_repeats fois aujourd'hui
                if alert_repeat_count[alert] < max_alert_repeats:
                    filtered_alerts.append(alert)
                break  # Une seule priorité par alerte

    return filtered_alerts

# Fonction principale
def main():
    global last_sent_time, alert_repeat_count

    while True:
        current_time = time.time()
        if (current_time - last_sent_time) >= min_delay_between_alerts:
            alerts = filter_alerts()
            if alerts:
                subject = f"Alerte IDS - Suricata | Instance: {instance_id}"
                body = "\n".join(alerts)
                body += "\n\nCeci est un mail généré par Surisentry."
                
                # Générer la liste des IDs et priorités des alertes pour le logging
                alert_ids_priorities = [f"ID: {hash(alert)}, Priority: {p}" for alert in alerts for p in alert_priority if f'[Priority: {p}]' in alert]

                if len(sent_alerts_today) < max_emails_per_day:
                    send_email(subject, body, alert_ids_priorities)
                    
                    # Mettre à jour le compteur de réenvois pour chaque alerte envoyée
                    for alert in alerts:
                        alert_repeat_count[alert] += 1
                        
                    sent_alerts_today.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time)))
                    last_sent_time = current_time

        # Pause de 60 secondes avant la prochaine vérification
        time.sleep(60)

if __name__ == "__main__":
    main()
