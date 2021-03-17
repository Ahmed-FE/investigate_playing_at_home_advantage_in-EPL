
"""
Created on Fri Mar 5 13:15:08 2021
Finished in sunday march 14th with all modifications 

@author:Ahmed Elsayed Abdenaby Refaei 
"""
'''
 the first question I will try to answer is "Does play at home consider as an advantage for the home team
 in the english premier league ?
1) to answer this question I will compare the winning vs loosing percentage in the english premier league for 8 season from 2008/2009 to 2015/2016 .
2) I will take the data for 4 teams from the upper half of the table and see their winning rate when it come to play home or away .
3) then I will repeat the same process but then with the teams from the lower half of the table for a specific season . 
'''
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import sqlite3 
'''
I will have two helper function :
    1) get_pandas_table_from_database in which I will establish a connection with the databae and get a table information 
    2) I will have get_id_from_a_table this helper function gives id for a team or a country from table in the data base for specoific informations 
    as decribed 
'''

def get_pandas_table_from_database(file_name_with_bath,Table_name):
    '''
    a function to get a table from sqlite database 

    Parameters
    ----------
    file_name_with_bath : the url with the file name to the database 

    Returns
    -------
    pandas table  .

    '''
    
    # create a connection with the sqlite3 data base 
    connection_to_the_sqlite3_data_base = sqlite3.connect(file_name_with_bath)
    # use pandas to create some form of table to access the data as a table 
    df = pd.read_sql_query("SELECT * from '%s'" % Table_name, connection_to_the_sqlite3_data_base)
    return(df)

 
def get_id_from_a_table (Table_name,id_column_name,country_team_name,country_team_column_name):
    '''
     helper function #1
    this function is to get a specific value associated with a specific input to the table 
    for example : if we want to get the country id from the country table so we input the table name 
    then the column name is the 'id' or name of the column . then the country for which we want to get 
    the id such as 'England' lastly the name of the column in which england is existing in this example 
    it will be 'name'
    
    important note : this function looking for unique values that means it can find a value that 
    appear in the data once not more .

    Parameters
    ----------
    Table_name : name of the table .
    id_column_name : name of the column of what we want to find .
    country_team_name : the key word that we want to find.
    country_team_column_name : the column in which the key word should appear 
    

    Raises
    ------
    KeyError
        if the keyword entered in a wrong format or not in the data .

    Returns
    -------
    result : float with the id number .

    '''
    
    file_name_with_bath='E:\study_material\MIT_OPEN_COURSES\egypt_fwd\project_1\soccer_data.sqlite'
    
    table=get_pandas_table_from_database(file_name_with_bath,Table_name)
    country_id=table[id_column_name].where(table[country_team_column_name] ==country_team_name)
    country_id_bool=country_id.isna()
    if not country_id_bool.all():
        result=float(country_id.dropna())
        return (result)
    else:
        raise KeyError('the country is not in the list ')

def season_results_for_a_team_or_country(table_name,id_column_name,country_team_column_name,country_team_name,column_name_in_match_table,season):
   
    # this part to make sure if there is any mistake with entering the format of the name it will handle 
    # it or ask the user to handle it 
   
    if country_team_name[0].islower()==True:
            first_letter=country_team_name[0].upper()
            country_team_name=first_letter+country_team_name[1:]
    try:  
            Country_team_id=get_id_from_a_table(table_name,id_column_name,country_team_name,country_team_column_name)
    except KeyError:
            print('country is not in the data ')

    file_name_with_bath='E:\study_material\MIT_OPEN_COURSES\egypt_fwd\project_1\soccer_data.sqlite'
    Table_name_2=('Match')
    matches_information=get_pandas_table_from_database(file_name_with_bath,Table_name_2)
    condition_1=matches_information[column_name_in_match_table]==Country_team_id 
    condition_2=matches_information['season'] ==season
    if condition_2.any():
        Home_team_goals=matches_information['home_team_goal'].where(condition_1 & condition_2)
        away_team_goals=matches_information['away_team_goal'].where(condition_1 & condition_2)
        matches= pd.concat([Home_team_goals, away_team_goals], axis=1, join="inner")
        matches=matches.dropna()
       
        #this part is to create a third column with the result 
        matches['home_team_result']='string'
        matches.loc[matches.home_team_goal == matches.away_team_goal, "home_team_result"] = "draw"
        matches.loc[matches.home_team_goal > matches.away_team_goal, "home_team_result"] = "win"
        matches.loc[matches.home_team_goal < matches.away_team_goal, "home_team_result"] = "lose"
        return(matches)
    else:
        raise KeyError('the season is not in the data or in the wrong format(please note the season has to be in xxxx/xxxx')
 


def percentage_of_winning_losing_for_home_team(season_results):
    '''
    this function take the season result pandas table with columns "home_team_goal","away_team_goal" and "home_team_result"
    and return a tuple with the first elements is the winning percentage of the home team and the second element is the 
    losses percentage of the home team 

    Parameters
    ----------
    season_results : panda table contains three columns "home_team_goal","away_team_goal" and "home_team_result"

    Returns
    -------
    a tuple with the first elements is the winning percentage of the home team and the second element is the 
    losses percentage of the home team

    '''
    
    wins=season_results.home_team_result.str.count('win').sum()
    length_of_the_data= season_results.shape[0]
    win_percentage=(wins/length_of_the_data)*100
    losses=season_results.home_team_result.str.count('lose').sum()
    losses_percentage=(losses/length_of_the_data)*100

    result=(win_percentage,losses_percentage)
    return(result)
def number_of_games_that_home_team_wins_or_lose_in_a_season(season_results):
    '''
    this function take the season result pandas table with columns "home_team_goal","away_team_goal" and "home_team_result"
    and return a tuple with the first elements is the winning percentage of the home team and the second element is the 
    losses percentage of the home team 

    Parameters
    ----------
    season_results : panda table contains three columns "home_team_goal","away_team_goal" and "home_team_result"

    Returns
    -------
    a tuple with the first elements is the winning percentage of the home team and the second element is the 
    losses percentage of the home team

    '''
    
    wins=season_results.home_team_result.str.count('win').sum()
    losses=season_results.home_team_result.str.count('lose').sum()
    result=(wins,losses)
    return(result)

def create_data_frame_to_plot_result(table_name,id_column_name,country_team_column_name,country_team_name_list,column_name_in_match_table,list_of_seasons,*argv):
    '''
    this function is the main function that has been used to develop the data frames and calling all the helper functions
    used for the analysis.
    the new part here is the *argv which allows me to give any number of argument it can be two as 
    in countries analyis or three as in teams analysis.
    you can see the first two argument is what do you want the label of your two data to be for instance if I am comparing winning at 
    home vs winning away that means i need to give two input 'winning_percentage_home','winning_percentage_away'
    the third arguments is just in case I am running the analyis to compare the winning of teams 
    in home vs winning away and this importnat it need to be 'away_team_api_id'
     

    Parameters
    ----------
    table_name : a described above name of the table 
    id_column_name : name of the column for team or countries` id
    country_team_column_name : name of the column for team or country
    country_team_name_list : name of the countries or team it has to be a list 
    column_name_in_match_table : the name of the column which contains the id in match table 
    list_of_seasons : which seasons to perform the analysis in it has to be a list 
    *argv :  the first two arguments are the label of your two data. 
    the third argument can be true or false depending on which analysis you want to conduct percentage or number of games 
    the last argument is 'away_team_api_id' if needed 
    Returns
    -------
    all_countries_winning_lossing_data_frame : TYPE
        DESCRIPTION.

    '''

    data_frames_list=[]
    for index ,country_team_name in enumerate(country_team_name_list) :
      seasons_list=[]
      winning_percentage_list=[]
      lossing_percentage_list=[]
      for season in list_of_seasons:
        season_name=season[-2:]
        season_result1=season_results_for_a_team_or_country(table_name,id_column_name,country_team_column_name,country_team_name,column_name_in_match_table,season)
        if argv[2]==True:
            season_result11=number_of_games_that_home_team_wins_or_lose_in_a_season(season_result1)
        else:
            season_result11=percentage_of_winning_losing_for_home_team(season_result1)
        seasons_list.append(season_name)
        winning_percentage_list.append(season_result11[0])
# this part is working when I need to calculate home and away results for the same team 
        try :
            # the argv part will be true if the required analysis want number of games not percentage of games 
             argv[3]=='away_team_api_id'
             season_result2=season_results_for_a_team_or_country(table_name,id_column_name,country_team_column_name,country_team_name,argv[3],season)
             if argv[2]==True:
                 season_result21=number_of_games_that_home_team_wins_or_lose_in_a_season(season_result2)
             else:
                 season_result21=percentage_of_winning_losing_for_home_team(season_result2)
             lossing_percentage_list.append(season_result21[1])
        except:
            lossing_percentage_list.append(season_result11[1])
    # create series for the winning at home data 
      winning_percentage_series= pd.Series(winning_percentage_list,index=np.array(seasons_list))
      lossing_percentage_series= pd.Series(lossing_percentage_list,index=np.array(seasons_list))
      single_country_winning_lossing_data_frame=pd.DataFrame({argv[0]:winning_percentage_series,argv[1]:lossing_percentage_series})
      data_frames_list.append(single_country_winning_lossing_data_frame)
      all_countries_winning_lossing_data_frame=pd.concat(data_frames_list,keys=country_team_name_list)
    return (all_countries_winning_lossing_data_frame)

def run_script(conduct_analysis_to_calculate_number_of_games,*argv):
    '''
    this function takes input boolean True to conduct_analysis_to_calculate_number_of_games and False for the percentage of winning 
    then in the *argv it takes weather to perform single analysis 
    for the sake of trying the code or just go with all the analysis.
    Parameters
    ----------
    conduct_analysis_to_calculate_number_of_games : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    table_name=['Team','Country']
    id_column_name=['team_api_id','id']
    country_team_column_name=['team_long_name','name']
# teams for 2008/2009 season 
    teams_08_09=['Manchester United','Liverpool','Chelsea','Arsenal','Everton','Aston Villa','Fulham',
 'Tottenham Hotspur','West Ham United','Manchester City','Wigan Athletic','Stoke City',
 'Bolton Wanderers','Portsmouth','Blackburn Rovers','Sunderland','Hull City','Newcastle United','Middlesbrough','West Bromwich Albion']
# teams for 2009/2010 season 
    teams_09_10=['Chelsea','Manchester United','Arsenal',
'Tottenham Hotspur','Manchester City','Aston Villa','Liverpool','Everton','Birmingham City','Blackburn Rovers','Stoke City','Fulham','Sunderland','Bolton Wanderers',
'Wolverhampton Wanderers','Wigan Athletic','West Ham United','Burnley','Hull City','Portsmouth']
    column_name_in_match_table=['home_team_api_id','country_id']
    seasons_09=['2008/2009']
    seasons_10=['2009/2010']
    try:
        argv[0]==True
        list_of_seasons=['2008/2009','2009/2010','2010/2011','2011/2012','2012/2013','2013/2014','2014/2015','2015/2016']
        countries=['England'] 
        results=create_data_frame_to_plot_result(table_name[1],id_column_name[1],country_team_column_name[1],countries,column_name_in_match_table[1],list_of_seasons,'winning_home','losing_Home',conduct_analysis_to_calculate_number_of_games)
        return(results)
    except:
          ## this part is for winning at home vs winning away for the same team in 2009 and 2010 seasons 
          results_09=create_data_frame_to_plot_result(table_name[0],id_column_name[0],country_team_column_name[0],teams_08_09,column_name_in_match_table[0],seasons_09,'winning_home','winning_away',conduct_analysis_to_calculate_number_of_games,'away_team_api_id')
          results_10=create_data_frame_to_plot_result(table_name[0],id_column_name[0],country_team_column_name[0],teams_09_10,column_name_in_match_table[0],seasons_10,'winning_home','winning_away',conduct_analysis_to_calculate_number_of_games,'away_team_api_id')
          results_09_2=create_data_frame_to_plot_result(table_name[0],id_column_name[0],country_team_column_name[0],teams_08_09,column_name_in_match_table[0],seasons_09,'winning_games_home','losing_games_home',conduct_analysis_to_calculate_number_of_games)
          results_10_2=create_data_frame_to_plot_result(table_name[0],id_column_name[0],country_team_column_name[0],teams_09_10,column_name_in_match_table[0],seasons_10,'winning_games_home','losing_games_Home',conduct_analysis_to_calculate_number_of_games)
          list_of_seasons=['2008/2009','2009/2010','2010/2011','2011/2012','2012/2013','2013/2014','2014/2015','2015/2016']
          countries=['England'] 
          results=create_data_frame_to_plot_result(table_name[1],id_column_name[1],country_team_column_name[1],countries,column_name_in_match_table[1],list_of_seasons,'winning_home','losing_Home',conduct_analysis_to_calculate_number_of_games)
          return ((results_09,results_09_2),(results_10,results_10_2),results)