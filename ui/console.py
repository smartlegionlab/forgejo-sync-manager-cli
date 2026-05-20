# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# License: BSD 3-Clause
import time
from core.config import ConfigManager
from core.auth import ForgejoAuth


class ConsoleUI:
    def __init__(self):
        self.config_manager = ConfigManager()

    @staticmethod
    def show_phase(phase_num: int, phase_name: str):
        print(f"\n{'=' * 50}")
        print(f"PHASE {phase_num}: {phase_name}")
        print(f"{'=' * 50}")

    @staticmethod
    def show_success(message: str):
        print(f"[✓] {message}")

    @staticmethod
    def show_error(message: str):
        print(f"[✗] {message}")

    @staticmethod
    def show_info(message: str):
        print(f"[i] {message}")

    def show_welcome(self):
        print(f"\n{'#' * 50}")
        print(f"#  Welcome to {self.config_manager.APP_FULL_NAME.upper()}")
        print(f"#  Repository sync tool for Forgejo")
        print(f"{'#' * 50}")
        time.sleep(1)

    @staticmethod
    def prompt_server_url() -> str:
        print("\nEnter Forgejo server URL:")
        server_url = input("  Server URL (e.g., http://localhost:3000): ").strip()
        return server_url

    @staticmethod
    def prompt_token() -> str:
        token = input("  Access token: ").strip()
        return token

    @staticmethod
    def prompt_retry_server() -> str:
        print("\n[!] Server connection failed")
        print("  1. Try again with different server URL")
        print("  2. Exit")
        choice = input("Select (1/2): ").strip()
        return choice

    @staticmethod
    def prompt_retry_auth() -> str:
        print("\n[!] Authentication failed")
        print("  1. Try again with different token")
        print("  2. Exit")
        choice = input("Select (1/2): ").strip()
        return choice

    def save_auth(self, auth: ForgejoAuth):
        config = {
            "token": auth.token,
            "server_url": auth.server_url,
            "username": auth.username
        }
        self.config_manager.save(config)

    @staticmethod
    def show_connection_status(auth: ForgejoAuth, user_data: dict = None):
        print(f"\n{'─' * 50}")
        print("CONNECTION STATUS")
        print(f"{'─' * 50}")
        print(f"  Server:     {auth.server_url}")
        print(f"  API:        {auth.get_api_url()}")
        print(f"  Status:     Connected")
        if user_data:
            print(f"  User:       {user_data.get('login', 'N/A')}")
            print(f"  Full name:  {user_data.get('full_name', 'N/A')}")
            print(f"  Email:      {user_data.get('email', 'N/A')}")
        print(f"{'─' * 50}")

    @staticmethod
    def show_main_menu():
        print("\n" + "=" * 50)
        print("MAIN MENU")
        print("=" * 50)
        print("  1. User Info")
        print("  2. Repositories")
        print("  3. Settings")
        print("  4. About")
        print("  0. Exit")
        print("=" * 50)

    @staticmethod
    def get_menu_choice() -> str:
        return input("\nSelect option: ").strip()

    @staticmethod
    def show_user_info(user_data: dict):
        print("\n" + "─" * 50)
        print("USER INFORMATION")
        print("─" * 50)
        print(f"  Username:    {user_data.get('login', 'N/A')}")
        print(f"  Full name:   {user_data.get('full_name', 'N/A')}")
        print(f"  Email:       {user_data.get('email', 'N/A')}")
        print(f"  User ID:     {user_data.get('id', 'N/A')}")

        created = user_data.get('created', 'N/A')
        if created != 'N/A':
            created = created.replace('T', ' ').replace('Z', '').split('.')[0]
        print(f"  Created:     {created}")

        print(f"  Admin:       {user_data.get('is_admin', False)}")
        print("─" * 50)
        input("\nPress Enter to continue...")

    @staticmethod
    def show_repo_statistics(repos: list):
        total = len(repos)
        private = sum(1 for r in repos if r.get('private', False))
        public = total - private
        forks = sum(1 for r in repos if r.get('fork', False))
        sources = sum(1 for r in repos if not r.get('fork', False))

        print("\n" + "─" * 50)
        print("REPOSITORIES OVERVIEW")
        print("─" * 50)
        print(f"  Total repositories:  {total}")
        print(f"  Public:              {public}")
        print(f"  Private:             {private}")
        print(f"  Forks:               {forks}")
        print(f"  Source repositories: {sources}")
        print("─" * 50)

    @staticmethod
    def show_repo_list(repos: list):
        print("\n" + "─" * 110)
        print("REPOSITORY LIST")
        print("─" * 110)
        print(f"{'#':<4} {'Repository Name':<50} {'Type':<10} {'Size (MB)':<15}")
        print("─" * 110)

        total_size = 0
        private_count = 0
        public_count = 0

        for n, repo in enumerate(repos, 1):
            name = repo.get('name', 'N/A')
            private = repo.get('private', False)
            repo_type = "Private" if private else "Public"
            size = repo.get('size', 0) / 1024

            if private:
                private_count += 1
            else:
                public_count += 1

            total_size += size

            print(f"{n:<4} {name:<50} {repo_type:<10} {size:.2f}")

        print("─" * 110)
        print(f"{'TOTAL':<55} {public_count + private_count:<10} {total_size:.2f}")
        print(f"{'Public':<55} {public_count:<10}")
        print(f"{'Private':<55} {private_count:<10}")
        print("─" * 110)
        input("\nPress Enter to continue...")

    @staticmethod
    def show_repo_menu():
        print("\n" + "=" * 50)
        print("REPOSITORY MENU")
        print("=" * 50)
        print("  1. Show Statistics")
        print("  2. Show All Repositories")
        print("  3. Check for Updates")
        print("  4. Sync All Repositories")
        print("  5. Reclone All Repositories")
        print("  0. Back to Main Menu")
        print("=" * 50)

    @staticmethod
    def show_updates_result(updates_count: int):
        print("\n" + "─" * 50)
        if updates_count == 0:
            print("No updates available. All repositories are up to date.")
        else:
            print(f"Found {updates_count} repositories with updates available.")
        print("─" * 50)

    @staticmethod
    def prompt_update_choice(updates_count: int) -> str:
        if updates_count == 0:
            return "0"
        print("\n  1. Update all")
        print("  0. Cancel")
        return input("\nSelect option: ").strip()

    @staticmethod
    def show_sync_results(results: dict):
        print("\n" + "─" * 50)
        print("UPDATE COMPLETED")
        print("─" * 50)
        print(f"  Cloned:  {results['cloned']}")
        print(f"  Updated: {results['updated']}")
        print(f"  Failed:  {results['failed']}")
        print("─" * 50)

    @staticmethod
    def show_reclone_results(results: dict):
        print("\n" + "─" * 50)
        print("RECLONE COMPLETED")
        print("─" * 50)
        print(f"  Cloned:   {results['cloned']}")
        print(f"  Recloned: {results['recloned']}")
        print(f"  Failed:   {results['failed']}")
        print("─" * 50)

    @staticmethod
    def show_settings(auth: ForgejoAuth):
        masked_token = ""
        if auth.token and len(auth.token) >= 8:
            masked_token = auth.token[:4] + "*" * (len(auth.token) - 8) + auth.token[-4:]
        elif auth.token:
            masked_token = "*" * len(auth.token)

        print("\n" + "─" * 50)
        print("SETTINGS")
        print("─" * 50)
        print(f"  Server URL:  {auth.server_url if auth.server_url else 'Not set'}")
        print(f"  Token:       {masked_token if auth.token else 'Not set'}")
        print("─" * 50)
        print("  1. Full Reset")
        print("  0. Back to Main Menu")
        print("=" * 50)

    @staticmethod
    def confirm_reset() -> bool:
        print("\n[!] WARNING: This will delete all configuration data.")
        confirm = input("Are you sure? (yes/no): ").strip().lower()
        return confirm == "yes"

    @staticmethod
    def show_about():
        print("\n" + "─" * 50)
        print("ABOUT")
        print("─" * 50)
        print(f"  {ConfigManager.APP_FULL_NAME}")
        print("  CLI tool for batch synchronization of Forgejo repositories")
        print("")
        print("  Author:     Alexander Suvorov")
        print("  GitHub:     https://github.com/smartlegionlab")
        print("  Repository: https://github.com/smartlegionlab/forgejo-sync-manager")
        print("  License:    BSD 3-Clause")
        print("  Disclaimer: https://github.com/smartlegionlab/forgejo-sync-manager/blob/master/DISCLAIMER.md")
        print("─" * 50)
        input("\nPress Enter to continue...")
