# basketball_reference_scraper

[Basketball Reference](https://www.basketball-reference.com/) is a great resource to aggregate statistics on NBA teams, seasons, players, and games. This package provides methods to acquire data for all these categories in pre-parsed and simplified formats.

## Wait, don't scrapers like this already exist?

Yes, scrapers and APIs do exist. The primary API used currently is for [stats.nba.com](https://stats.nba.com/), but the website blocks too many requests, hindering those who want to acquire a lot of data. Additionally, scrapers for [Basketball Reference](https://www.basketball-reference.com/) do exist, but none of them load dynamically rendered content. These scrapers can only acquire statically loaded content, preventing those who want statistics in certain formats (for example, Player Advanced Stats Per Game).
