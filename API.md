## Teams

Usage

```
from basketball_reference_scraper.teams import get_roster, get_team_stats, get_opp_stats, get_roster_stats, get_team_misc
```

### `get_roster(team, season)`
Parameters:
  - `team` - NBA team abbreviation (e.g. `'GSW'`, `'SAS'`)
  - `season_end_year` - Desired end year (e.g. `1988`, `2011`)

Returns:

  A Pandas Dataframe containing the following columns:

  ```
  ['NUMBER', 'PLAYER', 'POS', 'HEIGHT', 'WEIGHT', 'BIRTH_DATE', 
    'NATIONALITY', 'EXPERIENCE', 'COLLEGE']
  ```

### `get_team_stats(team, season_end_year, data_format='PER_GAME')`

Parameters:
  - `team` - NBA team abbreviation (e.g. `'GSW'`, `'SAS'`)
  - `season_end_year` - Desired end year (e.g. `1988`, `2011`)
  - `data_format` - One of `'TOTAL'|'PER_GAME'|'PER_POSS'`. Default value is `'PER_GAME'`

Returns:

  A Pandas Series containing the following indices:

  ```
  ['G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 
  'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
  ```


### `get_opp_stats(team, season_end_year, data_format='PER_GAME')`

Parameters:
  - `team` - NBA team abbreviation (e.g. `'GSW'`, `'SAS'`)
  - `season_end_year` - Desired end year (e.g. `1988`, `2011`)
  - `data_format` - One of `'TOTAL'|'PER_GAME'|'PER_POSS'`. Default value is `'PER_GAME'`

Returns:

  A Pandas Series containing the following indices:

  ```
  ['OPP_G', 'OPP_MP', 'OPP_FG', 'OPP_FGA', 'OPP_FG%', 'OPP_3P', 'OPP_3PA', 'OPP_3P%', 'OPP_2P', 'OPP_2PA', 'OPP_2P%', 'OPP_FT', 'OPP_FTA', 'OPP_FT%', 
  'OPP_ORB', 'OPP_DRB', 'OPP_TRB', 'OPP_AST', 'OPP_STL', 'OPP_BLK', 'OPP_TOV', 'OPP_PF', 'OPP_PTS']
  ```

### `get_roster_stats(team, season, data_format='PER_GAME', playoffs=False)`

Parameters:
  - `team` - NBA team abbreviation (e.g. `'GSW'`, `'SAS'`)
  - `season_end_year` - Desired end year (e.g. `1988`, `2011`)
  - `data_format` - One of `'TOTALS'|'PER_GAME'|'PER_MINUTE'|'PER_POSS'|'ADVANCED'`. Default value is `'PER_GAME'`
  - `playoffs` - Whether to return Playoff stats or not. One of `True|False`

Returns:

  A Pandas Series containing the following columns:

  ```
  ['PLAYER', 'POS', 'AGE', 'TEAM', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'SEASON']
  ```

### `get_team_misc(team, season)`

Parameters:
  - `team` - NBA team abbreviation (e.g. `'GSW'`, `'SAS'`)
  - `season_end_year` - Desired end year (e.g. `1988`, `2011`)

Returns:

  A Pandas Series containing the following columns:

  ```
  ['W', 'L', 'PW', 'PL', 'MOV', 'SOS', 'SRS', 'ORtg', 'DRtg', 'Pace', 'FTr', '3PAr', 'eFG%', 'TOV%', 'ORB%', 
  'FT/FGA', 'eFG%', 'TOV%', 'DRB%', 'FT/FGA', 'Arena', 'Attendance']
  ```

## Players

Usage

```
from basketball_reference_scraper.players import get_stats, get_game_logs, get_player_headshot
```

### `get_stats(name, stat_type='PER_GAME', playoffs=False, career=False)`

Parameters:
  - `name` - Player full name (e.g. `'LaMarcus Aldridge'`)
  - `stat_type` - One of `'PER_GAME', 'PER_MINUTE', 'PER_POSS', 'ADVANCED'` 
  - `playoffs` - Whether to return Playoff stats or not. One of `True|False`. Default value is `False`
  - `career` - Whether to return career stats or not. One of `True|False`. Default value is `False` 

Returns:

  A Pandas DataFrame that varies based on the parameters passed.
  Please refer to a [sample page](https://www.basketball-reference.com/players/a/aldrila01.html) for full details.

### `get_game_logs(name, start_date, end_date, playoffs=False)`

Parameters:
  - `name` - Player full name (e.g. `'LaMarcus Aldridge'`)
  - `start_date` - Date in string format of `'YYYY-MM-DD'`.
  - `end_date` - Date in string format of `'YYYY-MM-DD'`.
  - `playoffs` - Whether to return Playoff stats or not. One of `True|False`. Default value is `False`

Returns:

  A Pandas DataFrame containing the following columns:

  ```
  ['DATE', 'AGE', 'TEAM', 'HOME/AWAY', 'OPPONENT', 'RESULT', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'GAME_SCORE', '+/-']
  ```

### `get_player_headshot(name)`

Parameters:
  - `name` - Player full name (e.g. `'LaMarcus Aldridge'`)

Returns:
  A url that points to the Basketball Reference headshot of the individual player. For example, if `name = 'Kobe Bryant'`, the resulting url is `'https://d2cwpp38twqe55.cloudfront.net/req/202006192/images/players/bryanko01.jpg'`


## Seasons

Usage

```
from basketball_reference_scraper.seasons import get_schedule, get_standings
```


### `get_schedule(season, playoffs=False)`

Parameters:
  - `season` - Desired end year (e.g. `1988`, `2011`)
  - `playoffs` - Whether to return Playoff stats or not. One of `True|False`. Default value is `'False'`

Returns:

  A Pandas DataFrame with the following columns:

  ```
  ['DATE', 'VISITOR', 'VISITOR_PTS', 'HOME', 'HOME_PTS']
  ```

### `get_standings(date=None)`

Parameters:
  - `date` - Desired date in a string format (e.g. `'2020-01-06'`). Default value is `NONE`, which returns standings for the current date.

Returns:

  A dictionary containing standings for the Eastern and Western Conferences along with relevant statistics as a Pandas DataFrame. For example:

  ```
  >>> d = get_standings()
  >>> list(d['WESTERN_CONF'].columns)
  ['TEAM', 'W', 'L', 'W/L%', 'GB', 'PW', 'PL', 'PS/G', 'PA/G']
  ```

## Box Scores

Usage

```
from basketball_reference_scraper.box_scores import get_box_scores
```

### `get_box_scores(date, team1, team2, period='GAME', stat_type='BASIC')`

Parameters:
  - `date` - Desired date in a string format (e.g. `'2020-01-06'`)
  - `team1` - One of the team abbreviation (e.g. `'DEN'`, `'GSW'`) 
  - `team2` - Other team abbreviation (e.g. `'DEN'`, `'GSW'`) 
  - `period` - Period for which to acquire stats. One of `'GAME'|'Q1'|'Q2'|'Q3'|'Q4'|'H1'|'H2'`. Default value is `'GAME'` 
  - `stat_type` - Period for which to acquire stats. One of `'BASIC'|'ADVANCED'`. Default value is `'BASIC'`. Note that advanced stats are only available for `period='GAME'`. 

Returns:

  A dictionary containing relevant stats for each team as a Pandas DataFrame. For example:

  ```
  >>> d = get_box_scores('2020-01-06', 'DEN', 'ATL')
  >>> list(d['ATL'].columns)
  ['PLAYER', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', '+/-']
  ```

## Play-by-play

Usage

```
from basketball_reference_scraper.pbp import get_pbp
```

### get_pbp(date, team1, team2)

Parameters:
  - `date` - Desired date in a string format (e.g. `'2020-01-06'`)
  - `team1` - One of the team abbreviation (e.g. `'DEN'`, `'GSW'`) 
  - `team2` - Other team abbreviation (e.g. `'DEN'`, `'GSW'`) 

Returns:

  A Pandas DataFrame containing the actions performed by each team at a time. For example:

  ```
  >>> df = get_pbp('2020-01-06', 'DEN', 'ATL')
  >>> list(df.columns)
  ['QUARTER', 'TIME_REMAINING', 'DENVER_ACTION', 'ATLANTA_ACTION', 'DENVER_SCORE', 'ATLANTA_SCORE']
  ```

  Note that the `ACTION` columns (`'DENVER_ACTION'` and `'ATLANTA_ACTION'` in the above example) will contain `nan` if the team did not perform the primary action in the sequence. 

## Shot Charts

Usage

```
from basketball_reference_scraper.shot_charts import get_shot_chart
```

### get_shot_chart(date, team1, team2)

Parameters:
  - `date` - Desired date in a string format (e.g. `'2020-01-06'`)
  - `team1` - One of the team abbreviation (e.g. `'DEN'`, `'GSW'`) 
  - `team2` - Other team abbreviation (e.g. `'DEN'`, `'GSW'`) 

Returns:

  A dictionary containing the shot charts for each team.
  The shot charts are Pandas DataFrames with the following columns:
  ```
  ['x', 'y', 'QUARTER', 'TIME_REMAINING', 'PLAYER', 'MAKE_MISS', 'VALUE', 'DISTANCE']
  ```

  Where `'x'` and `'y'` are half-court coordinates in feet, `QUARTER` and `TIME_REMAINING` provide the time at which the shot occurred,
  `player` provides the player who shot the ball, `MAKE_MISS` is either `'MAKE'` or `'MISS'`, `VALUE` is the number of points gained, and `DISTANCE`
  is distance from the basket in ft.

  For example:

  ```
  >>> d = get_shot_chart('2019-12-28', 'TOR', 'BOS')
  >>> list(d['TOR'].columns)
  ['x', 'y', 'QUARTER', 'TIME_REMAINING', 'PLAYER', 'MAKE_MISS', 'VALUE', 'DISTANCE']
  >>> d['TOR'].iloc[1]
  x                     27.0 ft
  y                     9.75 ft
  QUARTER               1
  TIME_REMAINING        11:03.0
  PLAYER                Serge Ibaka
  MAKE_MISS             MISS
  VALUE                    2
  DISTANCE                 7 ft
  Name: 1, dtype: object
  ```

  Note that the team columns (`'Denver'` and `'Atlanta'` in the above example) will contain `nan` if the team did not perform the primary action in the sequence. 

## Injury Report

Usage

```
from basketball_reference_scraper.injury_report import get_injury_report
```


### get_injury_report()

Parameters:

Returns:

  A Pandas DataFrames with the following columns:
  ```
  ['PLAYER', 'TEAM', 'DATE', 'INJURY', 'STATUS', 'DESCRIPTION']
  ```

## Constants and Parameter Notes

### Dates
Dates are parsed using Pandas `to_datetime()` method and should follow appropriate constraints. Refer to the [documentation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html) for more specifications.

### Team Abbreviations
These are the team abbreviations used by Basketball Reference and should be used in the above methods.
```
ATLANTA HAWKS : ATL
ST. LOUIS HAWKS : SLH
MILWAUKEE HAWKS : MIL
TRI-CITIES BLACKHAWKS : TCB
BOSTON CELTICS : BOS
BROOKLYN NETS : BRK
NEW JERSEY NETS : NJN
CHICAGO BULLS : CHI
CHARLOTTE HORNETS (1988-2004): CHH
CHARLOTTE HORNETS (2014-Present): CHO
CHARLOTTE BOBCATS : CHA
CLEVELAND CAVALIERS : CLE
DALLAS MAVERICKS : DAL
DENVER NUGGETS : DEN
DETROIT PISTONS : DET
FORT WAYNE PISTONS : FWP
GOLDEN STATE WARRIORS : GSW
SAN FRANCISCO WARRIORS : SFW
PHILADELPHIA WARRIORS : PHI
HOUSTON ROCKETS : HOU
INDIANA PACERS : IND
LOS ANGELES CLIPPERS : LAC
SAN DIEGO CLIPPERS : SDC
BUFFALO BRAVES : BUF
LOS ANGELES LAKERS : LAL
MINNEAPOLIS LAKERS : MIN
MEMPHIS GRIZZLIES : MEM
VANCOUVER GRIZZLIES : VAN
MIAMI HEAT : MIA
MILWAUKEE BUCKS : MIL
MINNESOTA TIMBERWOLVES : MIN
NEW ORLEANS PELICANS : NOP
NEW ORLEANS/OKLAHOMA CITY HORNETS : NOK
NEW ORLEANS HORNETS : NOH
NEW YORK KNICKS : NYK
OKLAHOMA CITY THUNDER : OKC
SEATTLE SUPERSONICS : SEA
ORLANDO MAGIC : ORL
PHILADELPHIA 76ERS : PHI
SYRACUSE NATIONALS : SYR
PHOENIX SUNS : PHO
PORTLAND TRAIL BLAZERS : POR
SACRAMENTO KINGS : SAC
KANSAS CITY KINGS : KCK
KANSAS CITY-OMAHA KINGS : KCK
CINCINNATI ROYALS : CIN
ROCHESTER ROYALS : ROR
SAN ANTONIO SPURS : SAS
TORONTO RAPTORS : TOR
UTAH JAZZ : UTA
NEW ORLEANS JAZZ : NOJ
WASHINGTON WIZARDS : WAS
WASHINGTON BULLETS : WAS
CAPITAL BULLETS : CAP
BALTIMORE BULLETS : BAL
CHICAGO ZEPHYRS : CHI
CHICAGO PACKERS : CHI
ANDERSON PACKERS : AND
CHICAGO STAGS : CHI
INDIANAPOLIS OLYMPIANS : IND
SHEBOYGAN RED SKINS : SRS
ST. LOUIS BOMBERS : SLB
WASHINGTON CAPITOLS : WAS
WATERLOO HAWKS : WAT
SAN DIEGO ROCKETS : SDR
```

### Units
All units are imperial. This means that distances and heights are provided in ft and inches. Additionally, weights are provided in lbs.
