import json

DEFAULT_CONFIG_PATH = "../config/traffic_monitor_config.json"


if __name__ == "__main__":
    with open(DEFAULT_CONFIG_PATH) as f:
        config = json.load(f)

    stream_url = config.get("url")
    region_configs = config.get("regions")
