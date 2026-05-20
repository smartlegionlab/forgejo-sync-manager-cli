from ui.console import ConsoleUI
from core.auth import ForgejoAuth


def main():
    ui = ConsoleUI()
    ui.show_welcome()

    existing_config = ui.config_manager.load()

    auth = ForgejoAuth(
        username=existing_config.get("username", ""),
        token=existing_config.get("token", ""),
        server_url=existing_config.get("server_url", "")
    )

    if not auth.is_configured():
        print("\n[!] Forgejo connection data not found.")
        auth = ui.prompt_for_auth()
        ui.save_auth(auth)

    ui.show_config_status(auth)


if __name__ == "__main__":
    main()
