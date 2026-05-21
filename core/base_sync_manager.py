# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# License: BSD 3-Clause
import subprocess
import shutil
from pathlib import Path
from abc import ABC, abstractmethod
from core.auth import ForgejoAuth


class BaseSyncManager(ABC):
    def __init__(self, auth: ForgejoAuth):
        self.auth = auth
        self.base_dir = Path.home() / "forgejo-sync-manager" / auth.username
        self.repos_dir = self.base_dir / "repositories"

    def ensure_directories(self):
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.repos_dir.mkdir(parents=True, exist_ok=True)
        return self.repos_dir

    def get_authenticated_url(self, clone_url: str):
        from urllib.parse import urlparse
        parsed = urlparse(clone_url)
        authenticated_url = f"{parsed.scheme}://{self.auth.token}@{parsed.netloc}{parsed.path}"
        return authenticated_url

    def sync_repository(self, repo):
        repo_name = repo['name']
        clone_url = repo['clone_url']
        authenticated_url = self.get_authenticated_url(clone_url)
        repo_path = self.repos_dir / repo_name

        if repo_path.exists():
            try:
                subprocess.run(['git', '-C', str(repo_path), 'remote', 'set-url', 'origin', authenticated_url],
                               check=True, capture_output=True, text=True)
                subprocess.run(['git', '-C', str(repo_path), 'fetch'],
                               check=True, capture_output=True, text=True)
                subprocess.run(['git', '-C', str(repo_path), 'pull'],
                               check=True, capture_output=True, text=True)
                return "UPDATED"
            except subprocess.CalledProcessError:
                return "FAILED"
        else:
            try:
                subprocess.run(['git', 'clone', authenticated_url, str(repo_path)],
                               check=True, capture_output=True, text=True)
                return "CLONED"
            except subprocess.CalledProcessError:
                return "FAILED"

    def reclone_repository(self, repo):
        repo_name = repo['name']
        clone_url = repo['clone_url']
        authenticated_url = self.get_authenticated_url(clone_url)
        repo_path = self.repos_dir / repo_name

        if repo_path.exists():
            try:
                shutil.rmtree(repo_path)
                subprocess.run(['git', 'clone', authenticated_url, str(repo_path)],
                               check=True, capture_output=True, text=True)
                return "RECLONED"
            except Exception:
                return "FAILED"
        else:
            try:
                subprocess.run(['git', 'clone', authenticated_url, str(repo_path)],
                               check=True, capture_output=True, text=True)
                return "CLONED"
            except subprocess.CalledProcessError:
                return "FAILED"

    def get_repo_path(self, repo_name: str) -> Path:
        return self.repos_dir / repo_name

    def repo_exists_locally(self, repo_name: str) -> bool:
        repo_path = self.repos_dir / repo_name
        return repo_path.exists() and (repo_path / '.git').exists()

    @abstractmethod
    def sync_all_repositories(self, repos):
        pass

    @abstractmethod
    def sync_updates_only(self, repos_to_update):
        pass

    @abstractmethod
    def reclone_all_repositories(self, repos):
        pass

    @abstractmethod
    def check_repo_needs_update(self, repo):
        pass

    @abstractmethod
    def check_updates(self, repos):
        pass
