import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.model_selection import train_test_split
import sklearn.preprocessing as pre

import env

###################################################
################## ACQUIRE DATA ###################
###################################################

def get_db_url(db, user=env.username, password=env.password, host=env.host):
    '''
    This function uses the imported host, username, password from env file, 
    and takes in a database name and returns the url to access that database.
    '''

    return f'mysql+pymysql://{user}:{password}@{host}/{db}' 

def new_zillow_data():
    '''
    This reads the zillow 2017 properties data from the Codeup db into a df.
    '''
    # Create SQL query.
    sql_query='''
        SELECT bathroomcnt AS bathrooms,
            bedroomcnt AS bedrooms,
            taxvaluedollarcnt AS home_value,
            calculatedfinishedsquarefeet AS square_feet,
            yearbuilt AS year_built,
            fips
        FROM properties_2017 
        JOIN predictions_2017 USING (parcelid)
        JOIN propertylandusetype USING (propertylandusetypeid)
        WHERE propertylandusedesc IN ('Single Family Residential' , 'Inferred Single Family Residential')
                AND YEAR(transactiondate) = 2017;
        '''

    # Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_db_url(db = 'zillow'))

    return df

def aquire_zillow_data(new = False):
    ''' 
    Checks to see if there is a local copy of the data, 
    if not or if new = True then go get data from Codeup database
    '''
    
    filename = 'zillow.csv'
    
    #if we don't have cached data or we want to get new data go get it from server
    if (os.path.isfile(filename) == False) or (new == True):
        df = new_zillow_data()
        #save as csv
        df.to_csv(filename,index=False)

    #else used cached data
    else:
        df = pd.read_csv(filename)
          
    return df

def house_size(df, col_list):
    '''
    Creates size columns and assigns True or False based on if
    the features in col_list are above or below the interquartile range
    '''
    df['large_home'] = False
    df['small_home'] = False
    for col in col_list:

        q1, q3 = df[col].quantile([0.25, 0.75]) # get quartiles

        iqr = q3 - q1   # calculate interquartile range

        upper_bound = q3 + 1.5 * iqr   # get upper bound
        lower_bound = q1 - 1.5 * iqr   # get lower bound

        df.loc[df[col] > upper_bound, 'large_home'] = True
        df.loc[df[col] < lower_bound, 'small_home'] = True
    return df

def clean_zillow(df):
    '''Takes in zillow data and returns a clean df'''
    
    #drop nulls
    df = df.dropna()

    #add a column to describe the size of the house
    #df = house_size(df, ['bedrooms','bathrooms','square_feet'])

    #add column that displays ratio of bedrooms to bathrooms:
    df['bath_bed_ratio'] = df.bathrooms / df.bedrooms

    #convert data types
    df["year_built"] = df["year_built"].astype(int)
    df["bedrooms"] = df["bedrooms"].astype(int)  
    df["bathrooms"] = df["bathrooms"].astype(int) 
    df["square_feet"] = df["square_feet"].astype(int)

    # Relabeling fips data
    df['county'] = df.fips.replace({6037:'LA', 6059:'Orange', 6111:'Ventura'})
    # Get dummies for fips
    dummy_df = pd.get_dummies(df[['county']], dummy_na=False, drop_first=[True, True])
    df = pd.concat([df, dummy_df], axis=1)

    #Creating new column for home age using year_built, casting as integer
    df["2017_age"] = 2017 - df.year_built
    df["2017_age"] = df["2017_age"].astype(int)

    return df