import json
import os
from typing import List

from dotenv import load_dotenv

from config import constants


class ConfigError(Exception):
    pass


class Config:
    def __init__(self, config_path: str = constants.DEFAULT_CONFIG_PATH) -> None:
        self.config_path = config_path
        self._load_camera_stream_url_from_env()
        self._load_config()

    def _load_camera_stream_url_from_env(self) -> None:
        load_dotenv()
        self._camera_stream_url = os.getenv(constants.CAMERA_STREAM_URL_ENV)
        if not self.camera_stream_url:
            raise ConfigError(
                f"{constants.CAMERA_STREAM_URL_ENV} not set in environment variables"
            )

    def _load_config(self) -> None:
        try:
            with open(self.config_path) as f:
                config = json.load(f)
        except FileNotFoundError:
            raise ConfigError(f"Configuration file not found at {self.config_path}")
        except json.JSONDecodeError:
            raise ConfigError(
                f"Invalid JSON in configuration file at {self.config_path}"
            )

        self._region_configs = config.get(constants.REGIONS_CONFIG_KEY)
        if not self._region_configs:
            raise ConfigError(
                f"No regions specified in the configuration under key '{constants.REGIONS_CONFIG_KEY}'"
            )

    @property
    def camera_stream_url(self) -> str:
        """Get the camera stream URL."""
        return self._camera_stream_url  # type: ignore

    @property
    def region_configs(self) -> List[dict]:
        """Get the region configurations."""
        return self._region_configs
