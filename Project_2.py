# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 12:14:26 2023

@author: admin
"""

import pickle
import pandas as pd
import streamlit as st

#JB_dict = pickle.load(open('Model_test_2.pkl', 'rb'))
df = pickle.load(open('Model_test_2.pkl', 'rb'))
#Jobs = pd.DataFrame(JB_dict, columns = ['Job Title Cleaned'])
similarity = pickle.load(open('cosine1_sim.pkl', 'rb'))
#titles = pickle.load(open('title.pkl', 'rb'))

#indices = pickle.load(open('indices.pkl', 'rb'))

#indices = pd.Series(df.index, index = df['Job Title Cleaned']).drop_duplicates()

st.set_page_config(layout="centered")

def welcome():
    return "Welcome All"


def get_recommendations(title):
    indices = pd.Series(df.index, index=df['Job Title Cleaned'])
    idx = indices[title]
    titles = df['Job Title Cleaned']
    #indices = pd.Series(df.index, index=df['Job Title Cleaned'])
    sim_scores = list(enumerate(similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    job_indices = [i[0] for i in sim_scores]
    #return titles.iloc[job_indices]
    return df[['Job Title Cleaned', 'Company', 'Industry', 'Type of role cleaned']].iloc[job_indices]

st.title('Jobs Recommender System')

option = st.selectbox('Select your Job: ', df['Job Title Cleaned'].values)

if st.button('Click here to Recommend'):
    recommendation = get_recommendations(option)
    for i, row in recommendation.iterrows():
        st.write('Job Title: ', row['Job Title Cleaned'])
        #st.write("Job Title: ", row['Job Title Cleaned'], " | Company: ", row['Company'], " | Industry: ", row['Industry'],"| Type of Role: ", row['Type of role cleaned'])
        st.write('Company: ', row['Company'])
        st.write('Industry: ', row['Industry'])
        st.write('Type of role: ', row['Type of role cleaned'])
        st.write("=============================================")
        