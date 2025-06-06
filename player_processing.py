import polars as pl
from player import Player
from club import Club
from league import League
import logging
import sqlite3
import os

logging.basicConfig(level=logging.INFO)


class ClubPlayerProcessing():
    def __init__(self, player_csv, club_csv):
        self.player_csv = player_csv
        self.club_csv = club_csv
        self.all_teams_df = pl.read_csv(self.club_csv)
        self.all_players_df = pl.read_csv(self.player_csv)

    def create_leagues(self):
        """
        Get the leagues and clubs from {club.csv} and init them. Clubs have no players in them at the moment.
        """
        self.all_leagues = []
        self.all_clubs = []
        self.team_groups_by_league = self.all_teams_df.group_by(pl.col("league_id"))
        self.all_league_id = self.team_groups_by_league.agg()

        for id, league in self.team_groups_by_league:
            info = league.row(0, named=True)

            current_league_club = []
            for team in league.iter_rows(named=True):
                club = Club(
                    id=team["team_id"],
                    name=team["team_name"],
                    nationality=team["nationality_name"],
                    stadium=team["home_stadium"],
                    transfer_budget_eur=team["transfer_budget_eur"],
                    defensive_style=team["def_style"],
                    build_up_play=team["off_build_up_play"],
                    chance_creation=team["off_chance_creation"]
                )
                self.all_clubs.append(club)
                current_league_club.append(club)

            self.all_leagues.append(
                League(
                    info["league_id"],
                    info["league_name"],
                    info["nationality_name"],
                    [club.id for club in current_league_club]
                )
            )

        for c in self.all_clubs:
            logging.debug(c)
        logging.debug(f"len(self.all_clubs): {len(self.all_clubs)}")
        logging.debug(f"len(self.all_leagues): {len(self.all_leagues)}")
        for l in self.all_leagues:
            logging.debug(l.to_string())

    def get_mismatch_club(self):
        """
        Get the mismatch in club syntax in the data between the two csv files.
        Must call create_leagues() beforehand
        """
        # all_club_names = [c.name for c in self.all_clubs]
        player_groups_by_clubs = self.all_players_df.group_by(pl.col("Club"))
        all_player_club_name = player_groups_by_clubs.agg().get_column("Club").to_list()

        for club in self.all_clubs:
            if club.nationality in [ "Spain", "England", "Germany", "France", "Portugal", "Australia"]:
                if club.name not in all_player_club_name:
                    logging.debug(f" club missing/mismatch: {club.name}")


    def create_players(self):
        """
        get players from {players.csv} and assign them to clubs and leagues
        """
        self.player_groups_by_clubs = self.all_players_df.group_by(pl.col("Club"))
        all_club_names = [c.name for c in self.all_clubs]

        self.all_players = []


        for name, club in self.player_groups_by_clubs:
            club_name = club.row(0, named=True)["Club"]

            if club_name not in all_club_names:
                logging.debug(f"{club_name} not in club names.")
                continue

            current_club = None
            for team in self.all_clubs:
                if team.name == club_name:
                    current_club = team
                    break

            logging.debug(f"current club: {current_club}")
            for player in club.iter_rows(named=True):
                # logging.debug(player)
                current_club.players.append(player[""])
                self.all_players.append(
                    Player(
                        id=player[""],
                        name=player["Name"],
                        nationality=player["Nation"],
                        position=player["Position"],
                        age=player["Age"],
                        overall=player["Overall"],
                        pace=player["Pace"],
                        shooting=player["Shooting"],
                        passing=player["Passing"],
                        dribbling=player["Dribbling"],
                        defending=player["Defending"],
                        physicality=player["Physicality"],
                        accelaration=player["Acceleration"],
                        sprint=player["Sprint"],
                        positioning=player["Positioning"],
                        finishing=player["Finishing"],
                        shot=player["Shot"],
                        long_shot=player["Long"],
                        volleys=player["Volleys"],
                        penalties=player["Penalties"],
                        vision=player["Vision"],
                        crossing=player["Crossing"],
                        free_kick=player["Free"],
                        curve=player["Curve"],
                        agility=player["Agility"],
                        balance=player["Balance"],
                        reaction=player["Reactions"],
                        composure=player["Composure"],
                        interception=player["Interceptions"],
                        heading=player["Heading"],
                        defence=player["Def"],
                        standing_tackle=player["Standing"],
                        sliding_tackle=player["Sliding"],
                        jumping=player["Jumping"],
                        stamina=player["Stamina"],
                        strength=player["Strength"],
                        aggression=player["Aggression"],
                        attacking_work_rate=player["Att work rate"],
                        defensive_work_rate=player["Def work rate"],
                        preferred_foot=player["Preferred foot"],
                        weak_foot=player["Weak foot"],
                        skill_move=player["Skill moves"],
                        goalkeeping=player["GK"] if player["GK"] else 1,
                    )
                )

    def get_club_by_id(self):
        """
        get club from all_clubs by club_id
        """


    def cleanup_league(self):
        """
        Remove empty teams and empty leagues
        """
        empty_leagues = []
        for l in self.all_leagues:
            empty_clubs = []
            for c in l.clubs:

                if len(self.get_club_by_id(c).players) == 0:
                    empty_clubs.append(c)
            for empty_club in empty_clubs:
                l.clubs.remove(empty_club)

            if len(l.clubs) == 0:
                empty_leagues.append(l)

        for empty_league in empty_leagues:
            self.all_leagues.remove(empty_league)


    def get_league_by_nationality(self, nationality_list):
        """
        Get leagues from nationality (country code)
        """
        selected_leagues = []
        for l in self.all_leagues:
            if l.nationality in nationality_list:
                selected_leagues.append(l)
        return selected_leagues
    

    def get_club_by_id(self, id:str) -> Club:
        for c in self.all_clubs:
            if c.id == id:
                return c
            
    def get_players_by_id(self, id:str) -> Player:
        for p in self.all_players:
            if p.id == id:
                return p
    
    def convert_raw_to_db(self, file: str) -> None:
        tables = [
            """
            CREATE TABLE IF NOT EXISTS Leagues(
                league_id INTEGER PRIMARY KEY,
                league_name TEXT NOT NULL,
                nationality TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Clubs(
                club_id INTEGER PRIMARY KEY,
                club_name TEXT NOT NULL,
                nationality TEXT NOT NULL,
                stadium TEXT,
                transfer_budget INT,
                defensive_style TEXT,
                build_up_play TEXT,
                chance_creation TEXT,
                league_id INTEGER,
                FOREIGN KEY (league_id) REFERENCES Leagues(league_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Players(
                player_id INTEGER PRIMARY KEY,
                player_name TEXT NOT NULL,
                nationality TEXT NOT NULL,
                position TEXT NOT NULL,
                age INTEGER NOT NULL,

                overall INTEGER DEFAULT 50,
                pace INTEGER DEFAULT 50,
                shooting INTEGER DEFAULT 50,
                passing INTEGER DEFAULT 50,
                dribbling INTEGER DEFAULT 50,
                defending INTEGER DEFAULT 50,
                physicality INTEGER DEFAULT 50,
                accelaration INTEGER DEFAULT 50,
                sprint INTEGER DEFAULT 50,
                positioning INTEGER DEFAULT 50,
                finishing INTEGER DEFAULT 50,
                shot INTEGER DEFAULT 50,
                long_shot INTEGER DEFAULT 50,
                volleys INTEGER DEFAULT 50,
                penalties INTEGER DEFAULT 50,
                vision INTEGER DEFAULT 50,
                crossing INTEGER DEFAULT 50,
                free_kick INTEGER DEFAULT 50,
                curve INTEGER DEFAULT 50,
                agility INTEGER DEFAULT 50,
                balance INTEGER DEFAULT 50,
                reaction INTEGER DEFAULT 50,
                composure INTEGER DEFAULT 50,
                interception INTEGER DEFAULT 50,
                heading INTEGER DEFAULT 50,
                defence INTEGER DEFAULT 50,
                standing_tackle INTEGER DEFAULT 50,
                sliding_tackle INTEGER DEFAULT 50,
                jumping INTEGER DEFAULT 50,
                stamina INTEGER DEFAULT 50,
                strength INTEGER DEFAULT 50,
                aggression INTEGER DEFAULT 50,
                attacking_work_rate TEXT DEFAULT "Medium",
                defensive_work_rate TEXT DEFAULT "Medium",
                preferred_foot TEXT DEFAULT "Right",
                weak_foot INTEGER DEFAULT 50,
                skill_move INTEGER DEFAULT 50,
                goalkeeping INTEGER DEFAULT 50,

                injured BOOLEAN DEFAULT 0,

                club_id INTEGER,
                FOREIGN KEY (club_id) REFERENCES Clubs(club_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Seasons(
                season_number INTEGER NOT NULL,
                league_id INTEGER NOT NULL,
                PRIMARY KEY (season_number, league_id),
                FOREIGN KEY (league_id) REFERENCES Leagues(league_id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS Managers(
                manager_id INTEGER PRIMARY KEY NOT NULL,
                manager_name TEXT NOT NULL,
                current_club INTEGER NOT NULL,
                current_season INTEGER NOT NULL,
                FOREIGN KEY (current_club) REFERENCES Clubs(club_id),
                FOREIGN KEY (current_season) REFERENCES Seasons(season_number)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS ManagedClubs(
                season_number INTEGER NOT NULL,
                manager_id INTEGER NOT NULL,
                club_id INTEGER NOT NULL,
                PRIMARY KEY (season_number, manager_id, club_id),
                FOREIGN KEY (manager_id) REFERENCES Managers(manager_id),
                FOREIGN KEY (season_number) REFERENCES Seasons(season_number),
                FOREIGN KEY (club_id) REFERENCES Clubs(club_id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS Matchdays(
                matchday_number INTEGER NOT NULL,
                season_number INTEGER,
                home_team INTEGER,
                home_score INTEGER NOT NULL,
                away_team INTEGER,
                away_score INTEGER NOT NULL,
                PRIMARY KEY (season_number, matchday_number, home_team, away_team),
                FOREIGN KEY (season_number) REFERENCES Seasons(season_number),
                FOREIGN KEY (home_team) REFERENCES Clubs(club_id),
                FOREIGN KEY (away_team) REFERENCES Clubs(club_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Goalscorers(
                goal_id INTEGER NOT NULL PRIMARY KEY,
                player_id INTEGER,
                assister_id INTEGER,
                matchday_number INTEGER,
                season_number INTEGER,
                team_for INTEGER,
                team_against INTEGER ,
                FOREIGN KEY (player_id) REFERENCES Players(player_id),
                FOREIGN KEY (assister_id) REFERENCES Players(player_id),
                FOREIGN KEY (matchday_number) REFERENCES Matchdays(matchday_number),
                FOREIGN KEY (season_number) REFERENCES Seasons(season_number),
                FOREIGN KEY (team_for) REFERENCES Clubs(club_id),
                FOREIGN KEY (team_against) REFERENCES Clubs(club_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Assisters(
                assist_id INTEGER NOT NULL PRIMARY KEY,
                player_id INTEGER,
                goalscorer_id INTEGER,
                matchday_number INTEGER,
                season_number INTEGER,
                team_for INTEGER,
                team_against INTEGER,
                FOREIGN KEY (player_id) REFERENCES Players(player_id),
                FOREIGN KEY (goalscorer_id) REFERENCES Players(player_id),
                FOREIGN KEY (matchday_number) REFERENCES Matchdays(matchday_number),
                FOREIGN KEY (season_number) REFERENCES Seasons(season_number),
                FOREIGN KEY (team_for) REFERENCES Clubs(club_id),
                FOREIGN KEY (team_against) REFERENCES Clubs(club_id)
            )
            """,
        ]

        if not os.path.exists(file):
            with open(file, "x") as f:
                pass

        db = sqlite3.connect(file)
        cursor = db.cursor()
        for t in tables:
            print(t)
            cursor.execute(t)
        db.commit()

        all_league_tuples = []
        for l in self.all_leagues:
            all_league_tuples.append(l.to_sql_tuples())
        cursor.executemany("INSERT INTO Leagues VALUES(?, ?, ?)", all_league_tuples)

        all_club_tuples = []
        for l in self.all_leagues:
            for c in l.clubs:
                all_club_tuples.append(self.get_club_by_id(c).to_sql_tuples() + (l.id,))
        cursor.executemany(f"INSERT INTO Clubs VALUES({','.join('?' * len(all_club_tuples[0]))})", all_club_tuples)

        all_player_tuples = []
        for c in self.all_clubs:
            for p in c.players:
                all_player_tuples.append(self.get_players_by_id(p).to_sql_tuples() + (c.id,))
        cursor.executemany(f"INSERT INTO Players VALUES({','.join('?' * len(all_player_tuples[0]))})", all_player_tuples)

        db.commit()
        db.close()

if __name__ == "__main__":
    p_processing = ClubPlayerProcessing(player_csv="male_players.csv", club_csv="male_teams.csv")
    p_processing.create_leagues()
    p_processing.create_players()
    p_processing.get_mismatch_club()
    p_processing.cleanup_league()

    with open("test.log", "w", encoding="utf-8") as f:
        for l in p_processing.all_leagues:
            f.write(l.to_full_string())
            # if l.nationality in [ "Spain", "England", "Germany", "France", "Portugal"]:
            #     f.write(l.to_full_string())
