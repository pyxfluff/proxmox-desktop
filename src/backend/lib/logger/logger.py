# pyxfluff 2025-2026
# from Nanofox-Dev

from time import time
from math import floor

from backend import console


class Logger:
    def __init__(self, thread_name: str = "StdLog"):
        self.thread = thread_name

    def _print(self, message: str):
        console.print(f"[{floor(time() * 10000) / 10000}] [purple][{self.thread}][/] {message}")

    def log(self, message: str):
        self._print(f"[blue]\\[i] {message}[/]")
        return self

    def success(self, message: str):
        self._print(f"[green][✓] {message}[/]")
        return self

    def warn(self, message: str):
        self._print(f"[yellow][!] {message}[/]")
        return self

    def error(self, message: str):
        self._print(f"[red][✖] {message}[/]")
        return self
