from dataclasses import dataclass, field
from typing import List
from club import Club
from season import Season

@dataclass
class League:
    id: int
    name: str
    nationality: str
    clubs: List[Club] = field(default_factory=list)
    seasons: List[Season]

    # def _get_league_name(self) -> str:
    #     return self.name

    def to_string(self) -> str:
        return f"League(id={self.id}, name={self.name}, nationality={self.nationality}, clubs={len(self.clubs)})"

    def to_full_string(self) -> str:
        result = f"League(id={self.id}, name={self.name}, nationality={self.nationality}, clubs={len(self.clubs)})\n"
        for club in self.clubs:
            result += f"Club: {club.name}\n"
            result += f"{club.players_to_string()}\n\n"
        result += "\n\n\n"
        return result

