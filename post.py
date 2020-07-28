# import pyrebase


# print("hi")

# config = {
#   "apiKey": "AIzaSyDQ_d3UjNFUippgQGodEX0jHu8Fy6jEDBA",
#   "authDomain": "dalily-sy.firebaseapp.com",
#   "databaseURL": "https://dalily-sy.firebaseio.com/",
#   "storageBucket": "dalily-sy.appspot.com"
# }

# firebase = pyrebase.initialize_app(config)
# data = {
#     "name": "Mortimer 'Morty' Smith"
# }
# db = firebase.database()
# data = {"name": "Mortimer 'Morty' Smith"}
# db.child("users").push(data)
 


import requests

r = requests.get('https://dalily-sy.firebaseio.com/locations.json')
print(r.json())