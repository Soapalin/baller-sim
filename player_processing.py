import polars as pl
from player import Player
from club import Club
from league import League
import logging

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
                    current_league_club
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
                current_club.players.append(
                    Player(
                        id=player[""],
                        name=player["Name"],
                        nationality=player["Nation"],
                        position=player["Position"],
                        age=player["Age"]
                    )
                )

            logging.debug(current_club.players_to_string())

    def cleanup_league(self):
        """
        Remove empty teams and empty leagues
        """
        empty_leagues = []
        for l in self.all_leagues:
            empty_clubs = []
            for c in l.clubs:
                if len(c.players) == 0:
                    empty_clubs.append(c)
            for empty_club in empty_clubs:
                l.clubs.remove(empty_club)

            if len(l.clubs) == 0:
                empty_leagues.append(l)

        for empty_league in empty_leagues:
            self.all_leagues.remove(empty_league)



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