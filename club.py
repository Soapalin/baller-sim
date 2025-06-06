from dataclasses import dataclass, field
from typing import List
from player import Player

@dataclass
class Club:
    id: int
    name: str
    nationality: str
    stadium: str
    transfer_budget_eur: int
    defensive_style: str
    build_up_play: str
    chance_creation: str
    players: List[int] = field(default_factory=list)


    def to_sql_tuples(self) -> tuple:
        return (
            self.id, 
            self.name, 
            self.nationality, 
            self.stadium, 
            self.transfer_budget_eur, 
            self.defensive_style,
            self.build_up_play,
            self.chance_creation,
        )
