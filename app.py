# import pickle
# import pandas as pd
# import streamlit as st

# # Function to load data and models with error handling
# def load_data():
#     try:
#         df = pickle.load(open('Model_test_2.pkl', 'rb'))
#         similarity = pickle.load(open('cosine1_sim.pkl', 'rb'))
#         return df, similarity
#     except FileNotFoundError as e:
#         st.error(f"Pickle file not found: {e.filename}. Please ensure the necessary files are in the correct directory.")
#         st.stop()
#     except (EOFError, pickle.UnpicklingError) as e:
#         st.error(f"Error loading pickled data: {str(e)}")
#         st.stop()

# # Main function to display UI
# def main():
#     # Load data and models
#     df, similarity = load_data()

#     # Set page configuration
#     st.set_page_config(page_title="LinkedIn Jobs Recommender", layout="wide")

#     # Function to get job recommendations
#     def get_recommendations(title):
#         try:
#             indices = pd.Series(df.index, index=df['Job Title Cleaned'])
#             idx = indices[title]
#             sim_scores = list(enumerate(similarity[idx]))
#             sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#             sim_scores = sim_scores[1:6]  # Top 5 recommendations
#             job_indices = [i[0] for i in sim_scores]
#             return df.iloc[job_indices]
#         except KeyError:
#             return None

#     # Display UI elements
#     st.title('LinkedIn Jobs Recommender System')
#     st.write("Welcome to LinkedIn Jobs Recommender System")

#     # Search box for job titles
#     st.sidebar.subheader('Search for a Job Title:')
#     search_title = st.sidebar.text_input("", "").strip()
#     options = df['Job Title Cleaned'].values
#     filtered_options = [option for option in options if search_title.lower() in option.lower()]
#     option = st.sidebar.selectbox('Select a Job Title:', options=filtered_options)

#     # Multi-select for industries
#     industries = df['Industry'].unique()
#     selected_industries = st.sidebar.multiselect('Filter by Industries:', industries)

#     # Display selected filters
#     if selected_industries:
#         filtered_df = df[df['Industry'].isin(selected_industries)]
#     else:
#         filtered_df = df

#     # Button to trigger recommendation
#     if st.sidebar.button('Get Recommendations'):
#         if option:
#             recommendation = get_recommendations(option)
#             if recommendation is not None and not recommendation.empty:
#                 st.header('Recommended Jobs:')
#                 for i, row in recommendation.iterrows():
#                     st.subheader(row['Job Title Cleaned'])
#                     st.write(f"**Company:** {row['Company']}")
#                     st.write(f"**Industry:** {row['Industry']}")
#                     st.write(f"**Type of Role:** {row['Type of role cleaned']}")
#                     st.markdown("---")
#             else:
#                 st.warning(f"No recommendations found for '{option}'. Please select another job title or adjust filters.")
#         else:
#             st.warning("Please select a job title.")

#     # Display filtered data table
#     st.subheader('Filtered Job Data:')
#     st.dataframe(filtered_df[['Job Title Cleaned', 'Company', 'Industry', 'Type of role cleaned']])

# # Execute main function
# if __name__ == '__main__':
#     main()

import pickle
import pandas as pd
import streamlit as st
import plotly.express as px

# Function to load data and models with error handling
def load_data():
    try:
        df = pickle.load(open('Model_test_2.pkl', 'rb'))
        similarity = pickle.load(open('cosine1_sim.pkl', 'rb'))
        return df, similarity
    except FileNotFoundError as e:
        st.error(f"Pickle file not found: {e.filename}. Please ensure the necessary files are in the correct directory.")
        st.stop()
    except (EOFError, pickle.UnpicklingError) as e:
        st.error(f"Error loading pickled data: {str(e)}")
        st.stop()

# Function for user authentication
def authenticate(username, password):
    # Replace with actual authentication logic
    correct_username = 'admin'
    correct_password = 'password'
    return username == correct_username and password == correct_password

# Main function to display UI
def main():
    # Load data and models
    df, similarity = load_data()

    # Set page configuration
    st.set_page_config(page_title="LinkedIn Jobs Recommender", layout="wide")

    # Sidebar for login
    st.sidebar.title('Login')
    username = st.sidebar.text_input('Username')
    password = st.sidebar.text_input('Password', type='password')
    login_button = st.sidebar.button('Login')

    # Authenticate user
    if login_button:
        if authenticate(username, password):
            st.sidebar.success(f'Logged in as {username}')
            st.session_state.logged_in = True
        else:
            st.sidebar.error('Incorrect username or password')

    # Display main content if logged in
    if st.session_state.get('logged_in'):
        st.title('LinkedIn Jobs Recommender System')
        st.write("Welcome to LinkedIn Jobs Recommender System")

        # Function to get job recommendations
        def get_recommendations(title):
            try:
                indices = pd.Series(df.index, index=df['Job Title Cleaned'])
                idx = indices[title]
                sim_scores = list(enumerate(similarity[idx]))
                sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
                sim_scores = sim_scores[1:6]  # Top 5 recommendations
                job_indices = [i[0] for i in sim_scores]
                return df.iloc[job_indices]
            except KeyError:
                return None

        # Sidebar for search and filters
        st.sidebar.subheader('Search and Filters:')
        search_title = st.sidebar.text_input("Search for a Job Title:")
        options = df['Job Title Cleaned'].values
        filtered_options = [option for option in options if search_title.lower() in option.lower()]
        option = st.sidebar.selectbox('Select a Job Title:', options=filtered_options)

        # Multi-select for industries
        industries = df['Industry'].unique()
        selected_industries = st.sidebar.multiselect('Filter by Industries:', industries)

        # Display selected filters
        if selected_industries:
            filtered_df = df[df['Industry'].isin(selected_industries)]
        else:
            filtered_df = df

        # Button to trigger recommendation
        if st.sidebar.button('Get Recommendations'):
            if option:
                recommendation = get_recommendations(option)
                if recommendation is not None and not recommendation.empty:
                    st.header('Recommended Jobs:')
                    for i, row in recommendation.iterrows():
                        st.subheader(row['Job Title Cleaned'])
                        st.write(f"**Company:** {row['Company']}")
                        st.write(f"**Industry:** {row['Industry']}")
                        st.write(f"**Type of Role:** {row['Type of role cleaned']}")
                        st.markdown("---")
                else:
                    st.warning(f"No recommendations found for '{option}'. Please select another job title or adjust filters.")
            else:
                st.warning("Please select a job title.")

        # Display filtered job data
        st.subheader('Filtered Job Data:')
        st.dataframe(filtered_df[['Job Title Cleaned', 'Company', 'Industry', 'Type of role cleaned']])

        # User feedback section
        st.subheader('User Feedback:')
        user_feedback = st.text_area('Share your feedback or comments here:', height=150)
        if st.button('Submit Feedback'):
            # Implement logic to store or process user feedback (e.g., save to database)
            st.success('Feedback submitted successfully! Thank you.')

    else:
        st.info('Please login to access the LinkedIn Jobs Recommender System.')

# Execute main function
if __name__ == '__main__':
    main()
