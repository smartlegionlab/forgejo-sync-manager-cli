import sys
from ui.console import ConsoleUI
from core.auth import ForgejoAuth
from core.api_client import ForgejoAPIClient
import requests


def main():
    ui = ConsoleUI()
    ui.show_welcome()

    ui.show_phase(1, "Directory Structure Check")
    config_manager = ui.config_manager
    ui.show_success(f"Application directory: {config_manager.app_dir}")

    ui.show_phase(2, "Configuration Loading")
    existing_config = config_manager.load()

    if existing_config and existing_config.get("username"):
        ui.show_success("Configuration file found")
        auth = ForgejoAuth(
            username=existing_config.get("username", ""),
            token=existing_config.get("token", ""),
            server_url=existing_config.get("server_url", "")
        )
    else:
        ui.show_info("No configuration found")
        auth = None

    while True:
        if not auth or not auth.is_configured():
            ui.show_info("Authentication required")
            auth = ui.prompt_for_auth()

            try:
                client = ForgejoAPIClient(auth)
                client.test_connection()
                user_info = client.get_user_info()

                ui.save_auth(auth)
                ui.show_success("Authentication successful")

                ui.show_phase(3, "Connection Summary")
                ui.show_connection_status(auth, user_info)
                break

            except requests.exceptions.HTTPError as e:
                ui.show_error(f"Authentication failed: {e}")
                choice = ui.prompt_retry_or_exit()
                if choice == "2":
                    ui.show_info("Exiting...")
                    sys.exit(0)
                auth = None
                continue
            except Exception as e:
                ui.show_error(f"Connection error: {e}")
                sys.exit(1)
        else:
            try:
                client = ForgejoAPIClient(auth)
                client.test_connection()
                user_info = client.get_user_info()

                ui.show_success("Authentication successful")

                ui.show_phase(3, "Connection Summary")
                ui.show_connection_status(auth, user_info)
                break

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
        elif choice == "0":
            ui.show_info("Goodbye!")
            sys.exit(0)
        else:
            ui.show_error("Invalid option")


if __name__ == "__main__":
    main()
