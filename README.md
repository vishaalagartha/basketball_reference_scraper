# basketball_reference_scraper

[Basketball Reference](https://www.basketball-reference.com/) is a great resource to aggregate statistics on NBA teams, seasons, players, and games. This package provides methods to acquire data for all these categories in pre-parsed and simplified formats.

## Installing
### Via `pip`
I wrote this library as an exercise for creating my first PyPi package. Hopefully, you find it easy to use.
Install using the following command:

```
pip install basketball-reference-scraper
```

### Via GitHub
Alternatively, you can just clone this repo and import the libraries at your own discretion.

## Wait, don't scrapers like this already exist?

Yes, scrapers and APIs do exist. The primary API used currently is for [stats.nba.com](https://stats.nba.com/), but the website blocks too many requests, hindering those who want to acquire a lot of data. Additionally, scrapers for [Basketball Reference](https://www.basketball-reference.com/) do exist, but none of them load dynamically rendered content. These scrapers can only acquire statically loaded content, preventing those who want statistics in certain formats (for example, Player Advanced Stats Per Game).

### API
Currently, the package contains 5 modules: `teams`, `players`, `seasons`, `box_scores`, `pbp`, `shot_charts`, and `injury_report`. 
The package will be expanding to include other content as well, but this is a start.

For full details on the API please refer to the [documentation](https://github.com/vishaalagartha/basketball_reference_scraper/blob/master/API.md).
