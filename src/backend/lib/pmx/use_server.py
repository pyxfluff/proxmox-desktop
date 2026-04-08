# pyxfluff 2026

import os
import httpx
import orjson

from pathlib import Path
from backend import config
from backend.lib.logger import Logger

log = Logger("ProxmoxConnection")


class ProxmoxServer:
    servers: dict
    found = False
    hostname: str
    api_prefix = "/api2/json"
    client: httpx.Client

    def build_client(self, token: str):
        log.log(f"generating HttpClient with base_url={self.server['url']}{self.api_prefix}")
        return httpx.Client(
            base_url=f"{self.server['url']}{self.api_prefix}",
            verify=not config.ssl.ignore,  # type: ignore
            headers={"Authorization": f"PVEAPIToken={self.server['token']}={token}"},
            # timeout=10.0
        )

    def __init__(self, hostname: str):
        log.log("hai :3")
        data_dir = Path(__file__).parent / "Store"

        self.hostname = hostname

        if not data_dir.is_dir():
            log.warn("Data path not created. Creating indexes.")

            data_dir.mkdir()
            (data_dir / "servers.json").write_text('{"servers": {}}')

            log.success(
                "Indexes loaded. However, there are currently no servers to be displayed."
            )

        self.servers = orjson.loads((data_dir / "servers.json").read_text()).get("servers", {})

        log.log(f"Got servers: {self.servers}")

        if not self.servers.get(hostname):
            log.warn(
                f"Server {hostname} is not currently in our database! Please run `ProxmoxServer().populate()` to save this server."
            )
        else:
            self.found = True
            self.server = self.servers[self.hostname]
            self.client = self.build_client(config.get_server_key(hostname)["key"])

    def populate(self, ip: str, token: str, url: str, secret: str):
        log.log("Saving server credentials")

        if self.found:
            log.warn("Ignoring populate call because this is already a valid server!")
            return

        self.server = {"ip": ip, "url": url, "token": token}
        self.servers[self.hostname] = self.server
        config.add_server_to_keyring(self.hostname, secret)

        (Path(__file__).parent / "Store/servers.json").write_text(
            orjson.dumps({"servers": self.servers}).decode()
        )

        log.success("Added!").log("Testing connection...")

        self.client = self.build_client(config.get_server_key(self.hostname)["key"])

        print(self.test_connection())

    def test_connection(self):
        try:
            r = self.client.get("/version").raise_for_status().json()

            log.success(f"Successfully connected to Proxmox at {self.server["url"]}, Proxmox VE {r["data"]["version"]}")

            return True
        except httpx.HTTPError:
            log.error(f"could not connect to {self.server["url"]}, is it online? are your credentials correct?")

            return False
