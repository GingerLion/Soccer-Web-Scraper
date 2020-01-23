import numpy as np
import pandas as pd
from GeneralStats import GeneralStats

class AttackStats(GeneralStats):
    def __init__(self,league):
        super().__init__(league)
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
        self.create_df(self.attack_urls.keys())
        
    def create_df(self, stat):
        list_of_ids = {key:[] for key in stat}
        list_of_vals = {key:[] for key in stat}
        
        # collect ids & values from instance dictionary 
        for s in list_of_ids.keys():
            for val in self.attack_info[s]:
                list_of_ids[s].append(val[0])
                list_of_vals[s].append(val[1])
            
        # create dataframes
        shots_df = pd.DataFrame(index=list_of_ids['shots'],columns=['Shots'])
        sot_df = pd.DataFrame(index=list_of_ids['shots_on_target'],columns=['Shots On Target'])
        hw_df = pd.DataFrame(index=list_of_ids['hit_woodwork'],columns=['Hit Woodwork'])
        hg_df = pd.DataFrame(index=list_of_ids['header_goals'],columns=['Header Goals'])
        pg_df = pd.DataFrame(index=list_of_ids['penalty_goals'],columns=['Penalty Goals'])
        fkg_df = pd.DataFrame(index=list_of_ids['fk_goals'],columns=['Free Kick Goals'])
        offsides_df = pd.DataFrame(index=list_of_ids['offsides'],columns=['Offsides'])
        touches_df = pd.DataFrame(index=list_of_ids['touches'],columns=['Touches'])
        passes_df = pd.DataFrame(index=list_of_ids['passes'],columns=['Passes'])
        tb_df = pd.DataFrame(index=list_of_ids['through_balls'],columns=['Through Balls'])
        crosses_df = pd.DataFrame(index=list_of_ids['crosses'],columns=['Crosses'])
        corners_df = pd.DataFrame(index=list_of_ids['corners'],columns=['Corners'])
        
        # fill dataframes
        dfs = [shots_df,sot_df,hw_df,hg_df,pg_df,fkg_df,offsides_df,touches_df,passes_df,tb_df,crosses_df,corners_df]
        for df,keys in zip(dfs,list_of_vals.keys()):
            df[df.columns[0]] = list(map(int,list_of_vals[keys]))
            
        # join dataframes
        self.att_df = dfs[0].join(dfs[1:],how='outer')
        # replace NaNs
        self.att_df.fillna(0,inplace=True)
        
a = AttackStats('EN_PR')
print(a.att_df)