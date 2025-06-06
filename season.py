from typing import List, Union
from dataclasses import dataclass, field


@dataclass
class Match():
    home_team_id: int # club.id
    away_team_id: int # club.id
    matchday_number: int
    score_home: Union[int,None]
    score_away: Union[int,None]

    home_scorers: List[int] = field(default_factory=list)#player.id
    home_assisters: List[int] = field(default_factory=list)#player.id
    away_scorers: List[int] = field(default_factory=list)#player.id
    away_assisters: List[int] = field(default_factory=list)#player.id

@dataclass
class MatchdayFixture:
    matches: List[Match] = field(default_factory=list)

@dataclass
class Season():
    season_number: int
    league_id: int
    fixtures: List[MatchdayFixture] = field(default_factory=list)


# class Season():
#     fixtures: List[MatchdayFixture]
#     top_goalscorers: List[(tuple)] = field(default_factory=list)#player.id, number of goals
#     top_assisters: List[(tuple)] = field(default_factory=list)# player.id, number of assists

#     # def calculate_top_goalscorers(self) -> None:
#     #     all_goals = []
#     #     for f in self.fixtures:
#     #         for m in f.matches:
#     #             all_goals.extend(m.home_scorers)
#     #             all_goals.extend(m.away_scorers)

#     #     all_goalscorers = set(all_goals)



