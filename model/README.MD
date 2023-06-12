# Coffe Break

This project includes several files for data exploration, feature extraction, and model training on caffeine data.

## Files

### `eda.py`

This file performs exploratory data analysis on the caffeine data. It includes the following functionalities:

- Importing necessary libraries (`numpy`, `pandas`, `matplotlib.pyplot`, `seaborn`, `sklearn.cluster.DBSCAN`).
- Reading the data from the `caffeine.csv` file.
- Displaying the first 10 rows of the dataset.
- Providing general statistics of the dataset.
- Displaying unique values of the "type" column.
- Renaming column names and converting them to lowercase.
- Plotting the types and amounts of drinks using a bar chart.
- Calculating and displaying the percentage of each drink type.
- Creating a new column "caffeine_over_ml" by dividing "caffeine" by "volume".
- Plotting the caffeine level over volume, colored by drink type.
- Removing volume outliers by filtering out drinks with volumes greater than 800 ml.
- Creating a violin plot of caffeine distribution over drink types.
- Removing caffeine outliers by filtering out drinks with caffeine greater than 500 mg.
- Creating a box plot to check for outliers in the caffeine feature.
- Creating box plots to check for outliers in the volume feature for all drink types except "Energy Shots" and "Soft Drinks."
- Creating box plots to check for outliers in the volume feature for "Energy Shots" and "Soft Drinks" separately.
- Removing outliers for "Energy Shots" and "Soft Drinks" by filtering the dataset based on volume ranges.
- Displaying descriptive statistics of the cleaned dataset.
- Plotting the volume distribution after removing outliers for "Energy Shots" and "Soft Drinks."
- Plotting the types and amounts of drinks after removing outliers.
- Creating a correlation matrix heatmap.

### `feature_extraction.py`

This file performs feature extraction on the caffeine data. It includes the following functionalities:

- Importing necessary libraries (`pandas`, `re`, `matplotlib.pyplot`, `seaborn`, `numpy`, `sklearn.preprocessing`).
- Defining a function to remove special characters from the drink names.
- Reading the cleaned data from the `clean_caffeine.csv` file.
- Plotting the caffeine level over volume, colored by drink type.
- Extracting all drink names to generate a single text field.
- Converting the text to lowercase and removing special characters.
- Counting the number of unique words and their occurrences.
- Creating bins for word occurrences and plotting a bar chart.
- Filtering out words with less than 10 occurrences and plotting a bar chart.
- Counting the occurrences of words belonging to each drink type.
- Printing the count of words belonging to each drink type.

### `model_training.py`

This file trains a model on the caffeine data. It includes the following functionalities:

- Importing necessary libraries (`csv`, `pandas`, `sklearn.feature_extraction.text.TfidfVectorizer`, `sklearn.preprocessing.LabelEncoder`, `sklearn.linear_model.LogisticRegression`, `sklearn.pipeline.Pipeline`, `pickle`).
- Defining functions to preprocess drink names by converting them to lowercase and removing special characters.
- Reading the cleaned data from the `clean_caffeine.csv` file.
- Splitting the data into labels and features.
- Adding word features using TF-IDF vectorization.
- Converting the feature vector to a dataframe.
- Encoding labels using LabelEncoder.
- Training a logistic regression model.
- Saving the trained model, label encoder, TF-IDF vectorizer, and TF-IDF features.
