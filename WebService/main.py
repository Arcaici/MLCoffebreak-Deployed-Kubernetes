from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import pickle

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
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

    def data_used_for_db_ingestion(new_data):
        min_tfidf_feature_value = 0.0
        new_data = new_data.loc[:, ~(new_data == 0.0).all()]
        print(new_data)
        return new_data

    # loading model, label encoder, TfidfVectorizer
    le = pickle.load(open('pretrained_model/label_enc.pkl', 'rb'))
    tfidf_enc = pickle.load(open('pretrained_model/tfidf_enc.pkl', 'rb'))
    clf = pickle.load(open('pretrained_model/model.pkl', 'rb'))

    # input data
    drink  = str(request.form['drink'])
    volume = float(request.form['volume'])
    calories = int(request.form['calories'])
    caffeine = int(request.form['caffeine'])
    caffeine_over_ml = float(caffeine)/float(volume)

    new_data = pd.DataFrame(data=np.array([[drink, volume, calories, caffeine, caffeine_over_ml]]),
                                columns=['drink', 'volume', 'calories', 'caffeine', 'caffeine_over_ml'])
    new_data = preprocessing(new_data, tfidf_enc)

    #template data
    messages = {'result': '',
                'description': ''}

    # prediction
    predicted = clf.predict(new_data)
    predicted_proba = clf.predict_proba(new_data)
    print(predicted_proba)

    tmp = str(le.inverse_transform(predicted))
    tmp = tmp.replace("']", "")
    tmp = tmp.replace("['", "")

    #db new_data ingestion acquisition
    new_data = data_used_for_db_ingestion(new_data)
    dict_ingestion = {'label': predicted, 'data': new_data, 'result_proba': predicted_proba}
    print(dict_ingestion)

    #loading template
    messages['result'] =  tmp
    messages['description'] = f"You are drinking {tmp}, hope you are enjoing your brake!"

    return render_template("index.html", **messages)

if __name__ == '__main__':
    app.run(host="0.0.0.0")





