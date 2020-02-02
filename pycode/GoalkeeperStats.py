from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
from generalstats import GeneralStats

class GoalkeeperStats(GeneralStats):
    def __init__(self,league):
        self.league = league
        self.role = "Goalkeeper"
        self.gk_urls = {
            "clean_sheets": "https://footballapi.pulselive.com/football/stats/ranked/players/clean_sheet?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&positions=GOALKEEPER&altIds=true",
            "goals_conceded": "https://footballapi.pulselive.com/football/stats/ranked/players/goals_conceded?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&positions=GOALKEEPER&altIds=true",
            "saves": "https://footballapi.pulselive.com/football/stats/ranked/players/saves?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&positions=GOALKEEPER&altIds=true",
            "penalties_saved": "https://footballapi.pulselive.com/football/stats/ranked/players/penalty_save?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&positions=GOALKEEPER&altIds=true",
            "punches": "https://footballapi.pulselive.com/football/stats/ranked/players/punches?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&positions=GOALKEEPER&altIds=true",
            "high_claims": "https://footballapi.pulselive.com/football/stats/ranked/players/total_high_claim?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&positions=GOALKEEPER&altIds=true",
            "sweeper_clearances": "https://footballapi.pulselive.com/football/stats/ranked/players/total_keeper_sweeper?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&positions=GOALKEEPER&altIds=true",
            "throw_outs": "https://footballapi.pulselive.com/football/stats/ranked/players/keeper_throws?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&positions=GOALKEEPER&altIds=true",
            "goal_kicks": "https://footballapi.pulselive.com/football/stats/ranked/players/goal_kicks?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&positions=GOALKEEPER&altIds=true"
        }
        self.gk_info = super().parse_stats(self.gk_urls.keys(),super().get_(self.gk_urls))
        self.df = super().create_df(self.gk_info,super().getStatsNames)
        
#gk = GoalkeeperStats('EN_PR')
#print(gk.df)