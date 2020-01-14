from basketball_reference_scraper.teams import get_roster, get_team_stats, get_opp_stats, get_roster_stats, get_team_misc

df = get_roster('GSW', 2019)
print(df)

s = get_team_stats('GSW', 2019, data_format='PER_GAME')
print(s)

s = get_opp_stats('GSW', 2019, data_format='PER_GAME')
print(s)

s = get_roster_stats('GSW', 2019, data_format='PER_GAME', playoffs=False)
print(s)

s = get_team_misc('GSW', 2019)
print(s)

from basketball_reference_scraper.players import get_stats

s = get_stats('Stephen Curry', stat_type='PER_GAME', playoffs=False, career=False)
print(s)

from basketball_reference_scraper.seasons import get_schedule, get_standings

s = get_schedule(2018, playoffs=False)
print(s)

s = get_standings(date='2020-01-06')
print(s)

from basketball_reference_scraper.box_scores import get_box_scores

s = get_box_scores('2020-01-13', 'CHI', 'BOS', period='GAME', stat_type='BASIC')
print(s)

from basketball_reference_scraper.pbp import get_pbp

s = get_pbp('2020-01-13', 'CHI', 'BOS')
print(s)

from basketball_reference_scraper.shot_charts import get_shot_chart

s = get_shot_chart('2020-01-13', 'CHI', 'BOS')
print(s)

from basketball_reference_scraper.injury_report import get_injury_report

s = get_injury_report()
print(s)
