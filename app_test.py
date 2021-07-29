from flask import Flask, request, jsonify
import os
app = Flask(__name__)

@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    #print(f"got name {name}")
    print("name :", name)

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = "Welcome to our awesome platform!! "+name

    # Return the response in json format
    return jsonify(response)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.get_json()
    print("post param",param)
    # You can add the test cases you made in the previous function,
    # but in our case here you are just testing the POST functionality
    if param:
        if 'name' in param:
         name = param['name']
         return 'The name is : {}'.format(name)
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # You want to put the value of the env variable PORT if it exist (some services only open specifiques ports)
    port = int(os.environ.get('PORT', 5002))
    # Threaded option to enable multiple instances for
    # multiple user access support
    # You will also define the host to "0.0.0.0" because localhost will only be reachable from inside de server.
    app.run(host="0.0.0.0", port=port, threaded = True)           