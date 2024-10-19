import json
import logging
from mqtt_client import TOPIC

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCENARIO_GBMETRICS = "gbmetrics"
SCENARIO_GCMETRICS = "gcmetrics"

def publish_scenario(client, scenario, configuration, topic=TOPIC):
    """
    Function to publish a scenario on the MQTT broker.
    
    Parameters:
        client (mqtt.Client): The MQTT client instance.
        scenario (str): The scenario name to publish.
        configuration (dict): The configuration data for the scenario.
        topic (str): The MQTT topic to publish to. Defaults to TOPIC from mqtt_client.
    """
    # Validate input
    if not isinstance(configuration, dict):
        logger.error("Invalid configuration: Expected a dictionary.")
        return

    message = {
        "scenario": scenario,
        "configuration": configuration
    }
    payload = json.dumps(message)

    try:
        result = client.publish(topic, payload)
        if result.rc == 0:
            logger.info(f"Successfully published scenario '{scenario}' to topic '{topic}'.")
        else:
            logger.error(f"Failed to publish scenario '{scenario}'. Return code: {result.rc}")
    except Exception as e:
        logger.error(f"Error publishing scenario '{scenario}': {e}")
