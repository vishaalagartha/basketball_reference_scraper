# basketball_reference_scraper

## Teams

### `get_roster(team, season)`
Parameters:
  - `team` - NBA team abbreviation (e.g. `GSW`, `SAS`)
  - `season` - Desired year (e.g. `1988`, `2011`)

Returns:

  A Pandas Dataframe containing the following columns:

  ```
  ['NUMBER', 'PLAYER', 'POS', 'HEIGHT', 'WEIGHT', 'BIRTH_DATE', 
    'NATIONALITY', 'EXPERIENCE', 'COLLEGE']
  ```

### `get_team_series(team, season, data_format='PER_GAME')`

Parameters:
  - `team` - NBA team abbreviation (e.g. `GSW`, `SAS`)
  - `season` - Desired year (e.g. `1988`, `2011`)
  - `data_format` - One of `'TOTAL'|'PER_GAME'|'RANK'|'Y/Y'`. Default value is `'PER_GAME'`

Returns:

  A Pandas Series containing the following indices:

  ```
  ['G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 
  'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
  ```


### `get_opp_series(team, season, data_format='PER_GAME')`

Parameters:
  - `team` - NBA team abbreviation (e.g. `GSW`, `SAS`)
  - `season` - Desired year (e.g. `1988`, `2011`)
  - `data_format` - One of `'TOTAL'|'PER_GAME'|'RANK'|'Y/Y'`. Default value is `'PER_GAME'`

Returns:

  A Pandas Series containing the following indices:

  ```
  ['OPP_G', 'OPP_MP', 'OPP_FG', 'OPP_FGA', 'OPP_FG%', 'OPP_3P', 'OPP_3PA', 'OPP_3P%', 'OPP_2P', 'OPP_2PA', 'OPP_2P%', 'OPP_FT', 'OPP_FTA', 'OPP_FT%', 
  'OPP_ORB', 'OPP_DRB', 'OPP_TRB', 'OPP_AST', 'OPP_STL', 'OPP_BLK', 'OPP_TOV', 'OPP_PF', 'OPP_PTS']
  ```

### `get_roster_stats(team, season, data_format='PER_GAME', playoffs=False)`

Parameters:
  - `team` - NBA team abbreviation (e.g. `GSW`, `SAS`)
  - `season` - Desired year (e.g. `1988`, `2011`)
  - `data_format` - One of `'TOTALS'|'PER_GAME'|'RANK'|'PER_36'|'PER_100_POSS'|'ADVANCED'`. Default value is `'PER_GAME'`
  - `playoffs` - Whether to return Playoff stats or not. One of `True|False`

Returns:

  A Pandas Series containing the following columns:

  ```
  ['NUMBER', 'PLAYER', 'POS', 'HEIGHT', 'WEIGHT', 'BIRTH_DATE', 
    'NATIONALITY', 'EXPERIENCE', 'COLLEGE']
  ```

### `get_team_misc(team, season, data_format='PER_GAME')`

Parameters:
  - `team` - NBA team abbreviation (e.g. `GSW`, `SAS`)
  - `season` - Desired year (e.g. `1988`, `2011`)
  - `data_format` - One of `'PER_GAME'|'RANK'`. Default value is `'PER_GAME'`.

Returns:

  A Pandas Series containing the following columns:

  ```
  ['W', 'L', 'PW', 'PL', 'MOV', 'SOS', 'SRS', 'ORtg', 'DRtg', 'Pace', 'FTr', '3PAr', 'eFG%', 'TOV%', 'ORB%', 
  'FT/FGA', 'eFG%', 'TOV%', 'DRB%', 'FT/FGA', 'Arena', 'Attendance']
  ```

### `get_player_salaries(team, season)`

Parameters:
  - `team` - NBA team abbreviation (e.g. `GSW`, `SAS`)
  - `season` - Desired year (e.g. `1988`, `2011`)

Returns:

  A Pandas DataFrame containing the following columns:

  ```
  ['Name', 'Salary']
  ```

## Players

### `get_stats(name, stat_type='PER_GAME', playoffs=False, career=False)`

Parameters:
  - `name` - Player full name (e.g. `'LaMarcus Aldridge'`)
  - `stat_type` - One of `'PER_GAME', 'PER_MINUTE', 'PER_POSS', 'ADVANCED'` 
  - `playoffs` - Whether to return Playoff stats or not. One of `True|False`. Default value is `'False'`
  - `career` - Whether to return career stats or not. One of `True|False`. Default value is `False` 

Returns:

  A Pandas DataFrame that varies based on the parameters. Please refer to a [sample page](https://www.basketball-reference.com/players/a/aldrila01.html) for full details.

## Seasons

### `get_schedule(season, playoffs=False)`

Parameters:
  - `season` - Desired year (e.g. `1988`, `2011`)
  - `playoffs` - Whether to return Playoff stats or not. One of `True|False`. Default value is `'False'`

Returns:

  A Pandas DataFrame that varies based on the parameters. Please refer to a [sample page](https://www.basketball-reference.com/players/a/aldrila01.html) for full details.

### `get_standings(date=None)`

Parameters:
  - `date` - Desired date in a string format (e.g. `'2011-12-01'`). Default value is `NONE`, which returns standings for the current date.

Returns:

  A dictionary containing standings for the Eastern and Western Conferences along with relevant statistics as a Pandas DataFrame. For example:

  ```
  >>> d = get_standings()
  >>> list(d['Western Conference'].columns)
  ['Western Conference', 'W', 'L', 'W/L%', 'GB', 'PW', 'PL', 'PS/G', 'PA/G']
  ```
