from manager import Manager
import os
from dataclasses import dataclass
from typing import List
from league import League
from season import Season
from club import Club
from datetime import datetime
import sqlite3
from shutil import copyfile
ORIGIN_DB_SQLITE = "origin_baller_db.db"
CURRENT_MANAGER = Manager("None", [], [])
CURRENT_DB = ""

@dataclass
class SQLResult:
    success: bool
    error_message: str


class SQLDatabase():
    def __init__(self, db_file) -> None:
        self.db_file = db_file
        self.db = sqlite3.connect(self.db_file)
        self.cursor = self.db.cursor()

    def get_leagues_by_nationality(self, nationality: str) -> List[League]:
        self.cursor.execute(f"SELECT * from Leagues WHERE nationality == \"{nationality}\"")
        result_tuples = self.cursor.fetchall()
        return [self.sql_tuple_to_league(tup) for tup in result_tuples]

    def get_all_clubs_in_league(self, league_id: int) -> List[Club]:
        self.cursor.execute(f"SELECT * from Clubs WHERE league_id == {league_id}")
        result_tuples = self.cursor.fetchall()
        return [self.sql_tuple_to_club(tup) for tup in result_tuples]

    def create_new_season(self, league_id) -> Season:
        self.cursor.execute(f"SELECT COUNT(*) from Seasons")
        result_tuples = self.cursor.fetchall()
        print(result_tuples[0][0])
        self.cursor.execute(f"INSERT INTO Seasons VALUES(?,?)", (result_tuples[0][0]+1, league_id))
        self.db.commit()
        return Season(
            season_number=result_tuples[0][0]+1,
            league_id=league_id
        )

    def create_first_season(self, league_id) -> Season:
        self.cursor.execute(f"INSERT OR REPLACE INTO Seasons VALUES(?,?)", (1, league_id))
        self.db.commit()
        return Season(
            season_number=1,
            league_id=league_id
        )

    def create_manager(self, name:str, club:Club, current_season:int) -> SQLResult:
        now = int(datetime.now().timestamp())
        self.cursor.execute(f"INSERT INTO Managers VALUES(?, ?, ?, ?)", (now, name, club.id, current_season))
        self.db.commit()
        return Manager(
            id=now,
            name=name,
            current_season=current_season,
            clubs=[club.id]
        )

    def get_club_by_id(self, club_id:int) -> Club:
        self.cursor.execute(f"SELECT * from Clubs WHERE club_id == {club_id}")
        result_tuple = self.cursor.fetchone()
        return self.sql_tuple_to_club(result_tuple)

    def get_current_club(self, manager_id:int, season_number:int) -> Club:
        self.cursor.execute(f"SELECT * from ManagedClubs WHERE season_number={season_number} AND manager_id={manager_id}")
        result_tuple = self.cursor.fetchone()
        club_id = result_tuple[2]
        return self.get_club_by_id(club_id=club_id)

    def get_manager_by_id(self, manager_id:int) -> Manager:
        self.cursor.execute(f"SELECT * from Managers WHERE manager_id == {manager_id}")
        result_tuples = self.cursor.fetchone()
        return self.sql_tuple_to_manager(result_tuples)

    def get_current_manager(self) -> Manager:
        self.cursor.execute(f"SELECT * from Managers")
        result_tuples = self.cursor.fetchall()
        return self.sql_tuple_to_manager(result_tuples[0])

    def get_all_managers(self) -> List[Manager]:
        self.cursor.execute(f"SELECT * from Managers")
        result_tuples = self.cursor.fetchall()
        return [self.sql_tuple_to_manager(m) for m in result_tuples]

    def create_managed_club(self, season_number:int, manager_id:int, club_id:int) -> None:
        pass

    def sql_tuple_to_manager(self, manager_tuple: tuple) -> Manager:
        return Manager(
            id=manager_tuple[0],
            name=manager_tuple[1],
            clubs=[manager_tuple[2]],
            current_season=manager_tuple[3]
        )


    def sql_tuple_to_league(self, league_tuple: tuple) -> League:
        return League(
            id=league_tuple[0],
            name=league_tuple[1],
            nationality=league_tuple[1]
        )

    def sql_tuple_to_club(self, club_tuple: tuple) -> Club:
        return Club(
            id=club_tuple[0],
            name=club_tuple[1],
            nationality=club_tuple[2],
            stadium=club_tuple[3],
            transfer_budget_eur=0 if club_tuple[4] is None else club_tuple[4],
            defensive_style=club_tuple[5],
            build_up_play=club_tuple[6],
            chance_creation=club_tuple[7],
        )

ORIGIN = SQLDatabase(db_file=ORIGIN_DB_SQLITE)


def init_career(name, club, league_id):
    global CURRENT_DB, CURRENT_MANAGER
    season = ORIGIN.create_first_season(league_id=league_id)
    CURRENT_MANAGER = ORIGIN.create_manager(name=name, club=club, current_season=season.season_number)
    copyfile(ORIGIN.db_file,f"{CURRENT_MANAGER.name}_{CURRENT_MANAGER.id}_baller_db.db")
    CURRENT_DB = SQLDatabase(db_file=f"{CURRENT_MANAGER.name}_{CURRENT_MANAGER.id}_baller_db.db")
    CURRENT_DB.create_managed_club(
        season_number=CURRENT_MANAGER.current_season,
        manager_id=CURRENT_MANAGER.id,
        club_id=CURRENT_MANAGER.current_club()
    )

def load_career(manager_id:int):
    global CURRENT_DB, CURRENT_MANAGER
    CURRENT_MANAGER = ORIGIN.get_manager_by_id(manager_id)
    CURRENT_DB = SQLDatabase(db_file=f"{CURRENT_MANAGER.name}_{CURRENT_MANAGER.id}_baller_db.db")


# class Database():
#     manager: Manager
#     all_leagues: List[League]
#     all_clubs: List[Club]

#     def __init__(self, manager: Manager, all_leagues:List[League], all_clubs: List[Club]) -> None:
#         self.manager = manager
#         self.all_leagues = all_leagues
#         self.all_clubs = all_clubs

#     def get_clubs_by_league_id(self, league_id) -> List[Club]:
#         for l in self.all_leagues:
#             if l.id == league_id:
#                 return l.clubs
#         return []

#     def get_league_by_nationality(self, nationality_list, tier=1):
#         """
#         Get leagues that are of the same nationality as the list

#         Parameters
#         ----------
#         nationality_list: list(str)
#             list of nationalities to fetch several leagues of diff nationalities at once

#         Returns
#         ----------
#         list(League)
#         """
#         selected_leagues = []
#         for l in self.all_leagues:
#             if l.nationality in nationality_list:
#                 selected_leagues.append(l)
#         return selected_leagues

#     def get_clubs_by_league_id(self, league_id):
#         """"""
#         for l in self.all_leagues:
#             if l.id == league_id:
#                     return l.clubs

#     def get_clubs(self, league_name, nationality=None):
#         """"""
#         for l in self.all_leagues:
#             if l.name == league_name:
#                 if nationality is not None:
#                     if nationality == l.nationality:
#                         return l.clubs
#                 else:
#                     return l.clubs

# def load_save():
#     global DB, CURRENT_MANAGER
#     with open(DB_PICKLE, "rb") as file:
#         DB = pickle.load(file)
#     CURRENT_MANAGER = DB.manager


# def create_manager(name, club):
#     """
#     Create a manager save
#     """
#     global CURRENT_MANAGER
#     CURRENT_MANAGER = Manager(name=name, clubs=[club], trophies=[])
#     save_db()


# def save_db():
#     """
#     save DB in pickle file
#     """
#     global DB
#     DB = Database(manager=CURRENT_MANAGER, all_leagues=DB.all_leagues, all_clubs=DB.all_clubs)
#     with open(DB_PICKLE, "wb") as file:
#         pickle.dump(DB, file)


# if not os.path.exists(ORIGIN_DB_SQLITE):
#     player_processing = ClubPlayerProcessing(player_csv="male_players.csv", club_csv="male_teams.csv")
#     player_processing.create_leagues()
#     player_processing.create_players()
#     player_processing.get_mismatch_club()
#     player_processing.cleanup_league()
#     DB = Database(
#         manager=Manager("None", [], []),
#         all_leagues=player_processing.all_leagues,
#         all_clubs=player_processing.all_clubs
#     )
#     CURRENT_MANAGER = DB.manager
# else:
#     load_save()




