import sys
import os
from ui.console import ConsoleUI
from core.auth import ForgejoAuth
from core.api_client import ForgejoAPIClient
from core.sync_manager import SyncManager
import requests


def restart_app():
    python = sys.executable
    os.execl(python, python, *sys.argv)


def test_server_connection(server_url: str):
    test_auth = ForgejoAuth(server_url=server_url)
    test_client = ForgejoAPIClient(test_auth)
    test_client.test_connection()
    return True


def test_auth_connection(auth: ForgejoAuth):
    client = ForgejoAPIClient(auth)
    client.test_connection()
    client.get_user_info()
    return True


def main():
    ui = ConsoleUI()
    ui.show_welcome()

    ui.show_phase(1, "Directory Structure Check")
    config_manager = ui.config_manager
    ui.show_success(f"Application directory: {config_manager.app_dir}")

    ui.show_phase(2, "Configuration Loading")
    existing_config = config_manager.load()

    if existing_config and existing_config.get("token"):
        ui.show_success("Configuration file found")
        auth = ForgejoAuth(
            token=existing_config.get("token", ""),
            server_url=existing_config.get("server_url", "")
        )
    else:
        ui.show_info("No configuration found")
        auth = None

    while True:
        if not auth or not auth.is_configured():
            while True:
                ui.show_phase(3, "Server Connection Test")
                server_url = ui.prompt_server_url()

                try:
                    test_server_connection(server_url)
                    ui.show_success(f"Connected to {server_url}")
                    auth = ForgejoAuth(server_url=server_url)
                    break
                except requests.exceptions.ConnectionError:
                    ui.show_error(f"Cannot connect to {server_url}")
                    choice = ui.prompt_retry_server()
                    if choice == "2":
                        ui.show_info("Exiting...")
                        sys.exit(0)
                    continue
                except Exception as e:
                    ui.show_error(f"Server error: {e}")
                    choice = ui.prompt_retry_server()
                    if choice == "2":
                        ui.show_info("Exiting...")
                        sys.exit(0)
                    continue

            while True:
                ui.show_phase(4, "Authentication Test")
                token = ui.prompt_token()

                auth.token = token

                try:
                    test_auth_connection(auth)
                    ui.show_success("Authentication successful")
                    break
                except requests.exceptions.HTTPError as e:
                    ui.show_error(f"Authentication failed: {e}")
                    choice = ui.prompt_retry_auth()
                    if choice == "2":
                        ui.show_info("Exiting...")
                        sys.exit(0)
                    continue
                except Exception as e:
                    ui.show_error(f"Connection error: {e}")
                    choice = ui.prompt_retry_auth()
                    if choice == "2":
                        ui.show_info("Exiting...")
                        sys.exit(0)
                    continue

            try:
                client = ForgejoAPIClient(auth)
                user_info = client.get_user_info()
                repos = client.get_user_repos()

                ui.save_auth(auth)
                ui.show_success("Configuration saved")

                ui.show_phase(5, "Connection Summary")
                ui.show_connection_status(auth, user_info)
                break

            except Exception as e:
                ui.show_error(f"Failed to fetch data: {e}")
                sys.exit(1)
        else:
            try:
                client = ForgejoAPIClient(auth)
                client.test_connection()
                user_info = client.get_user_info()
                repos = client.get_user_repos()

                ui.show_success("Authentication successful")

                ui.show_phase(3, "Connection Summary")
                ui.show_connection_status(auth, user_info)
                break

            except requests.exceptions.ConnectionError:
                ui.show_error("Server connection failed")
                auth = None
                continue
            except requests.exceptions.HTTPError:
                ui.show_error("Token invalid or expired")
                auth = None
                continue
            except Exception as e:
                ui.show_error(f"Connection error: {e}")
                sys.exit(1)

    while True:
        ui.show_main_menu()
        choice = ui.get_menu_choice()

        if choice == "1":
            ui.show_user_info(user_info)
        elif choice == "2":
            ui.show_repo_statistics(repos)

            while True:
                ui.show_repo_menu()
                repo_choice = ui.get_menu_choice()

                if repo_choice == "1":
                    print("\n" + "─" * 50)
                    print("SYNCHRONIZING REPOSITORIES")
                    print("─" * 50)

                    sync_manager = SyncManager(auth)
                    results = sync_manager.sync_all_repositories(repos)

                    ui.show_sync_results(results)

                    input("\nPress Enter to continue...")
                elif repo_choice == "2":
                    print("\n" + "─" * 50)
                    print("RECLONING REPOSITORIES")
                    print("─" * 50)

                    sync_manager = SyncManager(auth)
                    results = sync_manager.reclone_all_repositories(repos)

                    ui.show_reclone_results(results)

                    input("\nPress Enter to continue...")
                elif repo_choice == "0":
                    break
                else:
                    ui.show_error("Invalid option")
        elif choice == "3":
            while True:
                ui.show_settings(auth)
                settings_choice = ui.get_menu_choice()

                if settings_choice == "1":
                    if ui.confirm_reset():
                        config_manager.reset()
                        ui.show_info("Configuration reset. Restarting...")
                        restart_app()
                    else:
                        ui.show_info("Reset cancelled")
                elif settings_choice == "0":
                    break
                else:
                    ui.show_error("Invalid option")
        elif choice == "0":
            ui.show_info("Goodbye!")
            sys.exit(0)
        else:
            ui.show_error("Invalid option")


if __name__ == "__main__":
    main()
