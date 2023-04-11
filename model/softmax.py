import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, classification_report, confusion_matrix
import seaborn as sns
from matplotlib import pyplot as plt

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

pd.set_option("display.max_columns", None)

#read data
df = pd.read_csv("clean_caffeine.csv")

#statistics
print("First 10 rows...\n")
print(df.head(10))
print("\n\n")
print("General statistics...\n")
print(df.describe())
print("\n\n")

#splitting trainining testing
label = df["type"]
df.drop(columns='type' , axis=1,inplace=True)
X_train, X_test, t_train, t_test = train_test_split(df, label, test_size=0.30, random_state=42)

#Adding words features using TFIDF (see feature_exctraction.py)
X_train.drink = clean_drink(X_train.drink)
X_train = X_train.reset_index()
tfid_enc = TfidfVectorizer(min_df=5, max_df=150, ngram_range=(1,3))

    #drinks features using TfidfVectorizer
drinks_word_features = tfid_enc.fit_transform(X_train.drink)
    #converting feature vector to dataframe
drinks_word_features = pd.DataFrame(drinks_word_features.toarray().transpose(),
                   index=tfid_enc.get_feature_names())
    #dropping drinks names from df
X_train.drop(columns= ["drink", "index"] ,axis=1, inplace=True)
    #resultant dataframe
X_train = pd.concat([X_train, drinks_word_features.transpose()], axis=1)

#label encoder
le = LabelEncoder()
le.fit(t_train)
t_train = le.transform(t_train)

#Model Tuning
parameters ={'penalty':['l1', 'l2'], 'C':[0.1,0.3,0.5,0.7,0.9, 1.0] , 'solver' : ['liblinear', 'saga'] , 'multi_class': ['auto'], 'max_iter':[100,800]}
soft_reg = LogisticRegression()

    #Grid-Search combine with cv
clf_w = GridSearchCV(soft_reg, parameters, scoring='f1_weighted' , cv= 5 )
clf_a = GridSearchCV(soft_reg, parameters, scoring='f1_macro' , cv= 5 )
clf_w.fit(X_train, t_train)
clf_a.fit(X_train, t_train)
    #best-score
print("best softmax score...\n")
print(clf_w.best_score_)
print(clf_a.best_score_)
print("best softmax params...\n")
print(clf_w.best_params_)
print(clf_a.best_params_)

#Model Selection

    #Training Model
clf = LogisticRegression(C=0.9, max_iter=100,  multi_class="auto", penalty='l2', solver='liblinear')
clf.fit(X_train,t_train)
    #label encoder
t_test = le.transform(t_test)
    #TFIDF test trasform
        #Adding words features using TFIDF (see feature_exctraction.py)
X_test.drink = clean_drink(X_test.drink)
X_test = X_test.reset_index()
drinks_word_features_test = tfid_enc.transform(X_test.drink)
        #converting feature vector to dataframe
drinks_word_features_test = pd.DataFrame(drinks_word_features_test.toarray().transpose(),
                   index=tfid_enc.get_feature_names())
        #dropping drinks names from df
X_test.drop(columns= ["drink", "index"] ,axis=1, inplace=True)
        #resultant dataframe
X_test = pd.concat([X_test, drinks_word_features_test.transpose()], axis=1)

    #predict
predicted = clf.predict(X_test)
    #scoring

print(classification_report(le.inverse_transform(t_test), le.inverse_transform(predicted), target_names= label.unique()))
mat = confusion_matrix(le.inverse_transform(t_test), le.inverse_transform(predicted), labels= label.unique())
fig, ax = plt.subplots(figsize=(10, 10))
ax = sns.heatmap(mat.T, square = True, annot = True, fmt ='d', cbar = False, xticklabels =  label.unique(), yticklabels =  label.unique())
plt.title('Confusion Matrix Softmax Regression')
plt.xlabel('true label')
plt.ylabel('predicted labels')
plt.show()

#best model
#{'C': 0.9, 'max_iter': 100, 'multi_class': 'auto', 'penalty': 'l2', 'solver': 'liblinear'}

