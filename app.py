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
st.set_page_config(layout="wide")

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
        return None

# Main function to display UI
def main():
    st.title('LinkedIn Jobs Recommender System')

    # Display welcome message
    st.write(welcome())

    # Sidebar with job selection
    st.sidebar.subheader('Select a Job Title:')
    option = st.sidebar.selectbox('', df['Job Title Cleaned'].values)

    # Button to trigger recommendation
    if st.sidebar.button('Get Recommendations'):
        recommendation = get_recommendations(option)
        if recommendation is not None and not recommendation.empty:
            st.header('Recommended Jobs:')
            for i, row in recommendation.iterrows():
                st.subheader('Job Title:')
                st.write(row['Job Title Cleaned'])
                st.subheader('Company:')
                st.write(row['Company'])
                st.subheader('Industry:')
                st.write(row['Industry'])
                st.subheader('Type of Role:')
                st.write(row['Type of role cleaned'])
                st.markdown("---")
        else:
            st.warning(f"No recommendations found for '{option}'. Please select another job title.")

# Execute main function
if __name__ == '__main__':
    main()
