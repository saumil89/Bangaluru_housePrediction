from flask import Flask, jsonify, render_template, request
import json
import util

app = Flask(__name__)

@app.route('/boot')
def first():
    return render_template('boot.html')

@app.route('/', methods=["GET","POST"]) 
def index():
    __loc = {'locations':[]}
    for i in util.get_locations():
        __loc['locations'].append(i.title())
    if request.method == "GET":
        statment = ""
    else:
        location = request.form["locations"]
        sqft = request.form["area"]
        bhk = request.form["bed"]
        bath = request.form["bath"]
        try:
            price = util.get_estimated_price(location=location, sqft=sqft, bhk=bhk, bath=bath)
            statment = f"Predicted Price for {location} with area {sqft} sq. ft., {bhk} bed(s) and {bath} bath(s) is {price} INR"
        except:
            statment = "Enter Valid Data"
        

    return render_template('index.html', data=__loc, price=statment) 
        

if __name__ == '__main__':
    app.run(debug=True)