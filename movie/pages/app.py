import os
import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Get the absolute path of the current file's directory
FILE_DIR = os.path.dirname(os.path.abspath(__file__))

# Get the absolute path of the project's root directory
PARENT_DIR = os.path.abspath(os.path.join(FILE_DIR, os.pardir))

# Get the absolute path of the directory containing the resources
RESOURCES_DIR = os.path.join(PARENT_DIR, "resources")

# Get the absolute path of the movie.csv file
DATA_PATH = os.path.join(RESOURCES_DIR, "data", "movie.csv")

# Get the absolute path of the model pickle file
MODEL_PATH = os.path.join(RESOURCES_DIR, "data", "nn_model1.pkl")

# Get the absolute path of the movie vector pickle file
VECTOR_PATH = os.path.join(RESOURCES_DIR, "data", "movie_vector.pkl")

# Load the movie dataframe from the CSV file
df = pd.read_csv(DATA_PATH)

# Load the model from the pickle file
model = pickle.load(open(MODEL_PATH, 'rb'))

# Load the movie vector from the pickle file
vector = pickle.load(open(VECTOR_PATH, 'rb'))

df.drop(labels='Unnamed: 0',axis=1,inplace=True)
#st.dataframe(df)

# Function to recommend movies based on user input
df = df.reset_index(drop=True)
def recommend_movies(movie_title, top_n=5):
    movie_title = movie_title.lower()
    filtered_movies = df[df['title'].str.lower() == movie_title]

    if filtered_movies.empty:
        return []

    movie_index = filtered_movies.index[0]

    # Get the feature vector for the given movie
    movie_vector = vector[movie_index].toarray()
    movie_vector = np.reshape(movie_vector, (1, -1))

    # Find the k nearest neighbors
    distances, indices = model.kneighbors(movie_vector)

    # Get the top N recommendations (excluding the given movie itself)
    top_recommendations = []
    for index in indices[0]:
        if df.iloc[index]['title'].lower() != movie_title:
            top_recommendations.append(df.iloc[index]['title'])
        if len(top_recommendations) == top_n:
            break

    return top_recommendations

# Streamlit app
def main():
    st.title("Movie Recommendation System")

    # User input
    movie_title = st.text_input("Enter movie title:")
    top_n = st.slider("Number of recommendations:", min_value=1, max_value=10, value=5)

    if st.button("Recommend"):
        # Perform movie recommendations
        recommended_movies = recommend_movies(movie_title, top_n)

        # Display the recommended movies
        st.subheader("Recommended Movies:")
        if recommended_movies:
            for movie in recommended_movies:
                st.write(movie)
        else:
            st.write("No movies found based on the given input.")

if __name__ == "__main__":
    main()