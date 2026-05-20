import json
from pathlib import Path


class ConfigManager:
    APP_NAME = "forgejo-sync"

    def __init__(self):
        self.app_dir = None
        self.config_path = None
        self._ensure_structure()

    def _ensure_structure(self):
        home = Path.home()
        self.app_dir = home / self.APP_NAME
        self.app_dir.mkdir(exist_ok=True)
        self.config_path = self.app_dir / "config.json"
        if not self.config_path.exists():
            self._create_default_config()

    def _create_default_config(self):
        with open(self.config_path, 'w') as f:
            json.dump({}, f)

    def load(self):
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def save(self, data):
        with open(self.config_path, 'w') as f:
            json.dump(data, f, indent=4)