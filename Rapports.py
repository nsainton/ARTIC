#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 16:12:24 2022

@author: noahsaintonge

Module that contains useful functions to realize a complete data analysis
of ARTIC data about the patients.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Analysis of a medical dataFrame with a few data in it to try and do the
#maximum with the data we got
#First step: dataFrame preparation and implementation of functions that
#will allow us to do the proper analysis

#We are going to analyse the dataFrame following the following plan
#First, we are going to represent therapist by therapist how much patients
#they got and how frequently they came back after coming for the first time
#in the therapist office

#Second, we are going to represent year by year the evolution of attendance
#of the differents activities offered by the association

#thirdly, we are going to represent some more general statistics about the
#whole inpact of the prendre soin activities on the patients and physicians

#Finally, we are going to analyse which service prescripts more consultations
#for the prendre soin activities


def keep_last(name):
    """Only keeps the last name of a patient
    
        Parameters
        ----------
        name : string
            Full name of the patient
        
        Returns
        -------
        last : string
            Last name of the patient
    """
    last = ''
    for c in name:
        if(65 <= c <= 90 or c == ' ') : last+=c
    last = last.strip()
    return last

def formate(df):
    """Keeps relevant info about the pandas DataFrame and renames some columns
    
    Parameters
    ----------
    df : pandas DataFrame
        The DataFrame that contains the relevant information and that you
        want to modify to make it usable
    
    Returns
    -------
    new_df : pandas DataFrame
        The DataFrame that has been modified according to the requierements of
        the study
    """
    total = list(df)[-1]
    new_df = df.rename(columns = {total : 'TOTAL', 'SERVICE 1' : 'SERVICE'})
    new_df = new_df[new_df['TOTAL'] > 0]
    columns = list(new_df)
    columns = [i for i in columns if i not in ['TOTAL', 'SERVICE','PATIENT']]
    print(columns)
    if('ORGANE' in columns):
        columns = [i for i in columns if i not in ['ORGANE', 'SEXE']]
    new_df.drop(columns, axis = 1, inplace = True)
    new_df = new_df[:-1] #removes last row of df
    return new_df


def set_service(df):
    """ Function to set the hospital service to a standard name in order
        to graphically plot the needed data
    
    Parameters
    ----------
    df : pandas DataFrame
        DataFrame that contains the column you need to modify string values
    
    Returns
    -------
    new_df : pandas DataFrame
        The modified DataFrame with one unique name for the same service

    """
    SERVICES = {'THO' : 'ONCOTHORACIQUE', 'DIG' : 'ONCODIG',\
                'CHOLO' : 'PSY', 'CH' : 'HDJ',\
                'GINECO' : 'GYNECO', 'GYN' : 'GYNECO', 'DIO' : 'RADIOTHERAPIE'}
    #Declaration of a dictionnary of services to correctly format the
    #DataFrame with the function set_service
    new_df = df
    for i in new_df.index:
        a = str(new_df.loc[i, 'SERVICE'])
        for k,v in SERVICES.items():
            if (k in a):
                new_df.loc[i, 'SERVICE'] = v
    return new_df

def find_os(dict_of_df = {}, df = pd.DataFrame(), attribute = None):
    """

    Parameters
    ----------
    dict_of_df : dict, optional
        dictionnary of DataFrames that contains the needed attribute. Is set 
        by default to an empty dictionnary to not be considered by the 
        function. The default is {}
    df : TYPE, optional
        DataFrame that contains the needed attribute. Is set by default to an 
        empty DataFrame to not be considered by the function. The default is 
        pd.DataFrame()
    attribute : str, optional
        Column of the DataFrame to search in. The default is None.

    Returns
    -------
    cols : list
        list of unique values encountered in the attribute column of the final.
        DataFrame

    """
    if(len(dict_of_df) == 0):
        bilan = pd.concat(dict_of_df.values())
    if(len(df) == 0) : 
        bilan = df
    col = bilan[attribute].dropna(axis = 0)
    cols = np.unique(col, return_counts = False)
    cols = [col.strip() for col in cols]
    cols = list(dict.fromkeys(cols)) #removes duplicates from the given list
    return cols

def stat_services(df):
    """Displays the proportion of patient that came prescripted by each service
       and for each organe already registered in the database
       
       Parameters
       ----------
       df : pandas DataFrame
           Contains the information for one workshop in one year
        
       Display
       -------
       Displays two pies. The first one is a pie that shows the proportion of
       patients that came from each service and the second one shows the
       proportion of patients that came for each organ
    """
    new_df = set_service(df)
    new_df.dropna(subset = ['SERVICE', 'ORGANE'], inplace = True)
    prescriptions = {}
    organs = {}
    SERVICES = find_os(df = df, attribute = 'SERVICE')
    ORGANS = find_os(df = df, attribute = 'ORGANE')
    for service in SERVICES:
        prescriptions[service] = new_df[new_df['SERVICE'] == service].size
    for organ in ORGANS:
        organs[organ] = new_df[new_df['ORGANE'] == organ].size
    services = list(prescriptions.values())
    organ = list(organs.values())
    plt.figure(figsize = (15,15))
    plt.pie(services, labels = SERVICES, normalize = True, shadow = True,\
            autopct = lambda x : str(round(x,2)) + '%')
    plt.legend(loc = 'lower right')
    plt.title('Pourcentage de pass prescrits par service', y = -0.01)
    plt.show()
    plt.figure(figsize = (15,15))
    plt.pie(organ, labels = ORGANS, normalize = True, shadow = True,\
            autopct = lambda x : str(round(x,2)) + '%')
    plt.legend(loc = 'lower right')
    plt.title('Proportion d\'organes touchés', y = -0.01)
    plt.show()
    return None

def stat_comebacks(df, low = 0, middle = 1, high = 4, graphic = True):
    """Function to display the number of patients who came a giver number
        of times for two number. And display the percentage of patients 
        that are in both groups.
        
        Parameters
        ----------
        df : pandas DataFrame
            DataFrame that countains the number of meetings that each
            patient went to
        low : int (optionnal)
            int such that you're looking for the number of patients
            that wen more than #low times. Default value is 0
        middle : int
            int such that you're looking for the number of patients
            that wen more than #middle times. Default value is 1
        high : int
            int such that you're looking for the number of patients
            that wen more than #high times. Default value is 4
        graphic : bool (optionnal)
            if graphic = True (default), then the number of patients that came
            more to #low, #middle and #high meetings are printed along with
            the percentage of people that came more than #high times and the 
            percentage of people that came more than #middle times. A pie chart
            is also printed with all those percentages. if graphic = False,
            nothing is printed but the number of people that came more than
            #low and less than #middle times, more than #middle and less than 
            #high and more than #high times are returned
        
        Returns
        -------
        tuple (optionnal)
            number of people that came more than #low and less than #middle 
            times, more than #middle and less than #high and more than 
            #high times
    """
    n_low = df[df['TOTAL']>low]['TOTAL'].size
    n_middle = df[df['TOTAL']>middle]['TOTAL'].size
    n_high = df[df['TOTAL']>high]['TOTAL'].size
    percentage_2 = n_high/n_low
    percentage_1 = n_middle/n_low
    if(graphic):
        print(f'Nombre de patients venus plus de {low} fois :', n_low)
        print(f'Nombre de patients venus plus de {middle} fois :',n_middle)
        print(f'Nombre de patients venus plus de {high} fois :',n_high)
        print('Pourcentage 0-4: ', str(percentage_2*100) + '%')
        print('Pourcentage 0-1: ', str(percentage_1*100) + '%')
        plt.figure(figsize = (10,10))
        persons = [n_low-n_middle, n_middle-n_high, n_high]
        plt.pie(persons, labels = ['1 visite','2-4 visites', '+4 visites'],\
                normalize = True, colors = ['red', 'green', 'orange'],\
                shadow = True, autopct = lambda x : str(round(x,2)) + '%')
        plt.legend()
        return None
    else:
        return (n_low-n_middle, n_middle-n_high, n_high)

def stat_genre(df):
    """Function that gives the percentage of men and women that attended
       a given workshop
       
       Parameters
       ----------
       df : pandas DataFrame
           Contains the information about the patients and more specifically
           their genre
    """
    men = df[df['SEXE'] == 'H']
    print(men.head())
    women = df[df['SEXE'] == 'F']
    men = stat_comebacks(men, graphic = False)
    women = stat_comebacks(women, graphic = False)
    once = (sum(men),sum(women))
    plt.figure(figsize = (12,10))
    plt.pie(once, labels = ['hommes','femmes'], normalize = True,\
            shadow = True, autopct = lambda x : str(round(x,2)) + '%',\
            colors = ['blue','red'])
    plt.legend()
    plt.title('Part des hommes et des femmes', y = -0.01)
    plt.show()
    return None

def patients_count(df, graphic = True):
    """Prints the statistic of one DataFrame and eventually returns the 
        number of meetings for one workshop
        
        Parameters
        ----------
        df : pandas DataFrame
            DataFrame that contains the relevant informations about the
            patients
        graphic : boolean (optionnal)
            if graphic = True (default value), then the statistics and the
            total number of meetings for a workshop is displayed and nothing
            is returned. If graphic = False, then nothing is displayed and the
            total number of meetings is returned
        
        Returns
        -------
        number_of_meeting : int (optionnal)
            total number of meetings for one workshop and a year
    """
    patients_count = df['TOTAL']
    statistics = patients_count.describe()
    number_of_meetings = sum(patients_count)
    if(graphic):
        patients_count.sort_values().value_counts(sort = False).plot.bar()
        print("some statistics about the patients\n", statistics)
        print("number of meetings :", number_of_meetings)
        return None
    else:
        return number_of_meetings

def stats_generales(datas, year):
    """Prints some general statistics about a given workshop
    
    Parameters
    ----------
    datas : dictonnary
        dictonnary of values that correspond to a given information about
        the patients and the workshop
    """
    plt.figure(figsize = (12, 8))
    x = list(range(2019,year + 1))
    plt.plot(x, datas['1rdv'], 'r', label = '1 consultation')
    plt.plot(x, datas['+1rdv'], 'g', label = '2-4 consultations')
    plt.plot(x, datas['+4rdv'], 'b', label = '+4 consultations')
    plt.plot(x, datas['nom'], label = 'nombre de consultations')
    plt.legend()
    plt.show()
    return None

def get_data(dict_of_df):
    """Get the data from the dictionnary of DataFrames for the number of
        consultations and the number patients that went to 1, between 2 and 4 
        and more than 4 meetings to the workshop
    
        Parameters
        ----------
        dict_of_df : dictionnary
            contains the pandas DataFrames of all the workshop sorted by year
            and workshop
        
        Returns
        -------
        datas : dictionnary
            dictionnary with all the needed information to analyse the data
    """
    one_consult = []
    less_four = []
    more_four = []
    number = []
    for i in dict_of_df.keys():
        df = dict_of_df[i]
        (one,lf,mf) = stat_comebacks(df, graphic = False)
        one_consult.append(one)
        less_four.append(lf)
        more_four.append(mf)
        nom = patients_count(df, graphic = False)
        number.append(nom)
    datas = {'1rdv' : one_consult, '+1rdv' : less_four,\
            '+4rdv' : more_four, 'nom' : number}
    return datas

def assemble_yearly(dict_of_df, year):
    """Will concatenate different DataFrames to get more general data about
        the workshops
        
        Parameters
        ----------
        dict_of_df : dictionnary
            dictionnary that contains the pandas DataFrames needed to be
            concatenated
        year : int or string
            year formated as aaaa that will be used to select the right
            DataFrames to concatenate
        
        Returns
        -------
        year_concat : pandas DataFrame
            DataFrame that contains the concatenation of all the DataFrames
            selected
    """
    year = str(year)
    new_dict = {k: v for (k,v) in dict_of_df.items() if year in k}
    year_concat = pd.concat(new_dict.values(), ignore_index = True)
    return year_concat

def workshop(therapeute):
    """
    

    Parameters
    ----------
    therapeute : str
        String containing the sheet name with the name of the therapeute and
        the associated year.

    Returns
    -------
    str
        The name of the workshop associated with the provided therapeute .

    """
    
    if ('Caroline' in therapeute) :
        return 'REFLEXOLOGIE'
    if ('Sylvie' in therapeute) :
        return 'OSTHEOPATHIE'
    if ('Sabine' in therapeute) :
        return 'AURICULOTHERAPIE'
    if ('Magalie' in therapeute) :
        return 'HYPNOSE'

def multi_therapies(dict_of_df):
    year = pd.concat(dict_of_df.values())
    print(year)
    duplicates = year[year.duplicated(subset = ['PATIENT'])]
    #function duplicated only remove one duplicate if there are more than one
    duplicate = {}
    for i in duplicates['PATIENT']:
        duplicate[str(i)] = []
    for k,v in dict_of_df.items():
        for ke in duplicate.keys():
            if ke in v['PATIENT'].unique() : 
                duplicate[ke].append(workshop(k))
    for k in duplicate.keys():
        duplicate[k] = list(dict.fromkeys(duplicate[k]))
    return duplicate


def main(df, dict_of_df, bilan = False):
    """Run main programme routine

    Parameters
    ----------
    df : pandas DataFrame
        DataFrame to analyse
    """
    patients_count(df)
    stat_comebacks(df)
    if(bilan):
        datas = get_data(dict_of_df)
        stats_generales(datas)
        bilan = pd.concat(dict_of_df.values())
        patients_count(bilan)
        stat_comebacks(bilan)

