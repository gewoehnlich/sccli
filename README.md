# sccli

sccli.gewoehnlich.org
useful links:
  https://developers.soundcloud.com/docs/api/explorer/open-api#/
  https://developers.soundcloud.com/docs/api/guide

tech:
python:latest
aiohttp, asyncio
ffmpeg
typer: https://github.com/fastapi/typer
rich: https://github.com/Textualize/rich
textual: https://github.com/Textualize/textual
pydantic: https://docs.pydantic.dev/latest/
pytest & pytest-asyncio: For testing.
.venv
pip
poetry + pyproject.toml
pyright | mypy
black code formatter
PEP-8 Styling Guide
loguru: https://github.com/Delgan/loguru
python-dotenv
alive-progress: https://github.com/rsalmei/alive-progress
ruff or flake8
pip-audit: https://pypi.org/project/pip-audit/
safety: https://github.com/pyupio/safety
pre-commit hooks

    1 sccli/
    2 ├── .env                  # Environment variables (API keys, etc.)
    3 ├── .gitignore            # Standard Python gitignore
    4 ├── pyproject.toml        # Poetry project configuration and dependencies
    5 ├── README.md             # Project documentation
    6 │
    7 ├── src/
    8 │   └── sccli/
    9 │       ├── init.py
   10 │       ├── main.py             # Main application entry point (boots the CLI)
   11 │       │
   12 │       ├── containers/
   13 │       │   ├── init.py
   14 │       │   │
   15 │       │   ├── track/
   16 │       │   │   ├── init.py
   17 │       │   │   ├── actions/
   18 │       │   │   │   └── download_track_action.py  # The "Use Case" logic
   19 │       │   │   ├── data/
   20 │       │   │   │   └── track_dto.py              # Pydantic model for a track
   21 │       │   │   ├── clients/
   22 │       │   │   │   └── soundcloud_api_client.py  # Logic to call SoundCloud's track endpoints
   23 │       │   │   └── exceptions/
   24 │       │   │       └── track_not_found.py        # Custom exceptions for this container
   25 │       │   │
   26 │       │   ├── playlist/
   27 │       │   │   └── ... (similar structure: actions, data, clients)
   28 │       │   │
   29 │       │   └── search/
   30 │       │       └── ... (similar structure)
   31 │       │
   32 │       ├── ship/
   33 │       │   ├── init.py
   34 │       │   └── console/
   35 │       │       ├── init.py
   36 │       │       ├── main.py             # Creates and configures the Typer app instance
   37 │       │       └── commands.py         # Defines all Typer CLI commands (e.g., download, `search`)
   38 │       │
   39 │       └── support/
   40 │           ├── init.py
   41 │           ├── config.py           # Pydantic settings management to load .env
   42 │           ├── http_client.py      # A reusable async HTTP client wrapper for aiohttp
   43 │           └── ui.py               # Helper functions for Rich (e.g., print_table)
   44 │
   45 └── tests/
   46     ├── containers/
   47     │   └── track/
   48     │       └── test_download_track_action.py
   49     └── ... (test structure mirrors the src structure)
