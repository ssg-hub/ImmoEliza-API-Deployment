from flask import Flask
from flask import make_response, jsonify, request
app = Flask(__name__)


'''
@app.route('/')
def home():
   return 'Enter a number'
'''
@app.route('/<number>')
#route to double a number
def user(number):
    fl = float(number)
    return f"Double is {fl*2}!"



income = {
    "salary": 2500,
    "bonus": 200,
    "taxes": 400
}

@app.route("/income")
#route for GET request
def get_stock():
    res = make_response(jsonify(income), 200)
    return res

@app.route("/log-in", methods=["GET", "POST"])
def log_in():

    if request.method == "POST":
        # Only if the request method is POST
        # attempt the login & do something else

    # Otherwise default to this
    return render_template("log_in.html")


if __name__ == '__main__':
   app.run(port=5001)