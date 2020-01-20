import requests
from PlayerInfo import PlayerInfo
from copy import deepcopy
import numpy as np 
import pandas as pd

class GeneralStats:
    
    def __init__(self,league):
        self.pi = PlayerInfo() # not permanent one class will be composed of all types of stats
        self.league = league
        self.identity = []
        self.goals = []
        self.assists = []
        self.apps = []
        self.mins = []
        self.yellows = []
        self.reds = []
        self.sub_on = []
        self.sub_off = []
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
        pages = self.get_(stat)
        for page in pages:
            for player in range(len(page['stats']['content'])):
                if stat == "goals":
                    self.goals.append(tuple((int(page['stats']['content'][player]['owner']['playerId']),int(page['stats']['content'][player]['value']))))
                elif stat == "assists":
                    self.assists.append(tuple((int(page['stats']['content'][player]['owner']['playerId']),int(page['stats']['content'][player]['value']))))
                elif stat == "apps":
                    self.apps.append(tuple((int(page['stats']['content'][player]['owner']['playerId']),int(page['stats']['content'][player]['value']))))
                    
    #take df.index (id) from self .pi and make a new DataFrame with that index & and extra columns all filled with NaN called self.gs
    #wherever the id matches index, fill in the appropriate stat
    def create_gs_df(self):
        list_of_ids = {
                "goals": [],
                "assists": [],
                "apps": []
                }
        list_of_vals = {
                "goals": [],
                "assists": [],
                "apps": []
                }
        # collect ids from goals
        for val in self.goals:
            list_of_ids['goals'].append(val[0])
            list_of_vals['goals'].append(val[1])
        # collect ids from assists
        for val in self.assists:
            list_of_ids['assists'].append(val[0])
            list_of_vals['assists'].append(val[1])
        # collect ids from apps
        for val in self.apps:
            list_of_ids['apps'].append(val[0])
            list_of_vals['apps'].append(val[1])

        # create dataframes
        goals_df = pd.DataFrame(index=list_of_ids['goals'],columns=['Goals'])
        assists_df = pd.DataFrame(index=list_of_ids['assists'],columns=['Assists'])
        apps_df = pd.DataFrame(index=list_of_ids['apps'],columns=['Appearances'])
        # fill dataframes
        goals_df['Goals'] = list_of_vals['goals']
        assists_df['Assists'] = list_of_vals['assists']
        apps_df['Appearances'] = list_of_vals['apps']
        # join dataframes
        self.gs = goals_df.join(assists_df,how='outer').join(apps_df,how='outer')
            
        
                
g = GeneralStats('EN_PR')
g.parse_stats('goals')
g.parse_stats('apps')
g.parse_stats('assists')
g.create_gs_df()
print(g.gs)
#print(g.pi.df)

#print(len(g.goals))
#print(len(g.assists))
#print(g.apps)