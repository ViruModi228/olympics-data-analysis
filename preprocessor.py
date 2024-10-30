import pandas as pd

def preprocess(athletes,regions):
    #summer olympics only
    athletes = athletes[athletes['Season'] == 'Summer']
    #merge regions
    athletes = athletes.merge(regions,on='NOC',how='left')
    #dropping duplicates
    athletes.drop_duplicates(inplace=True)
    #one hot encoding medals and concating

    athletes = pd.concat([athletes,pd.get_dummies(athletes['Medal']).astype('int')],axis=1)

    return athletes