from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
import time
from datetime import timedelta
import datetime
import os



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



@app.route("/")
def route():
    return render_template("index.html" )

@app.route("/result")
def result():
    return render_template("results.html" )

@app.route("/addBusiness")
def add_business():
    return render_template("addBusiness.html" )
@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html",)



# the application start
if __name__ == "__main__":
    app.run()
