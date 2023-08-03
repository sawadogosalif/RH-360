from datetime import timedelta,datetime
from functools import partial, reduce
from s2h_utils import *
from dateutil.relativedelta import *
import pandas as pd
import numpy as np



  

def reorganisation(data):
    
    """
    Algorithme  de réorganisation les données par périodes de congés prises.

        1. Ordorner les données by id ,date_debut et les classer selon selon la date_debut.
        2. Pour un id donné, 
            Si la date debut actuelle est suprieure à la date de debut précedente et la date de debut actuelle est inferieur
            à la date fin passée Alors retourner la date de debut precedende
            
        3. Etant données qu'on aura desormais des date_debut identiques  pour les dates qui se chevauchent alors
           Grouper par id, date_debut et ne retenir la dernire occurance de date_fin.
           
    
    Arguments:
          df {pd.DataFrame} --  dataframe

        Returns:
          pd.DataFrame
    """
    # 1
    #data["rank"]=data.groupby(by="id")["date_debut"].rank("first", ascending=True)
    data = data.sort_values(by = ['id', 'date_debut', 'date_fin'])
    # 2 !!les nan sont les premieres occurence de l'id , on rempli ces cases par la valeurs de debut elle-meme
    data['date_fin_shift'] = data.groupby(by="id")["date_fin"].shift()
    data['date_fin_shift'] = np.where(pd.isnull(data.date_fin_shift), data.date_debut, data.date_fin_shift) 

    data['date_debut_shift'] = data.groupby(by="id")["date_debut"].shift()
    cond  = (data.date_debut <= data.date_fin_shift) &  (data.date_debut >= data.date_debut_shift)
    data['date_debut'] = np.where(cond  , data.date_debut_shift, data.date_debut) 

    # 3
    data = data.sort_values(by = ['id', 'date_debut', 'date_fin'])
    data = data.groupby(["id","date_debut"]).agg({'date_fin':'last'}).reset_index()
    return data


def reorganisation_all(data):
    
    """This function allows each worker to merge registered 
       leave periods that overlap two by two or that are prolonged.
       It completes the function "reorganisation"
        
    Arguments:
      df {pd.DataFrame} -- Original table
     
    Returns:
      pd.DataFrame
       =====================================
        Input : 
        |id  |mois        |end         |
        |----|------------|------------|
        |1   |2017-11-20  |2017-12-15  |
        |1   |2017-11-21  |2017-12-17  |
        |1   |2018-03-20  |2018-03-27  |
        |2   |2017-11-20  |2017-11-21  |
        
        
        Output  : 
        |id  |mois        |end         |
        |----|------------|------------|
        |1   |2017-11-20  |2017-12-17  |
        |1   |2018-03-20  |2018-03-27  |
        |2   |2017-11-20  |2017-11-21  |
    """
    
    counter = 0
    while True:
        taille1 = len(data)
        data = reorganisation(data)
        taille2 = len(data)
        counter = counter + 1
        if taille1 == taille2:
            print(f"The algorithm stopped after {counter} iterations")
            break
    return data 


def get_days_month(data):
    
    low = data['date_debut']
    up = data['date_fin']
    
    # create a liste of months from min to max
    liste = [low]

    while low.strftime("%Y-%m")!=up.strftime("%Y-%m"):
        if is_monthend(low):
            low = low.replace(day=1) + relativedelta(months=1)
        else:
            low = low + relativedelta(day=31)
        liste.append(low)
        
     
        
    liste.append(up)
    liste = [[x, y] for x, y in zip(liste[:-1], liste[1:])]
    return liste


# total days in every month during non leap years
M_DAYS = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def isleap(year):
    """Return True for leap years, False for non-leap years."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def days_in_month(year, month):
    """Returns total number of days in a month accounting for leap years."""
    return M_DAYS[month] + (month == 2 and isleap(year))


def is_monthend(ref_date):
    """Checks whether a date is also a monthend"""
    return ref_date.day == days_in_month(ref_date.year, ref_date.month)
