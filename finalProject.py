#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 10:37:46 2019

@author: CritterWilson
"""

import pandas as pd
import numpy as np
from sklearn import tree
from progress.bar import Bar
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
# Load in the Data
data = pd.read_csv("movie_metadata.csv", header=0, skipinitialspace = False, na_values=["?"])
# =============================================================================
# Pre-Precessing
# =============================================================================
data = data.drop(columns=['color', 'num_critic_for_reviews', 'duration',
       'director_facebook_likes', 'actor_3_facebook_likes', 'language',
       'actor_1_facebook_likes', 'num_voted_users', 'cast_total_facebook_likes',
       'facenumber_in_poster', 'num_user_for_reviews', 'movie_imdb_link',
       'actor_2_facebook_likes', 'aspect_ratio', 'country',
       'movie_facebook_likes', 'movie_title'])
# Drop the null for the following - they weren't valuable anyway (we checked)
data = data.dropna(subset=['plot_keywords'])
data = data.dropna(subset=['actor_1_name'])
# Fill the null with the actor_1_name because it provides more data without
#  sacrificing valuable info (there weren't a ton with this issue)
data.actor_2_name = data.actor_2_name.fillna(data.actor_1_name)
data.actor_3_name = data.actor_3_name.fillna(data.actor_1_name)
data.director_name = data.director_name.fillna(data.actor_1_name)
# Fill the null with "Not Rated" - we checked
data.content_rating = data.content_rating.fillna("Not Rated")
# Fill the null with the mean value (dates and budgets and gross shouldn't
#  be a deciding factor in this algorithm anyway)
data.gross = data.gross.fillna(data.gross.mean())
data.budget = data.budget.fillna(data.budget.mean())
data.title_year = data.title_year.fillna(data.title_year.mean())
# Now we need to make new row items for every plot key word and genre
# A basic list will make this faster (trust me... I tried everything else)
data_list = []
# For each row in our data grame...
for index, row in data.iterrows():
    # ...split the plot_keywords and genres columns by the '|' delimeter
    kw = row.plot_keywords
    genre = row.genres
    kw_list = kw.split("|")
    genre_list = genre.split("|")
    # For each key word...
    for kw_new in kw_list:
        # ...and for each genre...
        for genre_new in genre_list:
            # ...make a new row in our list...
            new_row = data.loc[index].values
            # ...and add replace to columns with the new value
            new_row[6] = kw_new
            new_row[3] = genre_new
            # Append our new row onto the list 
            data_list.append(new_row)
# Convert the primitive list into a pandas dataframe
data = pd.DataFrame(data_list, columns=data.columns.values)
# Make dictionaires for later reference
le_director = LabelEncoder()
le_actor1 = LabelEncoder()
le_actor2 = LabelEncoder()
le_actor3 = LabelEncoder()
le_keywords = LabelEncoder()
le_genres = LabelEncoder()
le_rating = LabelEncoder()

data.director_name = le_director.fit_transform(data.director_name)
data.actor_1_name = le_actor1.fit_transform(data.actor_1_name)
data.actor_2_name = le_actor2.fit_transform(data.actor_2_name)
data.actor_3_name = le_actor3.fit_transform(data.actor_3_name)
data.plot_keywords = le_keywords.fit_transform(data.plot_keywords)
data.genres = le_genres.fit_transform(data.genres)
data.content_rating = le_rating.fit_transform(data.content_rating)

x = data.drop(columns=["plot_keywords"]).to_numpy()
y = data["plot_keywords"].to_numpy()

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)

id3 = tree.DecisionTreeClassifier()
id3.fit(x_train, y_train)
y_pred = id3.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print("id3 Accuracy: {}".format(accuracy))
