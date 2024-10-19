import pytest
import time
import yaml
from mqtt_client import mqtt_client
from prometheus import query_prometheus
from scenarios import publish_scenario

# Load the configuration
with open('config.yaml') as config_file:
    config = yaml.safe_load(config_file)

PROMETHEUS_WAIT_TIME = config["test"]["prometheus_wait_time"]

# Define scenarios
SCENARIO_GBMETRICS = "gbmetrics"

@pytest.fixture(scope="module")
def mqtt_client_fixture():
    """Fixture to initialize and connect the MQTT client."""
    client = mqtt_client()
    yield client
    client.loop_stop()
    client.disconnect()

def run_gbmetrics_all_connect(mqtt_client_fixture, gs_min, gs_max, centreid, flag, expected_count):
    """Execute a metrics connection scenario."""
    configuration = {
        "setup": {
            "gs_min": gs_min,
            "gs_max": gs_max,
            "centreid_min": centreid,
            "centreid_max": centreid,
            "metrics": "wmo_wis2_gb_connected_flag",
            "value": flag
        }
    }
    
    publish_scenario(mqtt_client_fixture, SCENARIO_GBMETRICS, configuration)
    time.sleep(PROMETHEUS_WAIT_TIME)

    query = f'wmo_wis2_gb_connected_flag{{centre_id="io-wis2dev-{centreid}-test"}} == {flag}'
    result = query_prometheus(query)
    assert result['status'] == 'success', "The Prometheus query failed"
    assert len(result['data']['result']) == expected_count, f"Expected {expected_count} GB connected, found {len(result['data']['result'])}"

# List of test cases
test_cases = [
    (14, 17, 10100, 1, 4),   # All connected : 10100
    (14, 17, 10101, 1, 4),   # Partial [All connected] : 10101
    (14, 15, 10101, 0, 2),   # Partial disconnect [2 disconnect] : 10101
    (14, 17, 10102, 1, 4),   # All connected  : 10102
    (14, 17, 10102, 0, 4)    # All disconnected : 10102
]

@pytest.mark.parametrize("gs_min, gs_max, centreid, flag, expected_count", test_cases)
def test_gbmetrics_connect(mqtt_client_fixture, gs_min, gs_max, centreid, flag, expected_count):
    """Test to simulate different GB connections and disconnections."""
    run_gbmetrics_all_connect(mqtt_client_fixture, gs_min, gs_max, centreid, flag, expected_count)
