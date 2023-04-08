import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, classification_report, confusion_matrix
import seaborn as sns
from matplotlib import pyplot as plt

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

#dropping drinks names
df.drop(columns= "drink" ,axis=1, inplace=True)

#splitting trainining testing
label = df["type"]
df.drop(columns='type' , axis=1,inplace=True)
X_train, X_test, t_train, t_test = train_test_split(df, label, test_size=0.30, random_state=42)

#MinMaxscaler
scaler = MinMaxScaler()
scaler.fit(X_train)
X_train = pd.DataFrame(data = scaler.transform(X_train),columns= X_train.columns )
print(X_train.head())


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
clf = LogisticRegression(penalty='none', solver='saga')
clf.fit(X_train,t_train)
    #MinMaxscaler
X_test = pd.DataFrame(data = scaler.transform(X_test),columns= X_test.columns )
    #label encoder
t_test = le.transform(t_test)
    #predict
predicted = clf.predict(X_test)
    #scoring

print(classification_report(le.inverse_transform(t_test), le.inverse_transform(predicted), target_names= label.unique()))
mat = confusion_matrix(le.inverse_transform(t_test), le.inverse_transform(predicted), labels= label.unique())
sns.heatmap(mat.T, square = True, annot = True, fmt ='d', cbar = False, xticklabels =  label.unique(), yticklabels =  label.unique())
plt.title('Confusion Matrix Softmax Regression')
plt.xlabel('true label')
plt.ylabel('predicted labels')
plt.show()



