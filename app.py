import pickle
import pandas as pd
import streamlit as st

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

# Main function to display UI
def main():
    # Load data and models
    df, similarity = load_data()

    # Set page configuration
    st.set_page_config(page_title="LinkedIn Jobs Recommender", layout="wide")

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

    # Display UI elements
    st.title('LinkedIn Jobs Recommender System')
    st.write("Welcome to LinkedIn Jobs Recommender System")

    # Search box for job titles
    search_title = st.text_input("Search for a Job Title:")
    options = df['Job Title Cleaned'].values
    filtered_options = [option for option in options if search_title.lower() in option.lower()]
    option = st.selectbox('Select a Job Title:', options=filtered_options)

    # Multi-select for industries
    industries = df['Industry'].unique()
    selected_industries = st.multiselect('Select Industries:', industries)

    # Button to trigger recommendation
    if st.button('Get Recommendations'):
        if option:
            recommendation = get_recommendations(option)
            if recommendation is not None and not recommendation.empty:
                st.header('Recommended Jobs:')
                for i, row in recommendation.iterrows():
                    st.write(f"**Job Title:** {row['Job Title Cleaned']}")
                    st.write(f"**Company:** {row['Company']}")
                    st.write(f"**Industry:** {row['Industry']}")
                    st.write(f"**Type of Role:** {row['Type of role cleaned']}")
                    st.markdown("---")
            else:
                st.warning(f"No recommendations found for '{option}'. Please select another job title.")
        else:
            st.warning("Please select a job title.")

# Execute main function
if __name__ == '__main__':
    main()


