# pyxfluff 2026

import orjson
import keyring

from pathlib import Path
from rich.console import Console

from fastapi import FastAPI

console = Console(force_terminal=True)

from .lib.logger import Logger

log = Logger("InitThread")

log.warn("Backend worker starting, loading AppConfig model")


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
            log.error(
                "App config not found. Please make sure backend_config.jsonc exists."
            )
            exit(1)

    def get_server_key(self, hostname):
        log.log(f"Accessing keyring prop={hostname}")

        return orjson.loads(
            keyring.get_password(
                f"proxmox_desktop_{self.keyring.name}", hostname  # type: ignore
            )
            or '{"found": false}'
        )

    def add_server_to_keyring(self, hostname: str, secret: str):
        log.log(f"Setting keyring prop={hostname}")
        keyring.set_password(
            f"proxmox_desktop_{self.keyring.name}", hostname, orjson.dumps({"found": True, "key": secret}).decode()  # type: ignore
        )

        return True


config = AppConfig()

log.warn("Initializing FastAPI")

app = FastAPI(debug=True, title="Proxmox Desktop", description="Backend API wrapper")


log.success("App loaded, handing off")
