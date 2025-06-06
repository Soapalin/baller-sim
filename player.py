from dataclasses import dataclass, field
from typing import List

@dataclass
class Player:
    id: int # maybe remove
    name: int
    nationality: str
    position: str
    age: int

    overall: int = field(default=50)
    pace: int = field(default=50)
    shooting: int = field(default=50)
    passing: int = field(default=50)
    dribbling: int = field(default=50)
    defending: int = field(default=50)
    physicality: int = field(default=50)
    accelaration: int  = field(default=50)
    sprint: int = field(default=50)
    positioning: int = field(default=50)
    finishing: int = field(default=50)
    shot: int = field(default=50)
    long_shot: int = field(default=50)
    volleys: int = field(default=50)
    penalties: int = field(default=50)
    vision: int = field(default=50)
    crossing: int = field(default=50)
    free_kick: int = field(default=50)
    curve: int = field(default=50)
    agility: int = field(default=50)
    balance: int = field(default=50)
    reaction: int = field(default=50)
    composure: int = field(default=50)
    interception: int = field(default=50)
    heading: int = field(default=50)
    defence: int = field(default=50)
    standing_tackle: int = field(default=50)
    sliding_tackle: int = field(default=50)
    jumping: int = field(default=50)
    stamina: int = field(default=50)
    strength: int = field(default=50)
    aggression: int = field(default=50)
    attacking_work_rate: int = field(default=50)
    defensive_work_rate: int = field(default=50)
    preferred_foot: str = field(default='R')
    weak_foot: int = field(default=3)
    skill_move: int = field(default=3)
    goalkeeping: int = field(default=50)

    # match fitness and stats 
    injured: bool = field(default=False)
    # goals_scored: int 


    def to_sql_tuples(self) -> tuple:
        return (
            self.id,
            self.name,
            self.nationality,
            self.position,
            self.age,
            self.overall,
            self.pace,
            self.shooting,
            self.passing,
            self.dribbling,
            self.defending,
            self.physicality,
            self.accelaration,
            self.sprint,
            self.positioning,
            self.finishing,
            self.shot,
            self.long_shot,
            self.volleys,
            self.penalties,
            self.vision,
            self.crossing,
            self.free_kick,
            self.curve,
            self.agility,
            self.balance,
            self.reaction,
            self.composure,
            self.interception,
            self.heading,
            self.defence,
            self.standing_tackle,
            self.sliding_tackle,
            self.jumping,
            self.stamina,
            self.strength,
            self.aggression,
            self.attacking_work_rate,
            self.defensive_work_rate,
            self.preferred_foot,
            self.weak_foot,
            self.skill_move,
            self.goalkeeping,
            self.injured
        )
