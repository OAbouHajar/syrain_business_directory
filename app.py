from operator import truediv
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

def get_all_data():
    r = requests.get("https://dalily-sy.firebaseio.com/locations.json")
    x = r.json()
    return x

def create_the_table_all():
    r = requests.get("https://dalily-sy.firebaseio.com/locations.json")
    data = r.json()
    
    table = ""
    for k,v in data.items():
        for y,k in v.items():
            if k['active'] is True:
                table += "<button name='resultRow' class='filterDiv collapsible "+ str(k["busSector"]) +"'>" + str(k["name"]) + "<br>" + "<span class='busdesc'>" + str(k["busDesc"][0:75]+'...') +"</span>" + "</button>"
                table += "<div class='content'>"
                table += '''<table>
                            <thead>
                            <tr>
                                <th>County</th>
                                <th>Name</th> 
                                <th>Phone</th> 
                                <th>Sector</th> 
                                <th>Maps</th> 
                                <th>Syrian Hire</th> 
                                <th>Description</th> 
                            </tr>
                            </thead>
                            <tbody>
                        '''
                table += "<tr>"
                table += "<td>" + str(k["countesAdd"]) + "</td>"
                table += "<td>" + str(k["name"]) + "</td>"
                table += "<td>" + str(k["phone"]) + "</td>"
                table += "<td>" + str(k["busSector"]) + "</td>"
                table += "<td><a class='aTable' href='{link}'>{link}</a>".format(link=str(k["googleUrl"]))+"</td>"
                table += "<td>" + str(k["syrianHire"]) + "</td>"
                table += "<td>" + str(k["busDesc"]) + "</td>"
                table += "</tr>"
                table += '''</tbody>
                            </table>'''
                table += "</div>"
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
    for y,k in x.items():
        if k['active'] is True:
            table += "<button name='resultRow' class='filterDiv collapsible "+ str(k["busSector"]) +"'>" + str(k["name"]) + "<br>" + "<span class='busdesc'>" + str(k["busDesc"][0:75]+'...') +"</span>" + "</button>"
            table += "<div class='content'>"
            table += '''<table>
                    <thead>
                        <tr>
                            <th>County</th>
                            <th>Name</th> 
                            <th>Phone</th> 
                            <th>Sector</th> 
                            <th>Maps</th> 
                            <th>Syrian Hire</th> 
                            <th>Description</th> 
                        </tr>
                        </thead>
                        <tbody>
                    '''
            table += "<tr>"
            table += "<td>" + str(k["countesAdd"]) + "</td>"
            table += "<td>" + str(k["name"]) + "</td>"
            table += "<td>" + str(k["phone"]) + "</td>"
            table += "<td>" + str(k["busSector"]) + "</td>"
            table += "<td><a class='aTable' href='{link}'>{link}</a>".format(link=str(k["googleUrl"]))+"</td>"
            # table += "<td><a herf='" + str(k["googleUrl"]) + "'>"+ str(k["googleUrl"])+"</a></td>"
            table += "<td>" + str(k["syrianHire"]) + "</td>"
            table += "<td>" + str(k["busDesc"]) + "</td>"
            table += "</tr>"
            table += '''</tbody>
                        </table>'''
            table += "</div>"
    return table

def get_icon_path(cat):
    paths = {
      "all":"/static/filter/all.png",
      "Car Maintenance":"/static/filter/mechanic.png",
      "Accountant":"/static/filter/accounts.png",
      "House":"/static/filter/wholesale.png",
      "Shopping":"/static/filter/grocy.png",
      "Restaurants":"/static/filter/retails.png",
      "Transportation":"/static/filter/van.png",
      "Handy":"/static/filter/handy.png",
      "Translation": "/static/filter/translate.png",
      "County": "/static/contant/border.png",
      "Phone": "/static/contant/phone.png",
      "Link": "/static/contant/link.png",
      "Hire": "/static/contant/hire.png",
      "Description": "/static/contant/description.png",
      "Sectore":"/static/contant/sectore.png",
    }

    return paths[cat]

def create_the_table_card(county):
    url = "https://dalily-sy.firebaseio.com/locations/%s.json" % (county)
    r = requests.get(url)
    x = r.json()

    table = ""
    table += "<div class='busAll'>"

    if x is None:
        return '''<script>
                alert("NO DATA FOR %s !");
                window.location.href = "/";
                </script>
                ''' %(county)
    for y,k in x.items():
            yshortM = y[1:10]+"model"
            yshortB = y[1:10]+"btn"
            yshortC = y[1:10]+"close"
            if k['active'] is True:
                table += '''
                <div  name='resultRow' class='busCard filterDiv ''' +  str(k["busSector"]) + "'" +'''>
                <span class="category"><img src=''' + get_icon_path(str(k["busSector"])) + ''' > </span>
                <span class="busName">''' + str(k["name"]) + '''</span>
                <span class="busTitle">''' + str(k["busDesc"][0:35]) + '''</span>
                <div class="busButton">
                    <button id="'''+ yshortB +'''" class="buttonBus" onclick="cardDetails(''' + "'"+ yshortM + "'"+ "," + "'"+ yshortB +"'"+ "," + "'" + yshortC + "'"+ ''')">More info</button>
                </div>
                </div>
                
                <div id="'''+ yshortM +'''" class="modal">
                    <div class="result">
                        <span class='close' id="''' + yshortC +'''">&times;</span>
                        <span class="searchResultsInfo"> The Search results For : </span>
                        <span id="resultsLableInfo" class=" resultsLableInfo ">   &nbsp;&nbsp;''' + str(k["name"]) + '''  </span>
                        <br>
                        <hr>
                            <label> <img class="resultInfoImg" src=''' + get_icon_path("County") + ''' >  County:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>
                            <span class="modelData  resultsLable ">''' +  str(k["countesAdd"]) + '''</span>
                            <hr>
                            <label> <img class="resultInfoImg" src=''' + get_icon_path("Phone") + ''' > Phone:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>
                            <span class="modelData  resultsLable "><a class='aTable' href="tel:{phone}">{phone}</a>'''.format(phone=str(k["phone"]))+'''</span>
                            <hr>
                            <label><img class="resultInfoImg" src=''' + get_icon_path("Sectore") + ''' > Sectore:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>
                            <span class="modelData  resultsLable ">''' + str(k["busSector"]) + '''</span>
                            <hr>
                            <label><img class="resultInfoImg" src=''' + get_icon_path("Link") + ''' > Link:&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>
                            <span class="modelData  resultsLable "> <a class='aTable' href='{link}' target="_blank">Click Here</a>'''.format(link=str(k["googleUrl"]))+'''</span>
                            <hr>
                            <label><img class="resultInfoImg" src=''' + get_icon_path("Hire") + ''' > Hire:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>
                            <span class="modelData  resultsLable ">''' + str(k["syrianHire"]) + '''</span>
                            <hr>
                            <label><img class="resultInfoImg" src=''' + get_icon_path("Description") + ''' > Description:</label>
                            <span class="modelData  resultsLable ">''' + str(k["busDesc"]) + '''</span>
                    </div>
                </div>
                '''
    table += "</div>"
    return table


def create_the_table_all_card(notManager = True):
    r = requests.get("https://dalily-sy.firebaseio.com/locations.json")
    data = r.json()
    
    table = ""
    table += "<div class='busAll'>"
    for k,v in data.items():
        for y,k in v.items():
            yshortM = y[1:10]+"model"
            yshortB = y[1:10]+"btn"
            yshortC = y[1:10]+"close"
            if k['active'] is notManager:
                table += '''
                <div  name='resultRow' class='busCard filterDiv ''' +  str(k["busSector"]) + "'" +'''>
                <span class="category"><img src=''' + get_icon_path(str(k["busSector"])) + ''' > </span>
                <span class="busName">''' + str(k["name"]) + '''</span>
                <span class="busTitle">''' + str(k["busDesc"][0:35]) + '''</span>
                <div class="busButton">
                    <button id="'''+ yshortB +'''" class="buttonBus" onclick="cardDetails(''' + "'"+ yshortM + "'"+ "," + "'"+ yshortB +"'"+ "," + "'" + yshortC + "'"+ ''')">More info</button>
                </div>
                </div>
                
                <div id="'''+ yshortM +'''" class="modal">
                    <div class="result">
                        <span class='close' id="''' + yshortC +'''">&times;</span>
                        <span class="searchResultsInfo"> The Search results For : </span>
                        <span id="resultsLableInfo" class=" resultsLableInfo ">   &nbsp;&nbsp;''' + str(k["name"]) + '''  </span>
                        <br>
                        <hr>
                            <label> <img class="resultInfoImg" src=''' + get_icon_path("County") + ''' >  County:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>
                            <span class="modelData  resultsLable ">''' +  str(k["countesAdd"]) + '''</span>
                            <hr>
                            <label> <img class="resultInfoImg" src=''' + get_icon_path("Phone") + ''' > Phone:&nbsp;&nbsp;&nbsp;&nbsp;</label>
                            <span class="modelData  resultsLable ">''' + str(k["phone"]) + '''</span>
                            <hr>
                            <label><img class="resultInfoImg" src=''' + get_icon_path("Sectore") + ''' > Sectore:&nbsp;&nbsp;&nbsp;&nbsp;</label>
                            <span class="modelData  resultsLable ">''' + str(k["busSector"]) + '''</span>
                            <hr>
                            <label><img class="resultInfoImg" src=''' + get_icon_path("Link") + ''' > Link:&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>
                            <span class="modelData  resultsLable "> <a class='aTable' href='{link}'>{link}</a>"'''.format(link=str(k["googleUrl"]))+'''</span>
                            <hr>
                            <label><img class="resultInfoImg" src=''' + get_icon_path("Hire") + ''' > Hire:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>
                            <span class="modelData  resultsLable ">''' + str(k["syrianHire"]) + '''</span>
                            <hr>
                            <label><img class="resultInfoImg" src=''' + get_icon_path("Description") + ''' > Description:</label>
                            <span class="modelData  resultsLable ">''' + str(k["busDesc"]) + '''"</span>
                    </div>
                </div>
                '''
    table += "</div>"
    return table




@app.route("/")
def route():
    return render_template("index.html" )

@app.route("/result2", methods=['GET'])
def result():
    select = 1
    select = request.args.get('countySearch')
    print(select)
    if select == 'all':
        table = create_the_table_all_card()
    else:
        table= create_the_table_card(select)
    return render_template("result2.html" , select=select , table=table)

@app.route("/manager")
def add_business_after():
    table = create_the_table_all_card(False)
    return render_template("result2Manager.html", select="NOT ACTIVE" , table=table)

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
    agree = request.form.get('agree')

    data = {
    "name": request.form.get('name'),
    "address": request.form.get('address'),
    "countesAdd": request.form.get('countesAdd'),
    "phone": request.form.get('phone'),
    "email": request.form.get('email'),
    "busSector": request.form.get('busSector'),
    "googleUrl": request.form.get('googleUrl'),
    "busDesc": request.form.get('busDesc'),
    "syrianHire": request.form.get('syrianHire'),
    "agree" : request.form.get('agree'),
    "active": False
    }
    print(data)
    add_data_to_db(countesAdd,data)
    
    return render_template("addBusinessAfter.html" )



@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html",)


@app.route("/result2")
def result1():


    data = get_all_data()
    table = ""
    for k,v in data.items():
        for y,k in v.items():
            table += "<button class='collapsible'>" + str(k["name"]) + "</button>"
            table += "<div class='content'>"
            table += '''<table>
	<thead>
	<tr>
        <th>County</th>
        <th>Name</th> 
        <th>Phone</th> 
        <th>Sector</th> 
        <th>Maps</th> 
        <th>Syrian Hire</th> 
	</tr>
	</thead>
	<tbody>
'''
            table += "<tr>"
            table += "<td>" + str(k["countesAdd"]) + "</td>"
            table += "<td>" + str(k["name"]) + "</td>"
            table += "<td>" + str(k["phone"]) + "</td>"
            table += "<td>" + str(k["busSector"]) + "</td>"
            table += "<td>" + str(k["googleUrl"]) + "</td>"
            table += "<td>" + str(k["syrianHire"]) + "</td>"
            table += "</tr>"
            table += '''</tbody>
                        </table>'''
            table += "</div>"

    return render_template("result2.html",table=table)


# the application start
if __name__ == "__main__":
    app.run()
