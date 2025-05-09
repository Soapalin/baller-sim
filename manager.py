from dataclasses import dataclass, field
from typing import List
from club import Club


@dataclass
class Manager():
    name: str
    clubs: List[Club] = field(default_factory=list)
    trophies: List[str] = field(default_factory=list)


    def current_club(self) -> Club|None:
        if len(self.clubs) == 0:
            return None
        else:
            return self.clubs[-1]