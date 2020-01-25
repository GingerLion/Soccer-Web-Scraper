import pandas as pd
import numpy as np


class AllStats:
    def __init__(self,league):
        self.league = league
        self.objs = [
                PlayerInfo(),
                GeneralStats(self.league),
                AttackStats(self.league),
                DefenceStats(self.league),
                GoalkeeperStats(self.league)
        ]
        self.dfs = [obj.df for obj in self.objs]
        self.join_dfs()
        
    def join_dfs(self):
        self.df = self.dfs[0].join(self.dfs[1:],how='outer')
        self.df.fillna(0,inplace=True)
        
a = AllStats('EN_PR')
print(a.df.columns)
