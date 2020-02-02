import requests
import re
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
        # dictionary of lists to store data for all players
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
        # list for relevant club names
        self.clubs = []
        # link for football api
        self.players_url = "https://footballapi.pulselive.com/football/teams/?/compseasons/274/staff?pageSize=30&compSeasons=274&altIds=true&page=0&type=player"
        # link for current premier league clubs
        self.clubs_url = "https://www.premierleague.com/clubs"
        # initialize pandas DataFrame object
        self.df = pd.DataFrame()
        # web-scrape clubs
        self.get_clubs()
        # fetch player info based on clubs
        self.get_player_info()
        # convert the data from dict to dataframe and clean
        self.convert_to_df()
        
    def get_clubs(self):
        response = requests.get(self.clubs_url)
        soup = BeautifulSoup(response.content,'html.parser')
        clubs_list = soup.find_all("a")
        #extract href links because they contain club number
        clubs_links = [link['href'] for link in clubs_list]
        #narrow down to links that have this regex pattern
        clubs = [link for link in clubs_links if re.search('clubs/[0-9]+',link)]
        #tidy-up club names
        for i in range(len(clubs)):
            clubs[i] = clubs[i].replace('-and-','-&-')
            clubs[i] = clubs[i].replace('-',' ')
        #split link to get club number & club name in tuples
        self.club_and_num = [(i.split("/")[2],i.split("/")[3]) for i in clubs]
    
    def get_player_info(self):
        response = dict()
        # for each club
        for i in range(len(self.club_and_num)):
            response = requests.get(self.players_url.replace(f'teams/?/',f'teams/{self.club_and_num[i][0]}/')).json()
            try: 
                players = response['players']
                #for every player in the club
                for p in players:
                    try:
                        self.player_info['id'].append(int(p['id']))
                        self.player_info['name'].append(p['name']['display'])
                        self.player_info['role'].append(p['info']['position'])
                        self.player_info['position'].append(p['info']['positionInfo'])
                        try: 
                            self.player_info['shirtNum'].append(int(p['info']['shirtNum']))
                        except:
                            self.player_info['shirtNum'].append(0)
                        try:
                            self.player_info['club'].append(self.club_and_num[i][1])
                        except:
                            self.player_info['club'].append('N/A')
                        try:
                            self.player_info['country'].append(p['birth']['country']['country'])
                        except:
                            self.player_info['country'].append('N/A')
                        try:
                            self.player_info['dob'].append(str(parse(p['birth']['date']['label']).date()))
                        except:
                            self.player_info['dob'].append('N/A')
                    except:
                        pass
            except:
                pass
            response = dict()
            
    def convert_to_df(self):
        #convert to pandas dataframe
        self.df = pd.DataFrame.from_dict(self.player_info,orient='columns')
        #use unique player id as index
        self.df.set_index('id',inplace=True)
        #clean some data
        self.df.replace('N/A',np.NaN,inplace=True)
        self.df['shirtNum'].replace(0,np.NaN,inplace=True)
        #capitalize first letter of column names
        self.df.columns = [x.title() for x in self.df.columns]
        self.df.rename(columns={ "club":"Club","country":"Country","dob":"Dob","name":"Name","position":"Position","role":"Role","shirtNum":"Shirt Number"},inplace=True)
        

