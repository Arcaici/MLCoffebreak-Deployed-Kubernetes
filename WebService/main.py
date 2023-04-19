import os
import socket

from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import pickle
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

app = Flask(__name__)

def isOpen(ip, port):
   test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      test.connect((ip, int(port)))
      test.shutdown(1)
      return True
   except:
      return False

def fakeLoadBalancer():
    ips = []
    ip = "cassandra"
    port = 9042
    if isOpen(ip, port):
        ips.append(ip)
    return ips

#connection variables
cluster = Cluster(fakeLoadBalancer(), port=9042,
                  auth_provider=PlainTextAuthProvider(username='cassandra', password='cassandra'))
session = cluster.connect('caffeine', wait_for_all_pools=False)

def make_lowercase(drink):
    return drink.str.lower()


def remove_special_chars(drink):
    # remove certain special characters from ingredients
    drink = drink.replace("'", " ")
    drink = drink.replace("''", " ")
    drink = drink.replace("%", " ")
    drink = drink.replace("!", " ")
    drink = drink.replace("(", " ")
    drink = drink.replace(")", " ")
    drink = drink.replace("/", " ")
    drink = drink.replace(",", " ")
    drink = drink.replace(".", " ")

    return drink


def clean_drink(drink):
    drink = make_lowercase(drink)
    drink = remove_special_chars(drink)
    return drink


def preprocessing(new_data, tfidf_enc):
    new_data.drink = clean_drink(new_data.drink)
    drinks_word_features = tfidf_enc.transform(new_data.drink)
    drinks_word_features = pd.DataFrame(drinks_word_features.toarray().transpose(),
                                        index=tfidf_enc.get_feature_names())
    new_data.drop(columns="drink", axis=1, inplace=True)
    new_data = pd.concat([new_data, drinks_word_features.transpose()], axis=1)
    return new_data


def data_used_for_db_ingestion(new_data):
    min_tfidf_feature_value = 0.0
    new_data = new_data.loc[:, ~(new_data == 0.0).all()]
    return new_data

def data_ingestion(newdata, drink):
    session.execute('USE caffeine')
    newdata = dict(newdata[0])
    tmp=""
    insert_query = "INSERT INTO caffeine.new_caffeine(drink_name, "
    for key in newdata.keys():
        insert_query = insert_query + str(key).replace(" ","_") + ', '
        tmp = str(key).replace(" ","_")

    insert_query = insert_query.replace(f"{tmp},", f"{tmp}")
    insert_query = insert_query + ") VALUES ('" + drink +"', "

    for el in newdata.values():
        insert_query = insert_query + str(el) + ', '
        tmp = str(el)
    insert_query = insert_query.replace(f"{tmp},", f"{tmp}")
    insert_query = insert_query + ");"

    session.execute(insert_query)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def requesthandler():

    # loading model, label encoder, TfidfVectorizer
    le = pickle.load(open('pretrained_model/label_enc.pkl', 'rb'))
    tfidf_enc = pickle.load(open('pretrained_model/tfidf_enc.pkl', 'rb'))
    clf = pickle.load(open('pretrained_model/model.pkl', 'rb'))

    # input data
    drink  = str(request.form['drink'])
    volume = float(request.form['volume'])
    calories = int(request.form['calories'])
    caffeine_ml = int(request.form['caffeine'])
    caffeine_over_ml = float(caffeine_ml)/float(volume)

    new_data = pd.DataFrame(data=np.array([[drink, volume, calories, caffeine_ml, caffeine_over_ml]]),
                                columns=['drink', 'volume', 'calories', 'caffeine_ml', 'caffeine_over_ml'])
    new_data = preprocessing(new_data, tfidf_enc)

    #template data
    messages = {'result': '',
                'description': ''}

    # prediction
    predicted = clf.predict(new_data)
    predicted_proba = clf.predict_proba(new_data)

    tmp = str(le.inverse_transform(predicted))
    tmp = tmp.replace("']", "")
    tmp = tmp.replace("['", "")

    #db new_data ingestion acquisition
    new_data = data_used_for_db_ingestion(new_data)
    dict_ingestion = new_data.to_dict('r')
    data_ingestion(dict_ingestion, drink)

    #loading template
    messages['result'] =  tmp
    messages['description'] = f"You are drinking {tmp}, hope you are enjoing your brake!"

    return render_template("index.html", **messages)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
    




