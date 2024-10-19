import requests
import time
import yaml
import logging

# Load configuration
with open('config.yaml') as config_file:
    config = yaml.safe_load(config_file)

# Configuration Prometheus
PROMETHEUS_URL = config["prometheus"]["url"]
SCRAPE_TIMEOUT = config["prometheus"]["scrape_timeout"]

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Validate configuration
required_keys = ["url", "scrape_timeout"]
for key in required_keys:
    if key not in config["prometheus"]:
        raise ValueError(f"Missing required configuration key: {key}")

def query_prometheus(query):
    """
    Function to query Prometheus with a specific query.
    """
    params = {'query': query}
    logger.info(f"Querying Prometheus with query: {query}")
    
    try:
        response = requests.get(PROMETHEUS_URL, params=params, timeout=SCRAPE_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error querying Prometheus: {e}")
        return None  # Return None or handle as needed

def wait_for_prometheus(query, expected_count, timeout=60, interval=5):
    """
    Function to wait for Prometheus to return the expected number of results.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            result = query_prometheus(query)
            if result and result['status'] == 'success' and len(result['data']['result']) == expected_count:
                return True
        except Exception as e:
            logger.error(f"Error while querying Prometheus: {e}")
        time.sleep(interval)
    logger.warning(f"Timeout waiting for Prometheus to return {expected_count} results.")
    return False
