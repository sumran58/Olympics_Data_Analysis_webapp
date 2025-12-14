import pandas as pd

def preprocess(df,region_df):

    #filtering for summer olympics
    df=df[df['Season']=='Summer']
    #we will merge with region df
    df=df.merge(region_df,on='NOC',how='left')
    #drop all the duplicates
    df.drop_duplicates(inplace=True)
    #one hot encoding the medal
    df=pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    return df

