from dataclasses import dataclass, field
from typing import List, Union
from club import Club


@dataclass
class Manager():
    id: int
    name: str
    clubs: List[int] = field(default_factory=list)
    current_season: int = field(default=1)
    trophies: List[str] = field(default_factory=list)


    def current_club(self) -> Union[Club, None]:
        if len(self.clubs) == 0:
            return None
        else:
            return self.clubs[-1]