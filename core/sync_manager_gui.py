# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# License: BSD 3-Clause
from core.base_sync_manager import BaseSyncManager


class GUISyncManager(BaseSyncManager):
    def check_repo_needs_update(self, repo):
        raise NotImplementedError("Not needed in GUI")

    def check_updates(self, repos):
        raise NotImplementedError("Not needed in GUI")

    def sync_all_repositories(self, repos):
        raise NotImplementedError("Use sync_repository in loop with progress signal")

    def sync_updates_only(self, repos_to_update):
        raise NotImplementedError("Use sync_repository in loop with progress signal")

    def reclone_all_repositories(self, repos):
        raise NotImplementedError("Use reclone_repository in loop with progress signal")
