import requests
from PlayerInfo import PlayerInfo
from copy import deepcopy
import pandas as pd
import numpy as np

class GeneralStats:
    
    def __init__(self,league):
        self.pi = PlayerInfo() # not permanent one class will be composed of all types of stats
        self.league = league
        self.general_info = {
            "goals": [],
            "assists": [],
            "apps": [],
            "mins": [],
            "yellows": [],
            "reds": [],
            "sub_on": [],
            "sub_off": []
        }
        self.general_urls = {
            "goals" : "https://footballapi.pulselive.com/football/stats/ranked/players/goals?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer=" + self.league + "&altIds=true",
            "assists" : "https://footballapi.pulselive.com/football/stats/ranked/players/goal_assist?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
            "apps" : "https://footballapi.pulselive.com/football/stats/ranked/players/appearances?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
            "mins" : "https://footballapi.pulselive.com/football/stats/ranked/players/mins_played?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
            "yellows" : "https://footballapi.pulselive.com/football/stats/ranked/players/yellow_card?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
            "reds" : "https://footballapi.pulselive.com/football/stats/ranked/players/red_card?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
            "sub_on" : "https://footballapi.pulselive.com/football/stats/ranked/players/total_sub_on?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true",
            "sub_off" : "https://footballapi.pulselive.com/football/stats/ranked/players/total_sub_off?page=0&pageSize=20&compSeasons=274&comps=1&compCodeForActivePlayer="+self.league+"&altIds=true"
        }
        self.parse_stats(self.general_info.keys())
        self.create_gs_df()
        
    def list_content_empty(self,li):
        """check if the end of json data is reached"""
        if not li['stats']['content']:
            return True
        else:
            return False
    
    def get_(self,stat):
        i = 0
        response = dict()
        ls_responses = []
        while True:
            if i > 0: # alter GET message to change pages
                self.general_urls[stat] = self.general_urls[stat].replace(f'page={i-1}',f'page={i}')
                response = requests.get(self.general_urls[stat]).json()
            else:
                response = requests.get(self.general_urls[stat]).json()
            # if no more content
            if self.list_content_empty(response):
                break
            #print(response)
            ls_responses.append(response)
            i = i+1
            response = dict()
        return ls_responses
    
    def parse_stats(self,stat):
            """
            Input: list of stat field names
            Process: parses json data from the api and stores it in
            the corresponding instance variables
            Output: None
            """
            for s in stat:
                pages = self.get_(s)
                for page in pages:
                    for player in range(len(page['stats']['content'])):
                        self.general_info[s].append(tuple((int(page['stats']['content'][player]['owner']['playerId']),int(page['stats']['content'][player]['value']))))
                       
    
    def create_gs_df(self):
        list_of_ids = {
                "goals": [],
                "assists": [],
                "apps": [],
                "mins": [],
                "yellows": [],
                "reds": [],
                "sub_on": [],
                "sub_off": []
                }
        list_of_vals = {
                "goals": [],
                "assists": [],
                "apps": [],
                "mins": [],
                "yellows": [],
                "reds": [],
                "sub_on": [],
                "sub_off": []
                }
        # collect ids & values from instance dictionary "general_info"
        for s in list_of_ids.keys():
            for val in self.general_info[s]:
                list_of_ids[s].append(val[0])
                list_of_vals[s].append(val[1])
            
        # create dataframes
        goals_df = pd.DataFrame(index=list_of_ids['goals'],columns=['Goals'])
        assists_df = pd.DataFrame(index=list_of_ids['assists'],columns=['Assists'])
        apps_df = pd.DataFrame(index=list_of_ids['apps'],columns=['Appearances'])
        mins_df = pd.DataFrame(index=list_of_ids['mins'],columns=['Minutes Played'])
        yellows_df = pd.DataFrame(index=list_of_ids['yellows'],columns=['Yellow Cards'])
        reds_df = pd.DataFrame(index=list_of_ids['reds'],columns=['Red Cards'])
        sub_on_df = pd.DataFrame(index=list_of_ids['sub_on'],columns=['Subbed On'])
        sub_off_df = pd.DataFrame(index=list_of_ids['sub_off'],columns=['Subbed Off'])
        
        # fill dataframes
        dfs = [goals_df,assists_df,apps_df,mins_df,yellows_df,reds_df,sub_on_df,sub_off_df]
        for df,keys in zip(dfs,list_of_vals.keys()):
            df[df.columns[0]] = list(map(int,list_of_vals[keys]))
            
        # join dataframes
        self.gs = dfs[0].join(dfs[1:],how='outer')
        # replace NaNs
        self.gs.fillna(0,inplace=True)
                
g = GeneralStats('EN_PR')
print(g.gs)