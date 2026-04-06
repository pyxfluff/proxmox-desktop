# pyxfluff 2026

import orjson
import keyring

from pathlib import Path
from rich.console import Console

from fastapi import FastAPI

console = Console(force_terminal=True)

console.print("[yellow]Backend worker starting, loading AppConfig model[/]")


# load config
class AppConfig:
    def __init__(self):
        try:
            for k, v in orjson.loads(
                (Path(__file__).parent / "backend_config.jsonc").read_text()
            ).items():
                obj = self
                for part in k.split(".")[:-1]:
                    if not hasattr(obj, part):
                        setattr(obj, part, type("", (), {})())

                    obj = getattr(obj, part)

                setattr(obj, k.split(".")[-1], v)
        except FileNotFoundError:
            console.print(
                "[red]App config not found. Please make sure backend_config.jsonc exists.[/]"
            )
            exit(1)

    def get_keyring(self):
        return orjson.loads(
            keyring.get_password(
                f"proxmox_desktop_{self.keyring.name}", self.keyring.user
            )
            or '{"is_initialized": false}'
        )

    def add_server_to_keyring(
        self, hostname: str, endpoint: str, token: str, secret: str
    ):
        ring = self.get_keyring()

        if ring["is_initialized"] == False:
            ring = {"is_initialized": True, "servers": {}, "_version": 1}

        ring["servers"][hostname] = {
            "endpoint": endpoint,
            "token": token,
            "secret": secret
        }

        keyring.set_password(f"proxmox_desktop_{self.keyring.name}", self.keyring.user, orjson.dumps(ring).decode())


config = AppConfig()

console.print("[yellow]Initializing FastAPI[/]")

app = FastAPI(debug=True, title="Proxmox Desktop", description="Backend API wrapper")


console.print("[green]App loaded, handing off[/]")
