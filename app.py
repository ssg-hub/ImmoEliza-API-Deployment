from preprocessing import cleaning_data
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

# A welcome message to test our server
# and define our requirements
@app.route('/', methods=['GET'])
def index():
    return "<h1>alive !!</h1>"

@app.route('/predict/', methods=['GET'])
def respond():
    # GET request returning a string to explain what the POST expects
    # Render the UI
    return render_template('reqd_input.html')

@app.route('/predict/', methods=['POST'])
def post_property_data():
    param = request.get_json()

    print("post param",param)

    if param:
        if 'data' in param:
            param = param['data']
            #cleaning_data    
        
            if not 'area' in param:
                return '''ERROR : No area found to predict the price,
                             please send property area.'''
            else:
                area = param['area']
                if not 'property-type' in param:
                    return '''<h2>ERROR : No type found to predict the price,
                             please send property type.<h2>'''
                else:
                    type = param['property-type']
                    if not 'number-of-rooms' in param:
                        return '''ERROR : Number of bedrooms not found to predict the price,
                             please send number of bedrooms in property.'''
                    else:
                        number_of_bedrooms = param['number-of-rooms']
                        if not 'zip-code' in param:
                            return '''<h2>ERROR : No zipcode found to predict the price,
                                please send property zipcode.<h2>'''
                        else:
                            zipcode = param['zip-code']
                            #cleaning_data.py

                            msg = "We will now predict the price using model."
                            return jsonify({
                                "Message" : msg,
                                "Prediction" : "price".format(345000)
                                })
                    
        else:
            return '''Please enter this data in the required format.'''

    else:
        return '''ERROR : No parameters found to predict the price,
             please send property parameters.'''
    
if __name__ == '__main__':
    app.run(port=5002, threaded = True)
