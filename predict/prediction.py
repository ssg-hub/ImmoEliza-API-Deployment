# from preprocessing import cleaning_data
from model import model_for_price
import pandas as pd

def opening_dict(dict_from_preprocess):
    y = dict_from_preprocess
    area = y["data"]["area"]
    

    return
    
def predict(data : dict) -> float:
    """
    Function to take data from make a prediction for price
    """

    #calling model_for_price() to get the regression model and an empy dataframe
    reg, df_copy = model_for_price

    '''# create a duplicate frame to populate user given data
    df_copy = pd.DataFrame().reindex(columns=df.columns)
    df_copy.loc[len(df_copy)] = 0'''

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
    row_for_prediction = df_copy.iloc[0]
    prediction = reg.predict(row_for_prediction.reshape(1,1))
    print('prediction', prediction[0,0]) 

    return