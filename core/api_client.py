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

    def get_user_repos(self):
        all_repos = []
        page = 1
        page_size = 50

        while True:
            url = f"{self.auth.get_api_url()}/user/repos"
            params = {
                'page': page,
                'limit': page_size
            }
            response = self.session.get(url, params=params)
            response.raise_for_status()
            repos = response.json()

            if not repos:
                break

            all_repos.extend(repos)

            if len(repos) < page_size:
                break

            page += 1

        return all_repos
