# core/sync_manager_cli.py
# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# License: BSD 3-Clause
import shutil
import subprocess
from datetime import datetime
from core.base_sync_manager import BaseSyncManager


class CLISyncManager(BaseSyncManager):
    def check_repo_needs_update(self, repo):
        repo_name = repo['name']
        repo_path = self.repos_dir / repo_name

        if not repo_path.exists():
            return True

        try:
            authenticated_url = self.get_authenticated_url(repo['clone_url'])

            subprocess.run(['git', '-C', str(repo_path), 'remote', 'set-url', 'origin', authenticated_url],
                           check=True, capture_output=True, text=True, timeout=10)

            subprocess.run(['git', '-C', str(repo_path), 'fetch', 'origin', 'HEAD'],
                           check=True, capture_output=True, text=True, timeout=30)

            local_hash = subprocess.run(['git', '-C', str(repo_path), 'rev-parse', 'HEAD'],
                                        check=True, capture_output=True, text=True, timeout=10).stdout.strip()

            remote_hash = subprocess.run(['git', '-C', str(repo_path), 'rev-parse', 'FETCH_HEAD'],
                                         check=True, capture_output=True, text=True, timeout=10).stdout.strip()

            return local_hash != remote_hash
        except:
            return True

    def check_updates(self, repos):
        needing_update = []
        total = len(repos)

        print(f"\nChecking {total} repositories...")

        for idx, repo in enumerate(repos, 1):
            if self.check_repo_needs_update(repo):
                needing_update.append(repo)

            if idx % 50 == 0 or idx == total:
                print(f"  Progress: {idx}/{total}")

        return needing_update

    def _sync_repository_with_progress(self, repo, current_index, total, failed_count):
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

    def _sync_repository_update_only_with_progress(self, repo, current_index, total, failed_count):
        repo_name = repo['name']
        clone_url = repo['clone_url']
        authenticated_url = self.get_authenticated_url(clone_url)
        repo_path = self.repos_dir / repo_name

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        progress = f"[{current_index}/{total}/{failed_count}]"

        if not repo_path.exists():
            try:
                subprocess.run(['git', 'clone', authenticated_url, str(repo_path)],
                               check=True, capture_output=True, text=True)
                print(f"{progress} [{timestamp}] {repo_name} - CLONED")
                return "CLONED"
            except subprocess.CalledProcessError as e:
                print(f"{progress} [{timestamp}] {repo_name} - FAILED: {e.stderr}")
                return "FAILED"
        else:
            try:
                subprocess.run(['git', '-C', str(repo_path), 'remote', 'set-url', 'origin', authenticated_url],
                               check=True, capture_output=True, text=True)
                subprocess.run(['git', '-C', str(repo_path), 'pull'],
                               check=True, capture_output=True, text=True)
                print(f"{progress} [{timestamp}] {repo_name} - UPDATED")
                return "UPDATED"
            except subprocess.CalledProcessError as e:
                print(f"{progress} [{timestamp}] {repo_name} - FAILED: {e.stderr}")
                return "FAILED"

    def _reclone_repository_with_progress(self, repo, current_index, total, failed_count):
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

        results = {"cloned": 0, "updated": 0, "failed": 0}
        total = len(repos)

        for idx, repo in enumerate(repos, 1):
            status = self._sync_repository_with_progress(repo, idx, total, results["failed"])
            if status == "CLONED":
                results["cloned"] += 1
            elif status == "UPDATED":
                results["updated"] += 1
            else:
                results["failed"] += 1

        return results

    def sync_updates_only(self, repos_to_update):
        self.ensure_directories()

        results = {"cloned": 0, "updated": 0, "failed": 0}
        total = len(repos_to_update)

        for idx, repo in enumerate(repos_to_update, 1):
            status = self._sync_repository_update_only_with_progress(repo, idx, total, results["failed"])
            if status == "CLONED":
                results["cloned"] += 1
            elif status == "UPDATED":
                results["updated"] += 1
            else:
                results["failed"] += 1

        return results

    def reclone_all_repositories(self, repos):
        self.ensure_directories()

        results = {"cloned": 0, "recloned": 0, "failed": 0}
        total = len(repos)

        for idx, repo in enumerate(repos, 1):
            status = self._reclone_repository_with_progress(repo, idx, total, results["failed"])
            if status == "CLONED":
                results["cloned"] += 1
            elif status == "RECLONED":
                results["recloned"] += 1
            else:
                results["failed"] += 1

        return results
