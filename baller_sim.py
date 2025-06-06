from textual.app import App, ComposeResult
from textual import events, log, work
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Header, Static, Tree
from new_save_screen import NewSaveScreen
from manager_dashboard_screen import ManagerDashboardScreeen
import baller_database

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



class ChooseSave(ModalScreen):
    def compose(self) -> ComposeResult:
        self.all_managers = baller_database.ORIGIN.get_all_managers()
        for m in self.all_managers:
            log(m)
        if len(self.all_managers) == 0:
            # yield Static("No save found. Please create a new save")
            self.notify("No save found. Please create a new save")
            self.app.pop_screen()
        yield Static("Choose your manager")
        for m in self.all_managers:
            current_club_name = baller_database.ORIGIN.get_club_by_id(m.current_club()).name
            log(current_club_name)
            yield Button(
                label=f"{m.name} - {current_club_name} - Season {m.current_season}",
                id=f"{m.name}_{m.id}"
            )

    def on_key(self, event: events.Key) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        # self.app.pop_screen()
        manager_id_chosen = event.button.id.split("_")[1]
        baller_database.load_career(manager_id=manager_id_chosen)
        self.app.pop_screen() # pop modal before going to dashboard
        self.app.push_screen(screen=ManagerDashboardScreeen(name="manager_dashboard"))



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

    async def switch_to_dashboard(self):
        self.install_screen(ManagerDashboardScreeen, "manager_dashboard")
        dashboard = await self.push_screen_wait("manager_dashboard")
        self.uninstall_screen("manager_dashboard")

    def open_save_modal(self):
        self.push_screen(ChooseSave())

    @work
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "new_save":
            new_save = await self.push_screen_wait(
                screen=NewSaveScreen(name="new_save"),
            )

            if new_save is not None:
                dashboard = await self.push_screen_wait(screen=ManagerDashboardScreeen(name="manager_dashboard"))
                self.uninstall_screen("manager_dashboard")

        if event.button.id == "continue":
            self.open_save_modal()

        if event.button.id == "exit":
            self.exit(event.button.id)



if __name__ == "__main__":
    app = BallerSim()
    reply = app.run()
    print(reply)


