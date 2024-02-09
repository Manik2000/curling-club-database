TABLES = {}


TABLES["Leagues"] = """CREATE OR REPLACE TABLE Leagues (
    league_code VARCHAR(10) PRIMARY KEY,
    league_name VARCHAR(30)
) ENGINE=InnoDB, CHARACTER SET=utf8mb4, COLLATE=utf8mb4_polish_ci;
"""


TABLES["Teams"] = """CREATE OR REPLACE TABLE Teams (
    team_code VARCHAR(15) PRIMARY KEY,
    team_name VARCHAR(30),
    league_code VARCHAR(10),
    established DATE,
    FOREIGN KEY(league_code) REFERENCES Leagues(league_code)
) ENGINE=InnoDB, CHARACTER SET=utf8mb4, COLLATE=utf8mb4_polish_ci;
"""


TABLES["Pants"] = """CREATE OR REPLACE TABLE Pants (
    id TINYINT UNSIGNED PRIMARY KEY,
    brand VARCHAR(40),
    model VARCHAR(40),
    price FLOAT,
    gender VARCHAR(10),
    size TINYINT UNSIGNED
) ENGINE=InnoDB, CHARACTER SET=utf8mb4, COLLATE=utf8mb4_polish_ci;
"""


TABLES["Handwear"] = """CREATE OR REPLACE TABLE Handwear (
    id TINYINT UNSIGNED PRIMARY KEY,
    brand VARCHAR(40),
    model VARCHAR(40),
    price FLOAT,
    gender VARCHAR(10),
    color VARCHAR(40),
    leather VARCHAR(40),
    kind VARCHAR(40),
    line VARCHAR(40), 
    size VARCHAR(5)
) ENGINE=InnoDB, CHARACTER SET=utf8mb4, COLLATE=utf8mb4_polish_ci;
"""


TABLES["Headwear"] = """CREATE OR REPLACE TABLE Headwear (
    id TINYINT UNSIGNED PRIMARY KEY,
    brand VARCHAR(40),
    model VARCHAR(40),
    price FLOAT,
    purpose VARCHAR(40),
    kind VARCHAR(40)
) ENGINE=InnoDB, CHARACTER SET=utf8mb4, COLLATE=utf8mb4_polish_ci;
"""


TABLES["Brooms"] = """CREATE OR REPLACE TABLE Brooms (
    id TINYINT UNSIGNED PRIMARY KEY,
    brand VARCHAR(40),
    model VARCHAR(40),
    price FLOAT,
    purpose VARCHAR(40),
    color VARCHAR(40),
    material VARCHAR(40),
    head VARCHAR(40),
    pad VARCHAR(40), 
    size TINYINT UNSIGNED
) ENGINE=InnoDB, CHARACTER SET=utf8mb4, COLLATE=utf8mb4_polish_ci;
"""

TABLES["Footwear"] = """CREATE OR REPLACE TABLE Footwear (
    id TINYINT UNSIGNED PRIMARY KEY,
    brand VARCHAR(40),
    model VARCHAR(40),
    price FLOAT,
    purpose VARCHAR(40),
    weight VARCHAR(40),
    color VARCHAR(40),
    slider VARCHAR(40),
    size TINYINT UNSIGNED
) ENGINE=InnoDB, CHARACTER SET=utf8mb4, COLLATE=utf8mb4_polish_ci;
"""


TABLES["Equipment"] = """CREATE OR REPLACE TABLE Equipment (
    gear_id TINYINT UNSIGNED PRIMARY KEY,
    team_code VARCHAR(10),
    quantity TINYINT UNSIGNED,
    total_price FLOAT, 
    footwear_id TINYINT UNSIGNED,
    brooms_id TINYINT UNSIGNED, 
    handwear_id TINYINT UNSIGNED,
    pants_id TINYINT UNSIGNED,
    headwear_id TINYINT UNSIGNED,    
    FOREIGN KEY (team_code) REFERENCES Teams(team_code),
    FOREIGN KEY (pants_id) REFERENCES Pants(id),
    FOREIGN KEY (handwear_id) REFERENCES Handwear(id),
    FOREIGN KEY (headwear_id) REFERENCES Headwear(id),
    FOREIGN KEY (footwear_id) REFERENCES Footwear(id),
    FOREIGN KEY (brooms_id) REFERENCES Brooms(id)
) ENGINE=InnoDB, CHARACTER SET=utf8mb4, COLLATE=utf8mb4_polish_ci;
"""

TABLES["Management"] = """CREATE OR REPLACE TABLE Management (
    management_id TINYINT UNSIGNED PRIMARY KEY,
    role VARCHAR(40)
) ENGINE=InnoDB, CHARACTER SET=utf8mb4, COLLATE=utf8mb4_polish_ci;
"""

TABLES["Coaches"] = """CREATE OR REPLACE TABLE Coaches (
    coach_id TINYINT UNSIGNED PRIMARY KEY,
    team_code VARCHAR(10),
    FOREIGN KEY (team_code) REFERENCES Teams(team_code)
) ENGINE=InnoDB, CHARACTER SET=utf8mb4, COLLATE=utf8mb4_polish_ci;
"""


TABLES["Salaries"] = """CREATE OR REPLACE TABLE Salaries (
    salary_id TINYINT UNSIGNED PRIMARY KEY,
    salary FLOAT,
    coach_id TINYINT UNSIGNED,
    management_id TINYINT UNSIGNED,
    FOREIGN KEY (coach_id) REFERENCES Coaches(coach_id),
    FOREIGN KEY (management_id) REFERENCES Management(management_id)
) ENGINE=InnoDB;"""


TABLES["Players"] = """CREATE OR REPLACE TABLE Players (
    player_id TINYINT UNSIGNED PRIMARY KEY,
    team_code VARCHAR(10),
    position VARCHAR(8),
    shooting_percentage FLOAT,
    FOREIGN KEY (team_code) REFERENCES Teams(team_code)
) ENGINE=InnoDB, CHARACTER SET=utf8mb4, COLLATE=utf8mb4_polish_ci;
"""


TABLES["Sponsors"] = """CREATE OR REPLACE TABLE Sponsors (
    sponsor_id TINYINT UNSIGNED PRIMARY KEY, 
    sponsor VARCHAR(40),
    amount FLOAT, 
    frequency TINYINT, 
    sign_date DATE, 
    expiry_date DATE
) ENGINE=InnoDB, CHARACTER SET=utf8mb4, COLLATE=utf8mb4_polish_ci;
"""


TABLES["Finance"] = """CREATE OR REPLACE TABLE Finance (
    payment_id BIGINT UNSIGNED PRIMARY KEY,
    player_id TINYINT UNSIGNED,
    gear_id TINYINT UNSIGNED, 
    salary_id TINYINT UNSIGNED,
    sponsor_id TINYINT UNSIGNED,
    date DATE,
    amount FLOAT(5),
    FOREIGN KEY (player_id) REFERENCES Players(player_id),
    FOREIGN KEY (gear_id) REFERENCES Equipment(gear_id),
    FOREIGN KEY (salary_id) REFERENCES Salaries(salary_id),
    FOREIGN KEY (sponsor_id) REFERENCES Sponsors(sponsor_id)
) ENGINE=InnoDB;
"""


TABLES["PersonalInfo"] = """CREATE OR REPLACE TABLE PersonalInfo (
    phone_number BIGINT UNSIGNED PRIMARY KEY,
    management_id TINYINT UNSIGNED,
    coach_id TINYINT UNSIGNED,
    player_id TINYINT UNSIGNED,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    born DATE,
    join_date DATE, 
    retire_date DATE,
    FOREIGN KEY (management_id) REFERENCES Management(management_id), 
    FOREIGN KEY (coach_id) REFERENCES Coaches(coach_id),
    FOREIGN KEY (player_id) REFERENCES Players(player_id)
) ENGINE=InnoDB, CHARACTER SET=utf8mb4, COLLATE=utf8mb4_polish_ci;
"""


TABLES["Matches"] = """CREATE OR REPLACE TABLE Matches (
    match_id BIGINT UNSIGNED PRIMARY KEY,
    date DATE,
    season VARCHAR(10),
    league_code VARCHAR(10), 
    matchweek TINYINT UNSIGNED,
    red_team VARCHAR(15),
    yellow_team VARCHAR(15), 
    hammer VARCHAR(10), 
    total_red TINYINT UNSIGNED,  
    total_yellow TINYINT UNSIGNED, 
    FOREIGN KEY (red_team) REFERENCES Teams(team_code),
    FOREIGN KEY (yellow_team) REFERENCES Teams(team_code),
    FOREIGN KEY (league_code) REFERENCES Leagues(league_code)
) ENGINE=InnoDB, CHARACTER SET=utf8mb4, COLLATE=utf8mb4_polish_ci;
"""


TABLES["Ends"] = """CREATE OR REPLACE TABLE Ends (
    end_id SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    end TINYINT UNSIGNED,
    match_id BIGINT UNSIGNED,
    points_red TINYINT UNSIGNED,
    points_yellow TINYINT UNSIGNED,
    FOREIGN KEY (match_id) REFERENCES Matches(match_id)
) ENGINE=InnoDB;
"""
