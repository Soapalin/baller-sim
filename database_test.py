from manager import Manager
import pickle
import os
from player_processing import ClubPlayerProcessing
from dataclasses import dataclass
from typing import List
from club import Club
import sqlite3
from baller_database import SQLDatabase, ORIGIN_DB_SQLITE


def create_db_from_processing():
    player_processing = ClubPlayerProcessing(player_csv="male_players.csv", club_csv="male_teams.csv")
    player_processing.create_leagues()
    player_processing.create_players()
    player_processing.get_mismatch_club()
    player_processing.cleanup_league()
    # player_processing.convert_raw_to_db("baller_db.db")
    player_processing.convert_raw_to_db("origin_baller_db.db")



def query_functions():
    ORIGIN = SQLDatabase(db_file=ORIGIN_DB_SQLITE)
    leagues = ORIGIN.get_leagues_by_nationality("France")
    print(leagues)
    for league in leagues:
        club_result = ORIGIN.get_all_clubs_in_league(league_id=league.id)
        print(club_result)

def count_functions():
    ORIGIN = SQLDatabase(db_file=ORIGIN_DB_SQLITE)
    ORIGIN.create_new_season(league_id=1)

create_db_from_processing()
# query_functions()
# count_functions()