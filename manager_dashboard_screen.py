from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static
import baller_database

class ManagerDashboardScreeen(Screen):
    def on_mount(self) -> None:
        pass

    def compose(self) -> ComposeResult:
        yield Static(f"Manager Dashboard - {baller_database.CURRENT_MANAGER.name}")
