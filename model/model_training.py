import csv

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import pickle

def make_lowercase(drinks):
    return drinks.str.lower()

def remove_special_chars(drinks):
    # remove certain special characters from ingredients
    drinks = [y.replace("'", " ")  for y in drinks]
    drinks = [y.replace("''", " ") for y in drinks]
    drinks = [y.replace("%", " ")  for y in drinks]
    drinks = [y.replace("!", " ")  for y in drinks]
    drinks = [y.replace("(", " ")  for y in drinks]
    drinks = [y.replace(")", " ")  for y in drinks]
    drinks = [y.replace("/", " ")  for y in drinks]
    drinks = [y.replace(",", " ")  for y in drinks]
    drinks = [y.replace(".", " ")  for y in drinks]

    return drinks

def clean_drink(drinks):
    drinks = make_lowercase(drinks)
    drinks = remove_special_chars(drinks)
    return drinks

#read data
df = pd.read_csv("clean_caffeine.csv")

#splitting labels and features
label = df["type"]
df.drop(columns='type' , axis=1,inplace=True)

#Adding words features using TFIDF (see feature_exctraction.py)
df.drink = clean_drink(df.drink)
tfid_enc = TfidfVectorizer(min_df=5, max_df=150, ngram_range=(1,3))
drinks_word_features = tfid_enc.fit_transform(df.drink)

#converting feature vector to dataframe
drinks_word_features = pd.DataFrame(drinks_word_features.toarray().transpose(),
                   index=tfid_enc.get_feature_names())
#dropping drink names from df
df.drop(columns = "drink" ,axis=1, inplace=True)

#resultant dataframe
df = pd.concat([df, drinks_word_features.transpose()], axis=1)

#label encoder
le = LabelEncoder()
le.fit(label)
label = le.transform(label)

#Training Model
clf = LogisticRegression(C=0.9, max_iter=100,  multi_class="auto", penalty='l2', solver='liblinear')
clf.fit(df, label)

#Saving Model
pickle.dump(clf, open('model.pkl', 'wb'))
pickle.dump(le, open('label_enc.pkl', 'wb'))
pickle.dump(tfid_enc, open('tfidf_enc.pkl','wb'))

#Saving TfIdf features name
tfid_features = tfid_enc.get_feature_names()
print(tfid_features)
with open('../cassandra_auto_columns/tfidf_feature_list.csv', 'w') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(tfid_features)