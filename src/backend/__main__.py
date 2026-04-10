# pyxfluff 2026

from pathlib import Path
from importlib import import_module

from backend import config, app
from backend.lib.logger import Logger

logger = Logger("Main")

logger.log("Loading routes")

for route in (Path(__file__).parent / "routes").rglob("*.py"):
    mod = route.relative_to(Path(__file__).parent).with_suffix("")
    mod = f"backend.{".".join(mod.parts)}"

    logger.log(f"Importing route module {mod}")
    route = import_module(mod)

    try:
        if route.router:
            app.include_router(route.router)
    except (ImportError, AttributeError):
        logger.error(
            f"Module {mod} is missing name `router`; make sure it has a valid APIRouter or move it outside of the routes folder"
        )

# config.get_keyring()

from backend.lib.pmx import ProxmoxServer

# ProxmoxServer(hostname="r730xd").populate(ip="10.25.0.6", token="root@pam!ProxmoxDesktop2", secret="redacted", url="https://10.25.0.6:8006")

server = ProxmoxServer(hostname="r730xd")
