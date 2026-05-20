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
        print(f"  Status:     Connected")
        print(f"  User:       {auth.username}")
        if user_data:
            print(f"  Full name:  {user_data.get('full_name', 'N/A')}")
            print(f"  Email:      {user_data.get('email', 'N/A')}")
        print(f"{'─' * 50}")

    def show_main_menu(self):
        print("\n" + "=" * 50)
        print("MAIN MENU")
        print("=" * 50)
        print("  1. User Info")
        print("  2. Repository Statistics")
        print("  0. Exit")
        print("=" * 50)

    def get_menu_choice(self) -> str:
        return input("\nSelect option: ").strip()

    def show_user_info(self, user_data: dict):
        print("\n" + "─" * 50)
        print("USER INFORMATION")
        print("─" * 50)
        print(f"  Username:    {user_data.get('login', 'N/A')}")
        print(f"  Full name:   {user_data.get('full_name', 'N/A')}")
        print(f"  Email:       {user_data.get('email', 'N/A')}")
        print(f"  User ID:     {user_data.get('id', 'N/A')}")
        print(f"  Created:     {user_data.get('created_at', 'N/A')}")
        print(f"  Admin:       {user_data.get('is_admin', False)}")
        print("─" * 50)

    def show_repo_statistics(self, repos: list):
        total = len(repos)
        private = sum(1 for r in repos if r.get('private', False))
        public = total - private
        forks = sum(1 for r in repos if r.get('fork', False))
        sources = sum(1 for r in repos if not r.get('fork', False))

        print("\n" + "─" * 50)
        print("REPOSITORY STATISTICS")
        print("─" * 50)
        print(f"  Total repositories:  {total}")
        print(f"  Public:              {public}")
        print(f"  Private:             {private}")
        print(f"  Forks:               {forks}")
        print(f"  Source repositories: {sources}")
        print("─" * 50)

    def show_repo_menu(self):
        print("\n" + "=" * 50)
        print("REPOSITORY MENU")
        print("=" * 50)
        print("  1. Sync All Repositories")
        print("  2. Reclone All Repositories")
        print("  0. Back to Main Menu")
        print("=" * 50)

    def show_sync_results(self, results: dict):
        print("\n" + "─" * 50)
        print("SYNC COMPLETED")
        print("─" * 50)
        print(f"  Cloned:  {results['cloned']}")
        print(f"  Updated: {results['updated']}")
        print(f"  Failed:  {results['failed']}")
        print("─" * 50)

    def show_reclone_results(self, results: dict):
        print("\n" + "─" * 50)
        print("RECLONE COMPLETED")
        print("─" * 50)
        print(f"  Cloned:   {results['cloned']}")
        print(f"  Recloned: {results['recloned']}")
        print(f"  Failed:   {results['failed']}")
        print("─" * 50)
