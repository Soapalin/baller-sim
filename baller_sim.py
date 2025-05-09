from textual.app import App, ComposeResult
from textual import events
from textual.widgets import Button, Label, Header, Static, Tree
from new_save_screen import NewSaveScreen

BALLER_SIM_BANNER = r"""
 ____        _ _             ____  _
| __ )  __ _| | | ___ _ __  / ___|(_)_ __ ___
|  _ \ / _` | | |/ _ \ '__| \___ \| | '_ ` _ \
| |_) | (_| | | |  __/ |     ___) | | | | | | |
|____/ \__,_|_|_|\___|_|    |____/|_|_| |_| |_|
"""

COLORS = [
    "white",
    "maroon",
    "red",
    "purple",
    "fuchsia",
    "olive",
    "yellow",
    "navy",
    "teal",
    "aqua",
]

class BallerSim(App[str]): # [str] is the type returned at the exit
    CSS_PATH = "baller_sim.tcss"
    TITLE = 'Baller Sim'
    SUB_TITLE = "A football managerial career mode simulation"
    # SCREENS = {"new_save": NewSaveScreen}
    # BINDINGS = [("n", "push_screen('new_save')", "NewSaveScreen")]

    def on_mount(self) -> None:
        # self.screen.styles.background = "slategrey"
        # self.screen.styles.background = "darkslategray"
        self.screen.styles.background = "ansi_black"
        self.screen.styles.border = ("heavy", "white")
        self.screen.border_title = 'Baller Sim'
        self.screen.border_subtitle = "by Lucien Tran"

    def on_key(self, event: events.Key) -> None:
        if event.key.isdecimal():
            self.screen.styles.background = COLORS[int(event.key)]
        # await self.mount(Welcome()) # when mounting a component and wanting to modify it, you need to make function async and await
        # self.query_one(Button).label = "YES!"

    def compose(self) -> ComposeResult:
        self.baller_title = Static(BALLER_SIM_BANNER, classes="title")
        self.baller_subtitle = Static(
            "A football managerial career mode simulation",
            classes="subtitle"
        )
        self.new_save = Button("New Save", id="new_save")
        self.continue_save = Button("Continue", id="continue")
        self.exit_save = Button("Exit", id="exit")

        yield self.baller_title
        yield self.baller_subtitle
        yield self.continue_save
        yield self.new_save
        yield self.exit_save

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "new_save":
            self.install_screen(NewSaveScreen, name="new_save")
            onboarding_completed = self.push_screen(screen="new_save")
        if event.button.id == "exit":
            self.exit(event.button.id)



if __name__ == "__main__":
    app = BallerSim()
    reply = app.run()
    print(reply)


