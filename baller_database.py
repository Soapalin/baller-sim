from manager import Manager
import pickle
import os
from player_processing import ClubPlayerProcessing
from dataclasses import dataclass
from typing import List
from league import League
from club import Club

DB_PICKLE = "BALLER_DB.pkl"
CURRENT_MANAGER = Manager("None", [], [])


class Database():
    manager: Manager
    all_leagues: List[League]
    all_clubs: List[Club]

    def __init__(self, manager: Manager, all_leagues:List[League], all_clubs: List[Club]) -> None:
        self.manager = manager
        self.all_leagues = all_leagues
        self.all_clubs = all_clubs

    def get_clubs_by_league_id(self, league_id) -> List[Club]:
        for l in self.all_leagues:
            if l.id == league_id:
                return l.clubs
        return []
    
    def get_league_by_nationality(self, nationality_list, tier=1):
        """
        Get leagues that are of the same nationality as the list

        Parameters
        ----------
        nationality_list: list(str)
            list of nationalities to fetch several leagues of diff nationalities at once

        Returns
        ----------
        list(League)
        """
        selected_leagues = []
        for l in self.all_leagues:
            if l.nationality in nationality_list:
                selected_leagues.append(l)
        return selected_leagues

    def get_clubs_by_league_id(self, league_id):
        """"""
        for l in self.all_leagues:
            if l.id == league_id:
                    return l.clubs

    def get_clubs(self, league_name, nationality=None):
        """"""
        for l in self.all_leagues:
            if l.name == league_name:
                if nationality is not None:
                    if nationality == l.nationality:
                        return l.clubs
                else:
                    return l.clubs


def load_save():
    global DB, CURRENT_MANAGER
    with open(DB_PICKLE, "rb") as file:
        DB = pickle.load(file)
    CURRENT_MANAGER = DB.manager

    with open("test.log", "w", encoding="utf-8") as f:
        for l in DB.all_leagues:
            f.write(l.to_full_string())


def create_manager(name, club):
    """
    Create a manager save
    """
    global CURRENT_MANAGER
    CURRENT_MANAGER = Manager(name=name, clubs=[club], trophies=[])
    save_db()


def save_db():
    """
    save DB in pickle file
    """
    global DB
    DB = Database(manager=CURRENT_MANAGER, all_leagues=DB.all_leagues, all_clubs=DB.all_clubs)
    with open(DB_PICKLE, "wb") as file:
        pickle.dump(DB, file)


if not os.path.exists(DB_PICKLE):
    player_processing = ClubPlayerProcessing(player_csv="male_players.csv", club_csv="male_teams.csv")
    player_processing.create_leagues()
    player_processing.create_players()
    player_processing.get_mismatch_club()
    player_processing.cleanup_league()
    DB = Database(
        manager=Manager("None", [], []),
        all_leagues=player_processing.all_leagues,
        all_clubs=player_processing.all_clubs
    )
    CURRENT_MANAGER = DB.manager
else:
    load_save()



 
