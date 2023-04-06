import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import DBSCAN

df = pd.read_csv("caffeine.csv")
print("First 10 rows...\n")
print(df.head(10))
print("\n\n")
print("General statistics...\n")
print(df.describe())
print("\n\n")

print("unique type values...\n")
print(df["type"].unique())

#renaming columns names
df.rename(columns={"Volume (ml)": "volume", "Caffeine (mg)":"caffeine"}, inplace=True)
df.rename(str.lower, axis ="columns", inplace=True)
drink_type = df["type"].unique()
drink_counts = df["type"].value_counts()

print(df.info())

#plotting caffeine drinks type
fig, ax = plt.subplots(figsize=(10, 7))
bars = ax.bar(drink_type, drink_counts, width=1, edgecolor="white", linewidth=0.7)
ax.set_title("Types and amounts of drinks")
ax.set_xlabel("Types of drinks")
ax.set_ylabel("Number of occurrences")

total_amount_drinks = sum(df["type"].value_counts())
print(total_amount_drinks)

n_bar = 0
for b in bars:
    type_amout = b.get_height()
    percent = int(type_amout * 100 / total_amount_drinks)
    ax.annotate('{}%'.format(percent), xy=(b.get_x() + b.get_width() / 2, type_amout/2),
                xytext=(0, 3),  # 3 points vertical offset
                color= "white",
                fontsize= 12,
                textcoords="offset points",
                ha='center', va='bottom')

plt.show()

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

#removing volume outliers
#I assumed that drinks with volumes greater than 800 ml are not so frequent
df = df[df.volume < 800]

#violinplot of caffeine over type of drink
fig, ax = plt.subplots(figsize=(10, 7))
ax = sns.violinplot(y="caffeine", x="type", data=caffeine_measures , )
ax.set_title("Caffeine distribution over drink types")
plt.show()

#removing caffeine outliers
#I assumed that drinks with caffeine greater than 500 mg are not so frequent
df = df[df.caffeine < 500]

#boxplot for check if there are other outliers in caffeine feature
fig, ax = plt.subplots(figsize=(10, 7))
ax = sns.boxplot(y="caffeine", x="type", data= df)
ax.set_title("caffeine distribution after removing outliers")
plt.show()

#boxplot for check if there are other outliers in volume feature

    #all drinks type besideze Soft Drink and Energy Drink
fig, ax = plt.subplots( figsize=(10, 7))
sns.boxplot(y="volume", x="type", data= df[(df.type != "Energy Shots") & (df.type !="Soft Drinks")])
ax.set_title("volume distribution after removing overall outliers (not Energy Shots | Soft Drinks ")
ax.set_title("volume distribution after removing overall outliers (not Energy Shots | Soft Drinks ")
plt.show()

    #only Soft Drink and Energy Drink
fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(10, 7))
sns.boxplot(y="volume", x="type", data= df[df.type == "Energy Shots"] , ax=axs[0])
sns.boxplot(y="volume", x="type", data= df[df.type =="Soft Drinks"], ax=axs[1])
axs[0].set_title("volume distribution after removing overall outliers (Energy Shots)")
axs[0].set_xlabel("")
axs[0].set_ylabel("")
axs[1].set_title("volume distribution after removing overall outliers (Soft Drinks)")
plt.show()

    #removing Soft Drink and Energy Drink outliers
energy_shots = df[df.type == "Energy Shots"]
energy_shots = energy_shots[energy_shots.volume < 70]
energy_shots = energy_shots[energy_shots.volume > 24]

soft_drink = df[df.type == "Soft Drinks"]
soft_drink = soft_drink[soft_drink.volume < 400]
soft_drink = soft_drink[soft_drink.volume > 260]

df = df[df.type != "Energy Shots"]
df = df[df.type != "Soft Drinks"]
df = df.append(soft_drink)
df = df.append(energy_shots)

print(df.describe())
print(df[df.type=="Energy Shots"])

    #only Soft Drink and Energy Drink after outlier where removed
fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(10, 7))
sns.boxplot(y="volume", x="type", data= df[df.type == "Energy Shots"] , ax=axs[0])
sns.boxplot(y="volume", x="type", data= df[df.type =="Soft Drinks"], ax=axs[1])
axs[0].set_title("volume distribution after removing outliers (Energy Shots)")
axs[0].set_xlabel("")
axs[0].set_ylabel("")
axs[1].set_title("volume distribution after removing outliers (Soft Drinks)")
plt.show()

#plotting caffeine drinks type after outliers where removed
fig, ax = plt.subplots(figsize=(10, 7))
bars = ax.bar(drink_type, drink_counts, width=1, edgecolor="white", linewidth=0.7, color="green")
ax.set_title("Types and amounts of drinks")
ax.set_xlabel("Types of drinks")
ax.set_ylabel("Number of occurrences")

total_amount_drinks = sum(df["type"].value_counts())
print(total_amount_drinks)

n_bar = 0
for b in bars:
    type_amout = b.get_height()
    percent = int(type_amout * 100 / total_amount_drinks)
    ax.annotate('{}%'.format(percent), xy=(b.get_x() + b.get_width() / 2, type_amout/2),
                xytext=(0, 3),  # 3 points vertical offset
                color= "white",
                fontsize= 12,
                textcoords="offset points",
                ha='center', va='bottom')

plt.show()

#correlation Matrix
fig, ax = plt.subplots(figsize=(10, 7))
ax = sns.heatmap(df.corr(), vmin= -1, vmax= 1, annot= True)
plt.show()

df.to_csv("clean_caffeine.csv", sep=",")

