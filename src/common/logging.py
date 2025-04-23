import logging


class DisabledEndpointFilter(logging.Filter):
    def __init__(self, path: str):
        super().__init__()
        self._path = path

    def filter(self, record: logging.LogRecord) -> bool:
        return self._path not in record.getMessage()
