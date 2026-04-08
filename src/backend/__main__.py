# pyxfluff 2026

from backend import console, config

console.print("[yellow]Loading routes[/]")

#config.get_keyring()

from backend.lib.pmx import ProxmoxServer

#ProxmoxServer(hostname="r730xd").populate(ip="10.25.0.6", token="root@pam!ProxmoxDesktop2", secret="redacted", url="https://10.25.0.6:8006")

server = ProxmoxServer(hostname="r730xd")
