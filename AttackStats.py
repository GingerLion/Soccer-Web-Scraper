import requests
import numpy as np
import pandas as pd
from GeneralStats import GeneralStats
from bs4 import BeautifulSoup

class AttackStats(GeneralStats):
    def __init__(self,league):
        self.role = "Attack"
        self.league = league
        self.attack_urls = {
            "shots": "https://footballapi.pulselive.com/football/stats/ranked/players/total_scoring_att?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
            "shots_on_target": "https://footballapi.pulselive.com/football/stats/ranked/players/ontarget_scoring_att?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
            "hit_woodwork": "https://footballapi.pulselive.com/football/stats/ranked/players/hit_woodwork?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
            "header_goals": "https://footballapi.pulselive.com/football/stats/ranked/players/att_hd_goal?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
            "penalty_goals": "https://footballapi.pulselive.com/football/stats/ranked/players/att_pen_goal?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
            "fk_goals": "https://footballapi.pulselive.com/football/stats/ranked/players/att_freekick_goal?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
            "offsides": "https://footballapi.pulselive.com/football/stats/ranked/players/total_offside?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
            "touches": "https://footballapi.pulselive.com/football/stats/ranked/players/touches?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
            "passes": "https://footballapi.pulselive.com/football/stats/ranked/players/total_pass?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
            "through_balls": "https://footballapi.pulselive.com/football/stats/ranked/players/total_through_ball?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
            "crosses": "https://footballapi.pulselive.com/football/stats/ranked/players/total_cross?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
            "corners": "https://footballapi.pulselive.com/football/stats/ranked/players/corner_taken?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true"
        }
        self.attack_info = {key:[] for key in self.attack_urls.keys()}
        self.attack_info = super().parse_stats(self.attack_urls.keys(),super().get_(self.attack_urls))
        self.df = super().create_df(self.attack_info,super().getStatsNames)
        