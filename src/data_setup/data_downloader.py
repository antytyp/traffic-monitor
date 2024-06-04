import logging
from typing import Union, Set

import requests  # type: ignore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataDownloader:
    def __init__(self, stream_url: str) -> None:
        self.stream_url = stream_url
        self.base_url = self._get_base_url()
        self.m3u8_url = self._get_m3u8_url()

        self.downloaded_ts_files_log: Set[str] = set()

    def _get_base_url(self) -> str:
        base_url = self.stream_url.rstrip(self.stream_url.split("/")[-1])
        logger.info(f"Prepared base url: {base_url}")
        return base_url

    def _get_m3u8_url(self) -> str:
        response = requests.get(self.stream_url)
        response.raise_for_status()
        m3u8_url_suffix = next(
            (key for key in response.text.split("\n") if key.endswith(".m3u8")),
        )
        m3u8_url = self.base_url + m3u8_url_suffix
        logger.info(f"Prepared m3u8 url: {m3u8_url}")
        return m3u8_url

    def fetch_new_ts_file(self) -> Union[bytes, None]:
        response = requests.get(self.m3u8_url)
        ts_files = [key for key in response.text.split("\n") if key.endswith(".ts")]
        ts_file_to_download = min(ts_files)

        if ts_file_to_download not in self.downloaded_ts_files_log:
            ts_file_url = self.base_url + ts_file_to_download
            response = requests.get(ts_file_url)
            logger.info(
                f"Downloaded data from {ts_file_url} of size {len(response.content)}."
            )
            ts_file_content = response.content
            self.downloaded_ts_files_log.add(ts_file_to_download)
        else:
            ts_file_content = None

        return ts_file_content
