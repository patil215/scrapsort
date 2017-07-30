from flask import redirect, render_template, render_template_string, Blueprint
from flask import request, url_for, flash, Response, jsonify
import time
from app.utils import tag
from app.init_app import app
import random
import pyrebase

@app.route("/")
def home_page():
    config = {
      "apiKey": "apiKey",
      "authDomain": "projectId.firebaseapp.com",
      "databaseURL": "https://smart-garbage-4ba99.firebaseio.com/",
      "storageBucket": "projectId.appspot.com"
    }

    firebase = pyrebase.initialize_app(config)

    db = firebase.database()
    values = db.child("recyclingData").get().val()

    items = []
    for value in list(values.keys()):
        if str(values[value]["version"]) == "0.2":
            items.append(values[value])

    numTrash = 0
    for item in items:
        if item["isTrash"] == True:
            numTrash += 1

    numRecycle = len(items) - numTrash

    numItems = len(items)

    percentages = {}
    # Assign percentages to each item
    for item in items:
        if 'recyclingLabel' in item and item['recyclingLabel'] != None:
            if item['recyclingLabel'] in percentages:
                percentages[item['recyclingLabel']] += 1
            else:
                percentages[item['recyclingLabel']] = 1

    for label in percentages.keys():
        percentages[label] = float(percentages[label]) / numRecycle

    data = {'numItems': numItems, 'numTrash' : numTrash, 'numRecycle' : numRecycle, 'percentages' : percentages}

    return render_template('pages/home_page.html', data=data)