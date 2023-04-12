import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import pickle

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

#loading model, label encoder, TfidfVectorizer
le = pickle.load(open('label_enc.pkl', 'rb'))
tfidf_enc = pickle.load(open('tfidf_enc.pkl', 'rb'))
clf = pickle.load(open('model.pkl', 'rb'))

#input data
new_data = pd.DataFrame(data= np.array([["Celsius Energy Drink", 354.882, 10, 200, 0.563568]]), columns=['drink', 'volume', 'calories', 'caffeine', 'caffeine_over_ml'])
print(new_data)

#preprocessing
new_data.drink = clean_drink(new_data.drink)
drinks_word_features=tfidf_enc.transform(new_data.drink)
drinks_word_features = pd.DataFrame(drinks_word_features.toarray().transpose(),
                   index=tfidf_enc.get_feature_names())
new_data.drop(columns = "drink" ,axis=1, inplace=True)
new_data = pd.concat([new_data, drinks_word_features.transpose()], axis=1)

#prediction
predicted = clf.predict(new_data)
print(le.inverse_transform(predicted))

# drink               Celsius Energy Drink
# volume                           354.882
# calories                              10
# caffeine                             200
# type                       Energy Drinks
# caffeine_over_ml                0.563568
