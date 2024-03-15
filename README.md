# basketball_reference_scraper

[Basketball Reference](https://www.basketball-reference.com/) is a resource to aggregate statistics on NBA teams, seasons, players, and games. This package provides methods to acquire data for all these categories in pre-parsed and simplified formats.

## Installing
### Via `pip`
I wrote this library as an exercise for creating my first PyPi package. Hopefully, you find it easy to use.
Install using the following command:

```
pip install basketball-reference-scraper
```

### Via GitHub
Alternatively, you can just clone this repo and import the libraries at your own discretion.

### Selenium

This package can also capture dynamically rendered content that is being added to the page via JavaScript, rather than baked into the HTML. To achieve this, it uses [Python Selenium](https://selenium-python.readthedocs.io/). Please refer to their [installation instructions](https://selenium-python.readthedocs.io/installation.html) and ensure you have [Chrome webdriver](https://selenium-python.readthedocs.io/installation.html#drivers) installed in and in your `PATH` variable.

## Wait, don't scrapers like this already exist?

Yes, scrapers and APIs do exist. The primary API used currently is for [stats.nba.com](https://stats.nba.com/), but the website blocks too many requests, hindering those who want to acquire a lot of data. Additionally, scrapers for [Basketball Reference](https://www.basketball-reference.com/) do exist, but none of them load dynamically rendered content. These scrapers can only acquire statically loaded content, preventing those who want statistics in certain formats (for example, Player Advanced Stats Per Game).

Most of the scrapers use outdated methodologies of scraping from `'https://widgets.sports-reference.com/'`. This is outdated and Basketball Reference no longer acquires their data from there. Additionally, [Sports Reference recently instituted a rate limiter](https://www.sports-reference.com/bot-traffic.html) preventing users from making an excess of 20 requests/minute. This package abstracts the waiting logic to ensure you never hit this threshold.

### API
Currently, the package contains 5 modules: `teams`, `players`, `seasons`, `box_scores`, `pbp`, `shot_charts`, and `injury_report`. 
The package will be expanding to include other content as well, but this is a start.

For full details on the API please refer to the [documentation](https://github.com/vishaalagartha/basketball_reference_scraper/blob/master/API.md).
