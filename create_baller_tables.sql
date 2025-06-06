CREATE TABLE IF NOT EXISTS Leagues(
    league_id INTEGER PRIMARY KEY,
    league_name TEXT NOT NULL,
    nationality TEXT NOT NULL
);

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
);


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
    preferred_foot TEXT DEFAULT "R",
    weak_foot INTEGER DEFAULT 50,
    skill_move INTEGER DEFAULT 50,
    goalkeeping INTEGER DEFAULT 50,

    injured BOOLEAN DEFAULT 0,

    club_id INTEGER,
    FOREIGN KEY (club_id) REFERENCES Clubs(club_id)
);

CREATE TABLE IF NOT EXISTS Seasons(
    season_number INTEGER NOT NULL,
    league_id INTEGER NOT NULL FOREIGN KEY,
    PRIMARY KEY (season_number, league_id),
    FOREIGN KEY (league_id) REFERENCES Leagues(league_id)
);

CREATE TABLE IF NOT EXISTS Managers(
    manager_id INTEGER PRIMARY KEY,
    manager_name TEXT NOT NULL,
    current_club INTEGER FOREIGN KEY,
    current_season INTEGER FOREIGN KEY
    FOREIGN KEY (current_club) REFERENCES Clubs(club_id)
    FOREIGN KEY (current_season) REFERENCES Seasons(season_number)
);

CREATE TABLE IF NOT EXISTS ManagedClubs(
    season_number INTEGER FOREIGN KEY,
    manager_id INTEGER FOREIGN KEY,
    club_id INTEGER FOREIGN KEY,
    PRIMARY KEY (season_number, manager_id, club_id),
    FOREIGN KEY (manager_id) REFERENCES Managers(manager_id),
    FOREIGN KEY (season_number) REFERENCES Seasons(season_number),
    FOREIGN KEY (current_club) REFERENCES Clubs(club_id)
);

CREATE TABLE IF NOT EXISTS Matchdays(
    matchday_number INTEGER NOT NULL,
    season_number INTEGER FOREIGN KEY,
    home_team INTEGER FOREIGN KEY,
    home_score INTEGER,
    away_team INTEGER FOREIGN KEY,
    away_score INTEGER,
    PRIMARY KEY (season_number, matchday_number, home_team, away_team),
    FOREIGN KEY (season_number) REFERENCES Seasons(season_number),
    FOREIGN KEY (home_team) REFERENCES Clubs(club_id),
    FOREIGN KEY (away_team) REFERENCES Clubs(club_id)
);

CREATE TABLE IF NOT EXISTS Goalscorers (
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
    FOREIGN KEY (team_against) REFERENCES Clubs(club_id),
);


CREATE TABLE IF NOT EXISTS Assisters WITH ERKEY(
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
    FOREIGN KEY (team_against) REFERENCES Clubs(club_id),
);

-- CREATE TABLE IF NOT EXISTS Trophies(
--     trophy_name TEXT NOT NULL,
--     season_number INTEGER FOREIGN KEY,
--     manager_id INTEGER FOREIGN KEY,
--     club_id INTEGER FOREIGN KEY
-- );
-- CREATE TABLE IF NOT EXISTS matches(

-- )


