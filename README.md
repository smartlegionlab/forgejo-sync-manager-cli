# forgejo-sync-manager <sup>v1.0.2</sup>

CLI tool for batch synchronization of Forgejo repositories to local machine.

---

[![GitHub top language](https://img.shields.io/github/languages/top/smartlegionlab/forgejo-sync-manager-cli)](https://github.com/smartlegionlab/forgejo-sync-manager-cli)
[![GitHub license](https://img.shields.io/github/license/smartlegionlab/forgejo-sync-manager-cli)](https://github.com/smartlegionlab/forgejo-sync-manager-cli/blob/master/LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/smartlegionlab/forgejo-sync-manager-cli)](https://github.com/smartlegionlab/forgejo-sync-manager-cli/)
[![GitHub stars](https://img.shields.io/github/stars/smartlegionlab/forgejo-sync-manager-cli?style=social)](https://github.com/smartlegionlab/forgejo-sync-manager-cli/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/smartlegionlab/forgejo-sync-manager-cli?style=social)](https://github.com/smartlegionlab/forgejo-sync-manager-cli/network/members)

---

## ⚠️ Disclaimer

**By using this software, you agree to the full disclaimer terms.**

**Summary:** Software provided "AS IS" without warranty. You assume all risks.

**Full legal disclaimer:** See [DISCLAIMER.md](https://github.com/smartlegionlab/forgejo-sync-manager-cli/blob/master/DISCLAIMER.md)

---

## Features

- Automatic authentication via personal access token
- Repository cloning and updating with progress tracking
- Update detection via commit hash comparison
- Full repository recloning option
- Parallel progress display for large repository sets
- Persistent configuration storage

## Requirements

- Python 3.8+
- Git
- Forgejo server with API access

## Installation

```bash
git clone https://github.com/smartlegionlab/forgejo-sync-manager-cli.git
cd forgejo-sync-manager-cli
python -m venv venv
source venv/bin/activate
python app.py
```

## Usage

```bash
python app.py
```

## Configuration

On first run, the tool will guide you through:

1. Server URL (e.g., `http://localhost:3000`)
2. Personal access token with `read:repository` and `read:user` scopes

Configuration is stored in `~/forgejo-sync-manager/config.json`

### Main Menu

- `1` - Display user information
- `2` - Repository operations
- `3` - Settings (full reset)
- `4` - About (author, repository, license, disclaimer)
- `0` - Exit

### Repository Menu

- `1` - Show statistics (total, public, private, forks)
- `2` - List all repositories with names, types, and sizes
- `3` - Check for updates (compares local and remote commit hashes)
- `4` - Sync all repositories (clone missing, pull existing)
- `5` - Reclone all repositories (delete and fresh clone)
- `0` - Back to main menu

## How It Works

1. **Authentication**: Token-based authentication via Forgejo API
2. **Repository Discovery**: Fetches complete repository list with pagination (50 per page)
3. **Update Detection**: For each existing repository, executes `git fetch` and compares `HEAD` with `FETCH_HEAD`
4. **Sync Operations**: Uses authenticated URLs with embedded token for Git operations
5. **Directory Structure**: `~/forgejo-sync-manager/{username}/repositories/`

## License

[BSD 3-Clause License](LICENSE)

Copyright (©) 2026, [Alexander Suvorov](https://github.com/smartlegionlab)
All rights reserved.

## Powered By

This application is built on top of:

| Library                                                                                      | Description                                                   | Version |
|----------------------------------------------------------------------------------------------|---------------------------------------------------------------|---------|
| **[forgejo-sync-manager-core](https://github.com/smartlegionlab/forgejo-sync-manager-core)** | Universal core library for Forgejo repository synchronization | v1.0.0  |
| **requests**                                                                                 | HTTP library for Python                                       | ≥2.31.0 |

## Related Projects

| Project                       | Description                             | Repository                                                            |
|-------------------------------|-----------------------------------------|-----------------------------------------------------------------------|
| **forgejo-sync-manager-gui**  | Desktop GUI application with dark theme | [GitHub](https://github.com/smartlegionlab/forgejo-sync-manager-gui)  |
| **forgejo-sync-manager-core** | Universal core library                  | [GitHub](https://github.com/smartlegionlab/forgejo-sync-manager-core) |

## See Also

- **[forgejo-sync-manager-gui](https://github.com/smartlegionlab/forgejo-sync-manager-gui)** - If you prefer graphical interface
- **[forgejo-sync-manager-core](https://github.com/smartlegionlab/forgejo-sync-manager-core)** - Core library for custom implementations