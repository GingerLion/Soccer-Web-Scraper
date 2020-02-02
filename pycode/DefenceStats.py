from generalstats import GeneralStats 
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

class DefenceStats(GeneralStats):
    def __init__(self,league):
        self.league = league
        self.role = "Defence"
        self.defence_urls = {
                "blocks":"https://footballapi.pulselive.com/football/stats/ranked/players/outfielder_block?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
                "interceptions":"https://footballapi.pulselive.com/football/stats/ranked/players/interception?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
                "tackles":"https://footballapi.pulselive.com/football/stats/ranked/players/total_tackle?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
                "lmtackles":"https://footballapi.pulselive.com/football/stats/ranked/players/last_man_tackle?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
                "clearances":"https://footballapi.pulselive.com/football/stats/ranked/players/total_clearance?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
                "h_clearances":"https://footballapi.pulselive.com/football/stats/ranked/players/head_clearance?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
                "abw":"https://footballapi.pulselive.com/football/stats/ranked/players/aerial_won?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
                "og":"https://footballapi.pulselive.com/football/stats/ranked/players/own_goals?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
                "err_2_goal":"https://footballapi.pulselive.com/football/stats/ranked/players/error_lead_to_goal?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
                "pens_conc":"https://footballapi.pulselive.com/football/stats/ranked/players/penalty_conceded?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
                "fouls":"https://footballapi.pulselive.com/football/stats/ranked/players/fouls?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
                "abl":"https://footballapi.pulselive.com/football/stats/ranked/players/aerial_lost?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true"
                }
        self.defence_info = {key:[] for key in self.defence_urls.keys()}
        self.defence_info = super().parse_stats(self.defence_urls.keys(),super().get_(self.defence_urls))
        self.df = super().create_df(self.defence_info,super().getStatsNames)