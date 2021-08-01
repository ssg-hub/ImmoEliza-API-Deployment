import os
from flask import Flask, request, jsonify, render_template
from preprocessing.cleaning_data import preprocess
from predict.prediction import price_prediction
from model.model_for_price import load_data, model_for_data

# creating flask app
app = Flask(__name__)

# a welcome message to test our server
@app.route('/', methods=['GET'])
def index():
    return "<h1>alive !!</h1>"


# a GET request to give information about the application
@app.route('/predict/', methods=['GET'])
def respond() -> str:
    # GET request returning a string to explain what the POST expects
    # Render the UI
    return render_template('reqd_input.html')


# a POST request that takes property data in json,
# does processing and returns the predicted price.
@app.route('/predict/', methods=['POST'])
def post_property_data():
    param = request.get_json()

    print("post param",param)

    if param:
        if 'data' in param:
            param = param['data']
            
            if (not 'zip-code' in param) or (not 'area' in param) or (
                not 'property-type' in param) or (not 'number-of-rooms' in param
                ) or (not "kitchen-equipped" in param) or (not "furnished" in param
                ) or (not "fireplace" in param) or (not "terrace" in param
                ) or (not "garden" in param) or (not "swimming-pool" in param
                ) or (not "building-condition" in param) :

                print("missing property parameter")
                return jsonify({
                    "Error" : "Parameters missing to predict the price, please send all property parameters."
                    })

            elif (
                 param['property-type'].upper() not in ["HOUSE","APARTMENT"] 
                ) or (
                 param['zip-code'] < 1000 or param['zip-code'] > 9999
                ) or (
                 param['number-of-rooms'] < 0 or param['number-of-rooms'] > 50
                ) or (
                 param['building-condition'].upper() not in 
                     ["GOOD","NOT SO GOOD","UNKNOWN"] 
                ) or (
                      (param['kitchen-equipped'].upper() or param['furnished'].upper() or 
                       param['fireplace'].upper() or param['terrace'].upper() or
                       param['garden'].upper() or param['swimming-pool'].upper())
                       not in ["YES","NO"]
                ) :
                
                print('parameter input not as per requirements')
                return jsonify({
                    "Error" : "Please refer the the table for acceptable parameter inputs."
                    })

            else:
                # call function to return a data frame copy from the model
                # the regression prediction model is generated
                df_copy = load_data()
                model = model_for_data('finalized_model.pkl')
                print(' model ok')

                # call function to user input data is processed 
                # as per model data requirements
                df = preprocess(df_copy, param)  
                print('preprocess ok')

                # call function to given the final price predicted
                predicted_price = price_prediction(df, model)
                print('price ok')
                return jsonify({
                    "Prediction" : predicted_price
                    })
                    
        else:
            print('input format issue')
            return jsonify({
                    "Error" : "Please enter this data in the required format.",
                    })
                    

    else:
        print('no input provided')
        return jsonify({
                    "Error" : "No parameters found to predict, the price,please send property parameters.",
                    })
        
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5002))
    app.run(host = "0.0.0.0", port = port, threaded = True)
