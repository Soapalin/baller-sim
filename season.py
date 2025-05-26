from club import Club
from league import League
from player import Player
from typing import List, Union
from dataclasses import dataclass


@dataclass
class Match():
    home_team_id: int # club.id 
    away_team_id: int # club.id
    matchday_number: int 
    score_home: Union[int,None]
    score_away: Union[int,None]

    home_scorers: List[int] #player.id
    home_assisters: List[int] #player.id
    away_scorers: List[int] #player.id
    away_assisters: List[int] #player.id

@dataclass
class MatchdayFixture:
    matches: List[Match]


class Season():
    fixtures: List[MatchdayFixture]
    top_goalscorers: List[(int,int)] #player.id, number of goals
    top_assisters: List[(int,int)] # player.id, number of assists

    # def calculate_top_goalscorers(self) -> None:
    #     all_goals = []
    #     for f in self.fixtures:
    #         for m in f.matches:
    #             all_goals.extend(m.home_scorers)
    #             all_goals.extend(m.away_scorers)
        
    #     all_goalscorers = set(all_goals)



