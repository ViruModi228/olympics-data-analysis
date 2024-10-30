import numpy as np
import pandas as pd

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')

    return years,country

def fetch_medal_tally(df,year,country):
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == year]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]
    
    if flag == 1:
        new_df = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year',ascending=True).reset_index()    
    else:
        new_df = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

    new_df['Total'] = new_df['Gold'] + new_df['Silver'] + new_df['Bronze']

    return new_df

def nations_per_time(df,value):
    data_per_year = df.drop_duplicates(['Year',value])['Year'].value_counts().reset_index()
    data_per_year.rename(columns={'count':value},inplace=True)
    return data_per_year

def most_successful(df,sport,country):
    temp_df = df.dropna(subset=['Medal'])

    if country != 'Overall':
        temp_df = temp_df[temp_df['region'] == country]
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    return temp_df['Name'].value_counts().reset_index().head(10).merge(df,left_on = 'Name',right_on='Name',how='left')[['Name','count','Sport','region']].drop_duplicates('Name')

def country_sport_heat(df,country):
    country_medal_df = df.dropna(subset=['Medal'])
    country_medal_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df = country_medal_df[country_medal_df['region'] == country]  # India
    new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count')

    return new_df

def get_age_distribution(df,sport,country):
    new_athelets = df.drop_duplicates(subset=['Name','region'])
    if sport == 'Overall' and country == 'Overall':
        pass
    if sport == 'Overall' and country != 'Overall':
        new_athelets = new_athelets[new_athelets['region'] == country]
    if sport != 'Overall' and country == 'Overall':
        new_athelets = new_athelets[new_athelets['Sport'] == sport]
    if sport != 'Overall' and country != 'Overall':
        new_athelets = new_athelets[(new_athelets['Sport'] == sport) & (new_athelets['region'] == country)]

    x1 = new_athelets['Age'].dropna()
    x2 = new_athelets[new_athelets['Medal'] == 'Gold']['Age'].dropna()
    x3 = new_athelets[new_athelets['Medal'] == 'Silver']['Age'].dropna()
    x4 = new_athelets[new_athelets['Medal'] == 'Bronze']['Age'].dropna()
    
    return x1,x2,x3,x4

def weight_height(df,sport,country):
    new_athelets = df.drop_duplicates(subset=['Name','region'])
    new_athelets['Medal'].fillna('No Medal',inplace=True)
    if sport == 'Overall' and country == 'Overall':
        temp_df = new_athelets
    elif sport == 'Overall' and country != 'Overall':
        temp_df = new_athelets[new_athelets['region'] == country]
    elif sport != 'Overall' and country == 'Overall':
        temp_df = new_athelets[new_athelets['Sport'] == sport]
    elif sport != 'Overall' and country != 'Overall':
        temp_df = new_athelets[(new_athelets['Sport'] == sport) & (new_athelets['region'] == country)]

    return temp_df

def men_women(df,df1,sport,country):
    if sport == 'Overall' and country == 'Overall':
        temp_df = df
        temp_df1 = df1
    elif sport == 'Overall' and country != 'Overall':
        temp_df = df[df['region'] == country]
        temp_df1 = df1[df1['region'] == country]
    elif sport != 'Overall' and country == 'Overall':
        temp_df = df[df['Sport'] == sport]
        temp_df1 = df1[df1['Sport'] == sport]
    elif sport != 'Overall' and country != 'Overall':
        temp_df = df[(df['Sport'] == sport) & (df['region'] == country)]
        temp_df1 = df1[(df1['Sport'] == sport) & (df1['region'] == country)]

    men = temp_df[temp_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = temp_df[temp_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    medal_men = temp_df1[temp_df1['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    medal_women = temp_df1[temp_df1['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women,on='Year',how='left')
    medal_final = medal_men.merge(medal_women,on='Year',how='outer')

    final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)
    medal_final.rename(columns={'Name_x':'Medal_Male','Name_y':'Medal_Female'},inplace=True)

    final.fillna(0,inplace=True)
    medal_final.fillna(0,inplace=True)

    final_medal = final.merge(medal_final,on='Year',how='outer')

    return final_medal

def athletes_country(df,df1,sport,country):
    if sport == 'Overall' and country == 'Overall':
        temp_df = df
        temp_df1 = df1
    elif sport == 'Overall' and country != 'Overall':
        temp_df = df[df['region'] == country]
        temp_df1 = df1[df1['region'] == country]
    elif sport != 'Overall' and country == 'Overall':
        temp_df = df[df['Sport'] == sport]
        temp_df1 = df1[df1['Sport'] == sport]
    elif sport != 'Overall' and country != 'Overall':
        temp_df = df[(df['Sport'] == sport) & (df['region'] == country)]
        temp_df1 = df1[(df1['Sport'] == sport) & (df1['region'] == country)]

    total_athletes = temp_df.drop_duplicates(['Year','Name'])['Year'].value_counts().reset_index()
    total_athletes.rename(columns={'count':'No of Athelets'},inplace=True)

    total_medal_athletes = temp_df1.drop_duplicates(['Year','Name'])['Year'].value_counts().reset_index()
    total_medal_athletes.rename(columns={'count':'No of Athelets'},inplace=True)

    final_athletes = total_athletes.merge(total_medal_athletes,on="Year")
    final_athletes.rename(columns={'No of Athelets_x':'total_athletes','No of Athelets_y':'medal_athletes'},inplace=True)

    return final_athletes
    