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
    players: List[Player] = field(default_factory=list)

    def players_to_string(self) -> str:
        return [p.name for p in self.players]

