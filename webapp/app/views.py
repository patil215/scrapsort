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
        items.append(values[value])

    numTrash = 0
    for item in items:
        if item["isTrash"] == True:
            numTrash += 1

    numRecycle = len(items) - numTrash

    numItems = len(items)

    data = {'numItems': numItems, 'numTrash' : numTrash, 'numRecycle' : numRecycle}

    return render('pages/home_page.html', data=data)