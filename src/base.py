import requests
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from os import getenv
load_dotenv()

class Base:
    """
    Class handles all connection to the API object and returns a dataframe
    from it's initialization. 
    """

    def __init__(self):

        self.api_url = "https://www.dnd5eapi.co/api"
        self.req = requests.get(self.api_url)
        self.base_dict = self.req.json()
        #used for iterating through larger dictionaries as a base string
        self.base_url = "https://www.dnd5eapi.co"
        self.get_monsters() 

    def get_monsters(self):
        '''Scraping data from the API and creating a Dataframe from it'''
        '''We create the mystr,response,and monsters locally'''
        mystr= 'https://www.dnd5eapi.co/api/monsters/'
        response= requests.get(mystr).json()['results']
        monsters=[]
        #iterate through the urls from the previous response
        for i in response:
            newstr=self.base_url+(i['url'])
            mdata= requests.get(newstr).json()
            monsters.append(mdata)

        self.df_mon = pd.DataFrame.from_dict(monsters)
        #extract the natural ac from the table
        self.df_mon['natural_ac']= [ac[0]['value'] for ac in self.df_mon.armor_class] 
        #extract the speeds from the nested data columns
        walk =[]
        swim=[]
        fly=[]
        burr=[]
        for s in self.df_mon.speed:
            try:
                walk.append(s['walk'].split(" ")[0])
            except:
                walk.append(np.nan)
            try:
                swim.append(s['swim'].split(" ")[0])
            except:
                swim.append(np.nan)
            try:
                fly.append(s['fly'].split(" ")[0])
            except:
                fly.append(np.nan)
            try:
                burr.append(s['burrow'].split(" ")[0])
            except:
                burr.append(np.nan)


        self.df_mon['speed_walk']=walk
        self.df_mon['speed_swim']=swim
        self.df_mon['speed_fly']=fly
        self.df_mon['speed_burrow']=burr

        self.mon_csv=self.df_mon[['index','name','size','type','alignment','natural_ac','speed_walk','speed_swim','speed_fly','speed_burrow','strength','dexterity','constitution','intelligence','wisdom','charisma','challenge_rating','xp','image','desc']]
        self.mon_csv.rename(columns={'index': 'monster_id'}, inplace=True)
        self.mon_csv.rename(columns={'desc': 'descrip'}, inplace=True)
        return self.df_mon

if __name__ == '__main__':
    c= Base()
    print('grabbing monster data.')
    c.mon_csv.to_csv('src/data/monsters.csv',index=False)
    print('monster data complete.')