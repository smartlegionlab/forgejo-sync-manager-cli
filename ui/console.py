from core.config import ConfigManager
from core.auth import ForgejoAuth


class ConsoleUI:
    def __init__(self):
        self.config_manager = ConfigManager()

    def show_welcome(self):
        print("=" * 50)
        print(f"  Welcome to {self.config_manager.APP_NAME}!")
        print("  Repository sync tool for Forgejo")
        print("=" * 50)
        print()

    def prompt_for_auth(self) -> ForgejoAuth:
        print("Forgejo Connection Setup:")
        print("(Leave empty to use existing config values)\n")

        existing_config = self.config_manager.load()

        auth = ForgejoAuth()

        if existing_config.get("username"):
            print(f"Current username: {existing_config['username']}")

        username = input("Enter username: ").strip()
        auth.username = username if username else existing_config.get("username", "")

        token = input("Enter access token: ").strip()
        auth.token = token if token else existing_config.get("token", "")

        server = input("Enter server URL (e.g., http://localhost:3000): ").strip()
        auth.server_url = server if server else existing_config.get("server_url", "")

        return auth

    def save_auth(self, auth: ForgejoAuth):
        config = {
            "username": auth.username,
            "token": auth.token,
            "server_url": auth.server_url
        }
        self.config_manager.save(config)
        print("[OK] Configuration saved")

    def show_config_status(self, auth: ForgejoAuth):
        if auth.is_configured():
            print("\n[OK] Configuration loaded:")
            print(f"    Server: {auth.server_url}")
            print(f"    Username: {auth.username}")
            print(f"    API URL: {auth.get_api_url()}")
        else:
            print("\n[WARNING] Incomplete configuration")
