import pickle
import streamlit as st
import requests
import pandas as pd
import imdb
import streamlit as st


st.set_page_config(page_title='Movie Recommender', layout='wide')

similarity_score = pickle.load(open('similarity.pkl', 'rb'))
movie_list = pickle.load(open('movie_list.pkl', 'rb'))
movie = pd.DataFrame(movie_list)

def get_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=6ab879cdd9872568a41d5adc835df231&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movies):
    index = movie[movie['title'] == movies].index[0]
    #distances=similarity_score[index]
    movies_list = sorted(list(enumerate(similarity_score[index])),reverse=True,key = lambda x: x[1])[1:6]
    recommended_movies =[]
    movie_poster=[]

    for i in movies_list[:]:
        movie_id = movie.iloc[i[0]].id

        recommended_movies.append(movie.iloc[i[0]].title)

        movie_poster.append(get_poster(movie_id)) #get poster from API
    return recommended_movies,movie_poster




st.title('Movie Recommender System')
st.write('Welcome to the Movie Recommender System. Select a movie to get personalized recommendations!')

option = st.sidebar.selectbox('Select a movie', movie['title'].values.tolist())
#options = movie['title'].values.tolist()  # Convert the movie titles to a list

#option = st.selectbox(
    #'Select a movie',
    #movie['title'].values.tolist()
#)
button_pressed = st.sidebar.button('Recommend')
#button_pressed = st.button('Recommend')  # Add a button and store its state

try:
    if button_pressed:
        with st.spinner('Fetching recommendations...'):
            recommended_movies, movie_poster = recommend(option)
        if recommended_movies:
            num_recommendations = len(recommended_movies)
            num_columns = min(num_recommendations, 5)
            columns = st.columns(num_columns)
            for i in range(num_recommendations):
                with columns[i % num_columns]:
                    st.text(recommended_movies[i])
                    st.image(movie_poster[i])
        else:
            st.warning('No recommendations found for the selected movie.')
except Exception as e:
    st.error('An error occurred: {}'.format(str(e)))