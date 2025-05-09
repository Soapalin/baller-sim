from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static



class NewSaveScreen(Screen):
    CSS_PATH = "baller_sim.tcss"
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        self.baller_title = Static("New Save", classes="title")
        self.baller_subtitle = Static("A football managerial career mode simulation", classes="subtitle")
        yield self.baller_title
        yield self.baller_subtitle