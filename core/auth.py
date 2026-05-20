from dataclasses import dataclass
from typing import Optional


@dataclass
class ForgejoAuth:
    username: str = ""
    token: str = ""
    server_url: str = ""

    def is_configured(self) -> bool:
        return bool(self.username and self.token and self.server_url)

    def get_api_url(self) -> str:
        base = self.server_url.rstrip('/')
        return f"{base}/api/v1"
