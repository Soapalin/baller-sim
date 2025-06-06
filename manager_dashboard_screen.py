from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static, ContentSwitcher, Button
from textual.containers import Container, Vertical
import baller_database
from textual import log, events

class ManagerDashboardScreeen(Screen):
    CSS_PATH = "manager_dashboard_screen.tcss"
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        self.manager = baller_database.CURRENT_MANAGER
        self.club = baller_database.CURRENT_DB.get_club_by_id(
            club_id=self.manager.current_club()
        )

        with Vertical(id="sidebar"):

            yield Static(f"Manager Dashboard - {self.manager.name}")
            yield Static(f"{self.club.name}")
            yield Static("")
            yield Button("Next Game", id="next-game")
            yield Button("Team Management", id="team-management")
            yield Button("League Table", id="league-table")
            yield Button("Stats", id="stats")
            yield Button("Calendar", id="calendar")
            yield Button("Club", id="club")
            yield Button("Transfers", id="transfers")
            yield Button("Manager", id="manager")

        with ContentSwitcher(initial="next-game"):
            yield self.next_game_content()
            yield self.team_management_content()
            yield self.league_table_content()
            yield self.stats_content()
            yield self.calendar_content()
            yield self.club_content()
            yield self.transfers_content()
            yield self.manager_content()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.query_one(ContentSwitcher).current = event.button.id

    def on_mount(self) -> None:
        pass

    def next_game_content(self) -> Container:
        return Container(
            Static("Next Game"),
            id="next-game"
        )

    def team_management_content(self) -> Container:
        return Container(
            Static("Team Management"),
            id="team-management"
        )

    def league_table_content(self) -> Container:
        return Container(
            Static("League Table"),
            id="league-table"
        )

    def stats_content(self) -> Container:
        return Container(
            Static("Stats"),
            id="stats"
        )

    def club_content(self) -> Container:
        return Container(
            Static("Club"),
            id="club"
        )

    def calendar_content(self) -> Container:
        return Container(
            Static("Calendar"),
            id="calendar"
        )

    def transfers_content(self) -> Container:
        return Container(
            Static("Transfers"),
            id="transfers"
        )

    def manager_content(self) -> Container:
        return Container(
            Static("Manager"),
            id="manager"
        )


