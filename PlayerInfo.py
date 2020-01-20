import requests
import bs4
from bs4 import BeautifulSoup 
import numpy as np
import pandas as pd
from dateutil.parser import parse
from datetime import datetime 

class PlayerInfo:
    """ 
        1. This class fetches basic player information from a 'footballapi' API and web-scrapes
        the current premier league clubs in order to grab premier league player data only from the API
        2. This data is converted into a pandas dataframe to be used for analysis or to be joined with 
        player stats data based on player id
        3. Modifications will be made to allow the user to choose which soccer league player data
           they want to grab
    """
    def __init__(self):
        self.player_info = {
            'id' : [],
            'name' : [],
            'role' : [],
            'position': [],
            'shirtNum': [],
            'country' : [],
            'club' : [],
            'dob' : []
        }
        self.clubs = []
        self.players_url = "https://footballapi.pulselive.com/football/players?pageSize=30&compSeasons=274&altIds=true&page=0&type=player&id=-1&compSeasonId=274"
        self.clubs_url = "https://www.premierleague.com/clubs"
        self.get_clubs()
        self.get_player_info()
        self.convert_to_df()
        
    def get_clubs(self):
        response = requests.get(self.clubs_url)
        soup = BeautifulSoup(response.content,'html.parser')
        for clubName in soup.find_all("h4",{"class":"clubName"}):
            self.clubs.append(clubName.text)
        
    def list_content_empty(self,li):
        if not li['content']:
            return True
        else:
            return False
    
    def get_player_info(self):
        i = 0
        response = dict()
        
        while True:
            if i > 0:
                self.players_url = self.players_url.replace(f'page={i-1}',f'page={i}')
                response = requests.get(self.players_url).json()
            else:
                response = requests.get(self.players_url).json()
            
            
            if self.list_content_empty(response):
                break
            
            try: 
                players = response['content']
                for p in players:
                    try:
                        if p['currentTeam']['name'] in self.clubs:
                            self.player_info['id'].append(int(p['playerId']))
                            self.player_info['name'].append(p['name']['display'])
                            self.player_info['role'].append(p['info']['position'])
                            self.player_info['position'].append(p['info']['positionInfo'])
                            try: 
                                self.player_info['shirtNum'].append(int(p['info']['shirtNum']))
                            except:
                                self.player_info['shirtNum'].append(0)
                            
                            self.player_info['club'].append(p['currentTeam']['name'])
                            self.player_info['country'].append(p['birth']['country']['country'])
                            try:
                                self.player_info['dob'].append(str(parse(p['birth']['date']['label']).date()))
                            except:
                                self.player_info['dob'].append('N/A')
                    except:
                        pass
            except:
                pass
            
            
            i = i + 1
            response = dict()
            
    def convert_to_df(self):
        #convert to pandas dataframe
        self.df = pd.DataFrame.from_dict(self.player_info,orient='columns')
        #use unique player id as index
        self.df.set_index('id',inplace=True)
        #clean some data
        self.df.replace('N/A',np.NaN,inplace=True)
        self.df['shirtNum'].replace(0,np.NaN,inplace=True)
