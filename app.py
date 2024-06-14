# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 12:14:26 2023
@author: admin
"""

import pickle
import pandas as pd
import streamlit as st

# Load data and models
df = pickle.load(open('Model_test_2.pkl', 'rb'))
similarity = pickle.load(open('cosine1_sim.pkl', 'rb'))

# Set page configuration
st.set_page_config(layout="centered")

# Welcome function
def welcome():
    return "Welcome to LinkedIn Jobs Recommender System"

# Function to get job recommendations
def get_recommendations(title):
    try:
        indices = pd.Series(df.index, index=df['Job Title Cleaned'])
        idx = indices[title]
        sim_scores = list(enumerate(similarity[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:6]
        job_indices = [i[0] for i in sim_scores]
        return df[['Job Title Cleaned', 'Company', 'Industry', 'Type of role cleaned']].iloc[job_indices]
    except KeyError:
        st.error(f"Job title '{title}' not found. Please select a valid job title.")

# Main function to display UI
def main():
    st.title('LinkedIn Jobs Recommender System')

    # Display welcome message
    st.write(welcome())

    # Dropdown to select job title
    option = st.selectbox('Select a Job Title:', df['Job Title Cleaned'].values)

    # Button to trigger recommendation
    if st.button('Get Recommendations'):
        recommendation = get_recommendations(option)
        if recommendation is not None:
            st.subheader('Recommended Jobs:')
            for i, row in recommendation.iterrows():
                st.write('Job Title:', row['Job Title Cleaned'])
                st.write('Company:', row['Company'])
                st.write('Industry:', row['Industry'])
                st.write('Type of role:', row['Type of role cleaned'])
                st.write("=============================================")

# Execute main function
if __name__ == '__main__':
    main()
