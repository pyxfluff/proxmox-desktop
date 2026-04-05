# pyxfluff 2026

import orjson
import keyring

from pathlib import Path
from rich.console import Console

from fastapi import FastAPI

console = Console(force_terminal=True)


# load config
class AppConfig:
    def __init__(self):
        try:
            # this assumes our working directory is the project root, will 100% cause problems later
            for k, v in orjson.loads(
                (Path(__file__).parent / "backend_config.jsonc").read_text()
            ).items():
                setattr(self, k, v)
        except FileNotFoundError:
            console.print(
                "[red]App config not found. Please make sure backend_config.jsonc exists.[/]"
            )
            exit(1)


config = AppConfig()

app = FastAPI(debug=True, title="Proxmox Desktop", description="Backend API wrapper")


console.print("[green]App loaded[/]")
