# mqtt_client.py

import ssl
import paho.mqtt.client as mqtt
import yaml

# Chargement de la configuration
with open('config.yaml') as config_file:
    config = yaml.safe_load(config_file)

# Configuration MQTT
BROKER_ADDRESS = config["mqtt"]["broker_address"]
BROKER_PORT = config["mqtt"]["broker_port"]
USERNAME = config["mqtt"]["username"]
PASSWORD = config["mqtt"]["password"]
TOPIC = config["mqtt"]["topic"]  # Ensure TOPIC is defined here

def mqtt_client():
    """
    Function to initialize and connect the MQTT client.
    """
    client = mqtt.Client()

    # Configuration SSL
    client.tls_set(cert_reqs=ssl.CERT_NONE)
    client.tls_insecure_set(True)
 
    # Authentification
    client.username_pw_set(USERNAME, PASSWORD)

    client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
    client.loop_start()

    return client
