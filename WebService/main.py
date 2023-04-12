from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import pickle

app = Flask(__name__)

messages = [{'result': '',
             'description': ''}]

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/send", methods=["POST"])
def requesthandler():

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

    # loading model, label encoder, TfidfVectorizer
    le = pickle.load(open('label_enc.pkl', 'rb'))
    tfidf_enc = pickle.load(open('tfidf_enc.pkl', 'rb'))
    clf = pickle.load(open('model.pkl', 'rb'))

    # input data
    drink  = request.form['drink']
    volume = request.form['volume']
    calories = request.form['calories']
    caffeine = request.form['caffeine']
    caffeine_over_ml = caffeine/volume

    new_data = pd.DataFrame(data=np.array([[drink, volume, calories, caffeine, caffeine_over_ml]]),
                                columns=['drink', 'volume', 'calories', 'caffeine', 'caffeine_over_ml'])
    new_data = preprocessing(new_data, tfidf_enc)

    # prediction
    predicted = clf.predict(new_data)
    messages['result'] = le.inverse_transform(predicted)
    messages['description'] = f"You are drinking {le.inverse_transform(predicted)}, hope you are enjoing your brake!"
    return render_template("index.html", message=messages)

if __name__ == '__main__':
    app.run(host="0.0.0.0")





