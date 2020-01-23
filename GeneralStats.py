import requests
from PlayerInfo import PlayerInfo
from copy import deepcopy
import pandas as pd
import numpy as np

class GeneralStats:
    
    def __init__(self,league):
        self.league = league
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
        #self.general_info = self.parse_stats(list(self.general_urls.keys()),self.get_(self.general_urls))
        #self.create_gs_df(self.general_urls.keys())
        
    def list_content_empty(self,li):
        """check if the end of json data is reached"""
        if not li:
            return True
        else:
            return False
    @staticmethod
    def get_(url_dict):
        # ls_responses will be a dict of lists which contain dictionaries
        ls_responses = {key:[] for key in url_dict.keys()}
        # for each stat run through each page
        for s in list(url_dict.keys()):
            i = 0
            response = dict()
            while True:
                if i > 0: # alter GET message to change pages
                    url_dict[s] = url_dict[s].replace(f'page={i-1}',f'page={i}')
                    response = requests.get(url_dict[s]).json()
                else:
                    response = requests.get(url_dict[s]).json()
                # if no more content
                if not response['stats']['content']:
                    break
                #print(response)
                ls_responses[s].append(response)
                i = i+1
                response = dict()
        return ls_responses
    
    @staticmethod
    def parse_stats(stat,pages):
        """
        Input: list of stat field names
        Process: parses json data from the api and stores it in
        the corresponding instance variables
        Return: dictionary of stats data
        """
        data_dict = {key: [] for key in stat}
        for s in stat:
            for page in pages[s]:
                for player in range(len(page['stats']['content'])):
                    data_dict[s].append(tuple((int(page['stats']['content'][player]['owner']['playerId']),int(page['stats']['content'][player]['value']))))
        return data_dict
    
    def create_gs_df(self, stat):
        list_of_ids = {key:[] for key in stat}
        list_of_vals = {key: [] for key in stat}
        
        # collect ids & values from instance dictionary 
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
g.general_info = g.parse_stats(list(g.general_urls.keys()),g.get_(g.general_urls))
g.create_gs_df(list(g.general_urls.keys()))
g.gs

        