from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static, Input, SelectionList, Button
from textual.widgets.selection_list import Selection
from textual.containers import Container
from textual.events import Mount
from league import League
from club import Club
from textual import log, on
import baller_database


class NewSaveScreen(Screen):
    CSS_PATH = "new_save_screen.tcss"
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def on_mount(self) -> None:
        self.query_one("#league_select").border_title = "Select the league you want to manage"
        self.query_one("#club_select").border_title = "Select the club you want to manage"

    def compose(self) -> ComposeResult:
        self.baller_title = Static("New Save", classes="title")
        self.baller_subtitle = Static("A football managerial career mode simulation", classes="subtitle")
        self.username_input = Input(placeholder="Manager's name", max_length=30)
        all_leagues = baller_database.DB.get_league_by_nationality(["France", "England"])
        all_leagues_tuples = [Selection(l.name, l.id, False) for l in all_leagues]
        self.league_selection = SelectionList[int](
            *all_leagues_tuples,
            name="League Selection",
            id="league_select",
        )
        self.club_selection = SelectionList[int](name="Club Selection", id="club_select", disabled=True)
        self.submit_button = Button("Submit", id="submit", disabled=True)
        yield self.baller_title
        # yield self.baller_subtitle
        yield self.username_input
        yield self.league_selection
        yield self.club_selection
        yield self.submit_button

    def populate_club_selection(self, league_id) -> None:
        self.all_clubs = baller_database.DB.get_clubs_by_league_id(league_id)
        all_clubs_tuples = [Selection(c.name, c.id, False) for c in self.all_clubs]
        self.club_selection.add_options(all_clubs_tuples)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            if len(self.username_input.value) == 0:
                self.notify("Please enter a username.", severity="error")
            if self.league_selection.selected[0] == None:
                self.notify("Please select a league you would like to manage.", severity="error")
            if self.club_selection.selected[0] == None:
                self.notify("Please select a club you would like to manage.", severity="error")

            club = next((c for c in self.all_clubs if c.id == self.club_selection.selected[0]),None)
            if club is None:
                self.notify("Please select a club you would like to manage.", severity="error")

            baller_database.create_manager(name=self.username_input.value, club=club)
            self.dismiss(True)

    @on(SelectionList.SelectionToggled)
    def update_selected_view(self, selection: SelectionList.SelectionToggled) -> None:
        log(selection)
        log(selection.selection)
        log(selection.selection.value)
        log(selection.selection_index)
        if selection.selection_list.id == "league_select":
            self.club_selection.clear_options()
            selection.selection_list.deselect_all()
            selection.selection_list.select(selection.selection)
            self.club_selection.disabled = False
            self.populate_club_selection(selection.selection.value)
        elif selection.selection_list.id == "club_select":
            selection.selection_list.deselect_all()
            selection.selection_list.select(selection.selection)
            self.submit_button.disabled = False




