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
        SELECT properties_2017.parcelid,
            bathroomcnt AS bathrooms,
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

def acquire_zillow_data(new = False):
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


def clean_zillow(df):
    '''Takes in zillow data and returns a clean df'''
    
    #drop duplicates
    df = df.drop_duplicates()

    #remove houses that have 0 bathrooms AND 0 bedrooms
    df = df[(df['bathrooms'] > 0 ) & (df['bedrooms'] > 0)]

    #drop houses that have 10,000 or more square feet
    df = df[df['square_feet'] <= 10000 ]

    #drop nulls
    df = df.dropna()

    #add column that displays ratio of bedrooms to bathrooms:
    df['bath_bed_ratio'] = df.bathrooms / df.bedrooms

    #convert data types
    df["year_built"] = df["year_built"].astype(int)
    df["bedrooms"] = df["bedrooms"].astype(int)   
    df["square_feet"] = df["square_feet"].astype(int)

    # Relabeling fips data
    df['county'] = df.fips.replace({6037:'LA', 6059:'Orange', 6111:'Ventura'})
    df = df.drop(columns='fips')

    #Creating new column for home age using year_built, casting as integer
    #df["2017_age"] = 2017 - df.year_built
    #df["2017_age"] = df["2017_age"].astype(int)

    return df

def scale_zillow(train, validate, test, scale_features=['bedrooms', 'bathrooms', 'square_feet', 'year_built']):
    '''
    Takes in train, validate, test and a list of features to scale
    and scales those features.
    Returns df with new columns with scaled data
    '''
    train_scaled = train.copy()
    validate_scaled = validate.copy()
    test_scaled = test.copy()
    
    minmax = pre.MinMaxScaler()
    minmax.fit(train[scale_features])
    
    train_scaled[scale_features] = pd.DataFrame(minmax.transform(train[scale_features]),
                                                  columns=train[scale_features].columns.values).set_index([train.index.values])
                                                  
    validate_scaled[scale_features] = pd.DataFrame(minmax.transform(validate[scale_features]),
                                               columns=validate[scale_features].columns.values).set_index([validate.index.values])
    
    test_scaled[scale_features] = pd.DataFrame(minmax.transform(test[scale_features]),
                                                 columns=test[scale_features].columns.values).set_index([test.index.values])
    
    return train_scaled, validate_scaled, test_scaled


def split_data(df, test_size=0.15):
    '''
    Takes in a data frame and the train size
    It returns train, validate , and test data frames
    with validate being 0.05 bigger than test and train has the rest of the data.
    '''
    train, test = train_test_split(df, test_size = test_size , random_state=27)
    train, validate = train_test_split(train, test_size = (test_size + 0.05)/(1-test_size), random_state=27)
    
    return train, validate, test


def prep_for_model(train, validate, test, target):
    '''
    Takes in train, validate, and test data frames
    then splits  for X (all variables but target variable) 
    and y (only target variable) for each data frame
    '''
    #create list of non-numeric variables to create dummies
    dummy_cols = list(train.select_dtypes(include=np.number).columns)
    #create list of numeric variables to drop for the model
    drop_columns = list(train.select_dtypes(exclude=np.number).columns) + [target]

    # Get dummies for fips
    dummy_df_train = pd.get_dummies(train[dummy_cols], dummy_na=False, drop_first=[True, True])
    X_train = pd.concat([train, dummy_df_train], axis=1)
    X_train = X_train.drop(columns=drop_columns)
    y_train = train[target]

    dummy_df_validate = pd.get_dummies(validate[dummy_cols], dummy_na=False, drop_first=[True, True])
    X_validate = pd.concat([validate, dummy_df_validate], axis=1)
    X_validate = X_validate.drop(columns=drop_columns)
    y_validate = validate[target]

    dummy_df_test = pd.get_dummies(test[dummy_cols], dummy_na=False, drop_first=[True, True])
    X_test = pd.concat([test, dummy_df_test], axis=1)
    X_test = X_test.drop(columns=drop_columns)
    y_test = test[target]

    return X_train, y_train, X_validate, y_validate, X_test, y_test


def big_zillow_wrangle(df, target):
    '''
    Takes in the target variable, if you want new data, and 
    if you want to remove outliers. 
    Returns a cleaned zillow dataframe and split dataframe ready for 
    exploration and modeling
    '''
    #clean data
    df = clean_zillow(df)
    #split data
    train, validate, test = split_data(df)
    #scale data
    train_scaled, validate_scaled, test_scaled = scale_zillow(train, validate, test)
    #prep for model
    X_train, y_train, X_validate, y_validate, X_test, y_test = prep_for_model(train_scaled, validate_scaled, test_scaled, target)
    #explore data
    train_exp = train.copy()
    
    return train_exp, X_train, y_train, X_validate, y_validate, X_test, y_test