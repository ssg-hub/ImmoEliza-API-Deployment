from numpy.lib.function_base import append
import pandas as pd
import numpy as np
from scipy.stats import zscore
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


def inital_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    function for initial cleaning tasks like
    removing columns, duplicates.
    """
    # remove columns not needed for analysis
    df = df.drop(
            columns = [
                "terrace_area",
                "garden_area",
                "land_surface",
                "subtype", 
                "facade_count"
                
            ]
        )
        
    # remove rows with missing area or price values
    df = df.dropna( subset = ["price","area"])
    
    # fill null 'building_condition' values with the most common or desired value
    df = df.fillna({'building_condition': "UNKNOWN"})
      
    # remove duplicates that are the same in below features
    cleaned_df = df.drop_duplicates(subset = [
                            "zipcode", 
                            "price",
                            "area",
                            "number_of_rooms"
            ], keep='first'
        )

    return cleaned_df

def outlier_removal(df : pd.DataFrame) -> pd.DataFrame:
    """
    function to remove outliers that have a value
    more than 3 standard devations from the mean
    source : https://www.kite.com/python/answers/how-to-remove-outliers-from-a-pandas-dataframe-in-python
    """
    col_for_oultier_removal = ['area', 'price','number_of_rooms']
    
    for each in col_for_oultier_removal:
        z_scores = zscore(df[each])

        abs_z_scores = np.abs(z_scores)
    
        # create a boolean array for std dev less than 3
        filtered_entries = (abs_z_scores < 3)

        # filter for dataframe without outliers
        df = df[filtered_entries]
                
    return df

def handle_categorical_features(df : pd.DataFrame) -> pd.DataFrame:
    """
    function to encode categorical variables
    source : https://pbpython.com/categorical-encoding.html
    """

    # creating a column list for subset dataframe for categorical variables
    col_list = list(df.select_dtypes(include=['object']))
        
    # using One Hot encoding 
    
    col_list.append('zipcode')

    encoded_df = pd.get_dummies(df, columns= col_list)
    
    # This will select float columns only
    float_col = encoded_df.select_dtypes(include=['float64']) 

    #convert columns to float
    for col in float_col.columns.values:
        encoded_df[col] = encoded_df[col].astype('int64')
          
    return encoded_df


def model_for_data() -> RandomForestRegressor:
    """
    Function to create a prediction model step by step.
    Returns the model to predict price for given parameters.
    source : https://towardsdatascience.com/create-a-model-to-predict-house-prices-using-python-d34fe8fad88f
    """

    # read the csv file for data
    df = pd.read_csv("/home/becode/property_listing_analysis/houses.csv")
    
    #rearrange the col list acc to input that will be received
    clist = ['zipcode','area','type','number_of_rooms','price','subtype','kitchen_equipped',
             'furnished','fireplace','terrace','terrace_area','garden','garden_area',
             'land_surface','facade_count','swimming_pool','building_condition']

    df = df[clist]
    
    # preprocess the df
    df = inital_cleaning(df)
        
    df = outlier_removal(df)
    
    df = handle_categorical_features(df)  
        
    # preparing target variable
    y = df['price'].to_numpy().reshape(-1,1)

    #preparing features data
    feature_df = df.drop(columns=["price"])
    X = feature_df
    
    # split the data into test and train
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=13, test_size=0.2 )

    # define the regressor 
    reg = RandomForestRegressor(n_estimators = 50,random_state=0).fit(X_train, y_train)
    
    # predicting for random row from test data
    prediction = reg.predict(X_test.sample()).reshape(1,1)
    print('prediction', prediction[0,0]) 

    # prediction score
    score = round(reg.score(X_test,y_test),3)
    print('score',score)
    
    # create a duplicate frame to populate user given data
    df_copy = pd.DataFrame().reindex(columns=df.columns)
    df_copy.loc[len(df_copy)] = 0
    
    # data for one row
    data = {
        "zipcode": 1000,
        "area": 45,
        "type": "APARTMENT",
        "number_of_rooms": 3
        }
    zip = data['zipcode']
    zip_name = "zipcode_"+str(zip)
    
    pr_type_name = data['type']
    type_name = "type_" + pr_type_name
    
    df_copy.at[0,'area'] = data['area']
    df_copy.at[0,'number_of_rooms'] = data['number_of_rooms']
    df_copy.at[0,zip_name]= 1
    df_copy.at[0,type_name] = 1
    
    df_copy.drop(columns=["price"])
        
    # This will select float columns only
    float_col = df_copy.select_dtypes(include=['float64']) 

    for col in float_col.columns.values:
        df_copy[col] = df_copy[col].astype('int64')
        
    print(df_copy.head)
    
    pred_df = pd.DataFrame.from_dict(data.items())
    print(pred_df)
    
    # make a single prediction
    row_for_prediction = df.iloc[0]
    prediction = reg.predict(row_for_prediction.reshape(1,1))
    print('prediction', prediction[0,0]) 
    
    return reg, df_copy


model_for_data()

