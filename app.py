from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
import time
from datetime import timedelta
import datetime
import os
import pyrebase



app = Flask(__name__)  # "dunder name".

DEBUG = True
## Configureation for flask
app.config.from_object(__name__)
## external configuration stores in external file
app.config.from_pyfile("configuration/myconfig.cfg")
## update flask config to set the life time of session to 15, if no actions the session will be logout.
app.config.update(
    ## time out logged in session after minutes=15 time
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=45),
)
## Generate a random String as secret key wach time we run the app for more secuity.
app.secret_key = os.urandom(32)

def add_data_to_db(child,data):
    config = {
    "apiKey": "AIzaSyDQ_d3UjNFUippgQGodEX0jHu8Fy6jEDBA",
    "authDomain": "dalily-sy.firebaseapp.com",
    "databaseURL": "https://dalily-sy.firebaseio.com/",
    "storageBucket": "dalily-sy.appspot.com"
    }

    firebase = pyrebase.initialize_app(config)

    db = firebase.database()
    db.child("locations").child(child).push(data)

def get_all_data(link):
    if link is "all":
        r = requests.get("https://dalily-sy.firebaseio.com/locations.json")
    else:
        url = "https://dalily-sy.firebaseio.com/locations/%s.json" % (link)
        r = requests.get(url)
    x = r.json()
    return x

def create_the_table_all():
    r = requests.get("https://dalily-sy.firebaseio.com/locations.json")
    x = r.json()
    
    table = ""
    for k,v in x.items():
        for y,k in v.items():
            table += "<tr>"
            table += "<td>" + str(k["countesAdd"]) + "</td>"
            table += "<td>" + str(k["name"]) + "</td>"
            table += "<td>" + str(k["phone"]) + "</td>"
            table += "<td>" + str(k["busSector"]) + "</td>"
            table += "<td>" + str(k["googleUrl"]) + "</td>"
            table += "<td>" + str(k["syrianHire"]) + "</td>"
            table += "</tr>"
    return table


def create_the_table(county):
    url = "https://dalily-sy.firebaseio.com/locations/%s.json" % (county)
    r = requests.get(url)
    x = r.json()
    table = ""

    if x is None:
        return '''<script>
                alert("NO DATA FOR %s !");
                window.location.href = "/";
                </script>
                ''' %(county)
    for k,v in x.items():
        table += "<tr>"
        table += "<td>" + str(v["countesAdd"]) + "</td>"
        table += "<td>" + str(v["name"]) + "</td>"
        table += "<td>" + str(v["phone"]) + "</td>"
        table += "<td>" + str(v["busSector"]) + "</td>"
        table += "<td>" + str(v["googleUrl"]) + "</td>"
        table += "<td>" + str(v["syrianHire"]) + "</td>"
        table += "</tr>"
    return table

@app.route("/")
def route():
    return render_template("index.html" )

@app.route("/result", methods=['GET'])
def result():
    select = 1
    select = request.args.get('countySearch')
    print(select)
    if select == 'all':
        table = create_the_table_all()
    else:
        table= create_the_table(select)
    return render_template("results.html" , select=select , table=table)

@app.route("/addBusiness")
def add_business():
    return render_template("addBusiness.html" )

@app.route("/addProcess", methods=['POST'])
def add_business_process():
    name = request.form.get('name')
    address = request.form.get('address')
    countesAdd = request.form.get('countesAdd')
    phone = request.form.get('phone')
    email = request.form.get('email')
    busSector = request.form.get('busSector')
    googleUrl = request.form.get('googleUrl')
    busDesc = request.form.get('busDesc')
    select = request.form.get('syrianHire')

    data = {
    "name": request.form.get('name'),
    "address": request.form.get('address'),
    "countesAdd": request.form.get('countesAdd'),
    "phone": request.form.get('phone'),
    "email": request.form.get('email'),
    "busSector": request.form.get('busSector'),
    "googleUrl": request.form.get('googleUrl'),
    "busDesc": request.form.get('busDesc'),
    "syrianHire": request.form.get('syrianHire')
    }
    print(data)
    add_data_to_db(countesAdd,data)

    return render_template("index.html" )



@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html",)



# the application start
if __name__ == "__main__":
    app.run()
