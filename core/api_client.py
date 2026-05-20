import requests
from core.auth import ForgejoAuth


class ForgejoAPIClient:
    def __init__(self, auth: ForgejoAuth):
        self.auth = auth
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"token {auth.token}",
            "Accept": "application/json"
        })

    def test_connection(self):
        url = f"{self.auth.get_api_url()}/version"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_user_info(self):
        url = f"{self.auth.get_api_url()}/user"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
