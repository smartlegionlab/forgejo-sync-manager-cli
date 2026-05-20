import subprocess
import shutil
from datetime import datetime
from pathlib import Path
from core.auth import ForgejoAuth


class SyncManager:
    def __init__(self, auth: ForgejoAuth):
        self.auth = auth
        self.base_dir = Path.home() / "forgejo-sync"
        self.repos_dir = self.base_dir / "repositories"

    def ensure_directories(self):
        self.base_dir.mkdir(exist_ok=True)
        self.repos_dir.mkdir(exist_ok=True)
        return self.repos_dir

    def get_authenticated_url(self, clone_url: str):
        from urllib.parse import urlparse
        parsed = urlparse(clone_url)
        authenticated_url = f"{parsed.scheme}://{self.auth.token}@{parsed.netloc}{parsed.path}"
        return authenticated_url

    def sync_repository(self, repo, current_index: int, total: int, failed_count: int):
        repo_name = repo['name']
        clone_url = repo['clone_url']
        authenticated_url = self.get_authenticated_url(clone_url)
        repo_path = self.repos_dir / repo_name

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        progress = f"[{current_index}/{total}/{failed_count}]"

        if repo_path.exists():
            try:
                subprocess.run(['git', '-C', str(repo_path), 'remote', 'set-url', 'origin', authenticated_url],
                               check=True, capture_output=True, text=True)
                subprocess.run(['git', '-C', str(repo_path), 'fetch'],
                               check=True, capture_output=True, text=True)
                subprocess.run(['git', '-C', str(repo_path), 'pull'],
                               check=True, capture_output=True, text=True)
                print(f"{progress} [{timestamp}] {repo_name} - UPDATED")
                return "UPDATED"
            except subprocess.CalledProcessError as e:
                print(f"{progress} [{timestamp}] {repo_name} - FAILED: {e.stderr}")
                return "FAILED"
        else:
            try:
                subprocess.run(['git', 'clone', authenticated_url, str(repo_path)],
                               check=True, capture_output=True, text=True)
                print(f"{progress} [{timestamp}] {repo_name} - CLONED")
                return "CLONED"
            except subprocess.CalledProcessError as e:
                print(f"{progress} [{timestamp}] {repo_name} - FAILED: {e.stderr}")
                return "FAILED"

    def reclone_repository(self, repo, current_index: int, total: int, failed_count: int):
        repo_name = repo['name']
        clone_url = repo['clone_url']
        authenticated_url = self.get_authenticated_url(clone_url)
        repo_path = self.repos_dir / repo_name

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        progress = f"[{current_index}/{total}/{failed_count}]"

        if repo_path.exists():
            try:
                shutil.rmtree(repo_path)
                subprocess.run(['git', 'clone', authenticated_url, str(repo_path)],
                               check=True, capture_output=True, text=True)
                print(f"{progress} [{timestamp}] {repo_name} - RECLONED")
                return "RECLONED"
            except Exception as e:
                print(f"{progress} [{timestamp}] {repo_name} - FAILED: {e}")
                return "FAILED"
        else:
            try:
                subprocess.run(['git', 'clone', authenticated_url, str(repo_path)],
                               check=True, capture_output=True, text=True)
                print(f"{progress} [{timestamp}] {repo_name} - CLONED")
                return "CLONED"
            except subprocess.CalledProcessError as e:
                print(f"{progress} [{timestamp}] {repo_name} - FAILED: {e.stderr}")
                return "FAILED"

    def sync_all_repositories(self, repos):
        self.ensure_directories()

        results = {
            "cloned": 0,
            "updated": 0,
            "failed": 0
        }

        total = len(repos)

        for idx, repo in enumerate(repos, 1):
            status = self.sync_repository(repo, idx, total, results["failed"])
            if status == "CLONED":
                results["cloned"] += 1
            elif status == "UPDATED":
                results["updated"] += 1
            else:
                results["failed"] += 1

        return results

    def reclone_all_repositories(self, repos):
        self.ensure_directories()

        results = {
            "cloned": 0,
            "recloned": 0,
            "failed": 0
        }

        total = len(repos)

        for idx, repo in enumerate(repos, 1):
            status = self.reclone_repository(repo, idx, total, results["failed"])
            if status == "CLONED":
                results["cloned"] += 1
            elif status == "RECLONED":
                results["recloned"] += 1
            else:
                results["failed"] += 1

        return results
