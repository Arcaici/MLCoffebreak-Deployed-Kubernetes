import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn import preprocessing

def remove_special_chars(text):
    # remove certain special characters from ingredients
    text = text.replace("&", " ")
    text = text.replace("%", " ")
    text = text.replace("(", " ")
    text = text.replace(")", " ")
    text = text.replace("/", " ")
    text = text.replace(",", " ")
    text = text.replace(",", " ")
    return text



pd.set_option("display.max_columns", None)

#reading data
df = pd.read_csv("clean_caffeine.csv")

drink_type = df["type"].unique()
drink_counts = df["type"].value_counts()

#plotting caffeine drinks type over  volume and caffeine level ratio

caffeine_measures = df[["volume","caffeine", "type"]]
color_values = sns.color_palette("Set2", drink_type.size)
color_map = dict(zip(drink_type, color_values))

fig, ax = plt.subplots(figsize=(10, 7))
for dt in drink_type:
    tmp =  caffeine_measures[caffeine_measures["type"]==dt]
    ax.scatter(tmp.volume, tmp.caffeine, c = tmp.type.map(color_map))

labels = list(color_map.keys())

ax.legend(labels)

ax.set_title("Caffeine over volume colored by drink type")
ax.set_xlabel("Drink volume (ml)")
ax.set_ylabel("Caffeine level (mg)")
plt.show()

coffee = df[df.type == "Coffee"]
print(coffee.describe())
print(coffee.head(50))

#Looking for text features
    #Generating one text field
drinks = df["drink"]
print(drinks)
text = ""
for d in drinks:
    text = text + " " + d

#all words to lowercase
text = text.lower()
text = remove_special_chars(text)
print(text)

#looking for the amount of unique words
text = pd.Series(text.split())
print(text.unique())
print(text.value_counts())
    #including 1-word amount
word_amount = text.value_counts()
bin = [1, 10, 20, 50, 100, 110, 170]

labels = []
for i in range(len(bin)-1):
    labels.append(str(bin[i]) + "-" + str(bin[i+1]))

valbin = pd.cut(word_amount.values, bin, labels=labels, include_lowest=True)
counts = pd.value_counts(valbin)
px = 1/plt.rcParams['figure.dpi']  # pixel in inches
fig, ax = plt.subplots(figsize=(10, 7))
ax.bar(labels, counts,color = (0,0,1, 0.8))
ax.set_title("Words occurrency")
ax.set_ylabel("number of features ")
ax.set_xlabel("Word occurrencys bin")
plt.show()

    #escluding 1-word amount
no_under_nine_word_amount = word_amount[word_amount > 9]
bin = [10, 20, 50, 100, 110, 170]

labels = []
for i in range(len(bin)-1):
    labels.append(str(bin[i]) + "-" + str(bin[i+1]))

valbin = pd.cut(no_under_nine_word_amount.values, bin, labels=labels, include_lowest=True)
counts = pd.value_counts(valbin)
px = 1/plt.rcParams['figure.dpi']  # pixel in inches
fig, ax = plt.subplots(figsize=(10, 7))
ax.bar(labels, counts,color = (0,0,1, 0.6))
ax.set_title(f"Words occurrency (total number ={no_under_nine_word_amount.size})")
ax.set_ylabel("number of features ")
ax.set_xlabel("Word occurrencys bin")
plt.show()
print(no_under_nine_word_amount)
    #Types drinks over words
df["drink"] = df["drink"].str.lower()

    #initializing dict for counting words belonging to drinks types
types_word_feature_dict = {}
for t in drink_type:
    types_word_feature_dict[f"{t}"] = 0
print(types_word_feature_dict)

    #counting words belonging to drinks types
for w in no_under_nine_word_amount.index:
    for _, row in df.iterrows():
        if w in row.drink:
           types_word_feature_dict[f"{row.type}"] = types_word_feature_dict[f"{row.type}"] + 1
print(types_word_feature_dict)

