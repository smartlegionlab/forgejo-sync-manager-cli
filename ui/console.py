from core.config import ConfigManager
from core.auth import ForgejoAuth


class ConsoleUI:
    def __init__(self):
        self.config_manager = ConfigManager()

    def show_phase(self, phase_num: int, phase_name: str):
        print(f"\n{'=' * 50}")
        print(f"PHASE {phase_num}: {phase_name}")
        print(f"{'=' * 50}")

    def show_success(self, message: str):
        print(f"[✓] {message}")

    def show_error(self, message: str):
        print(f"[✗] {message}")

    def show_info(self, message: str):
        print(f"[i] {message}")

    def show_welcome(self):
        print(f"\n{'#' * 50}")
        print(f"#  Welcome to {self.config_manager.APP_NAME.upper()}!")
        print(f"#  Repository sync tool for Forgejo")
        print(f"{'#' * 50}")

    def prompt_for_auth(self) -> ForgejoAuth:
        print("\nEnter connection details:")

        username = input("  Username: ").strip()
        token = input("  Access token: ").strip()
        server_url = input("  Server URL (e.g., http://localhost:3000): ").strip()

        return ForgejoAuth(username, token, server_url)

    def prompt_retry_or_exit(self) -> str:
        print("\n[!] Authentication failed")
        print("  1. Retry with new credentials")
        print("  2. Exit")
        choice = input("Select (1/2): ").strip()
        return choice

    def save_auth(self, auth: ForgejoAuth):
        config = {
            "username": auth.username,
            "token": auth.token,
            "server_url": auth.server_url
        }
        self.config_manager.save(config)

    def show_connection_status(self, auth: ForgejoAuth, user_data: dict = None):
        print(f"\n{'─' * 50}")
        print("CONNECTION STATUS")
        print(f"{'─' * 50}")
        print(f"  Server:     {auth.server_url}")
        print(f"  API:        {auth.get_api_url()}")
        print(f"  Status:     {self.config_manager.APP_NAME}")
        print(f"  User:       {auth.username}")
        if user_data:
            print(f"  Full name:  {user_data.get('full_name', 'N/A')}")
            print(f"  Email:      {user_data.get('email', 'N/A')}")
        print(f"{'─' * 50}")

    def show_main_menu(self):
        print("\n" + "=" * 50)
        print("MAIN MENU")
        print("=" * 50)
        print("  1. Exit")
        print("=" * 50)

    def get_menu_choice(self) -> str:
        return input("\nSelect option: ").strip()
