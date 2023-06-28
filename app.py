import pickle
import streamlit as st
import requests
import pandas as pd
import time

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=57102a94faf2460c8371270e77e29d2b"
    retry_count = 3
    retry_delay = 1  # seconds

    while retry_count > 0:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if 'poster_path' in data:
                poster_path = data['poster_path']
                full_path = "https://image.tmdb.org/t/p/w500" + poster_path
                return full_path
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_count -= 1

    return None

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title('Movie recommender system')
selected_movie_name = st.selectbox(
    'Hey there, choose a movie.',
    movies['title'].values)

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

if st.button('recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        if posters[0] is not None:
            st.image(posters[0])
    with col2:
        st.text(names[1])
        if posters[1] is not None:
            st.image(posters[1])

    with col3:
        st.text(names[2])
        if posters[2] is not None:
            st.image(posters[2])
    with col4:
        st.text(names[3])
        if posters[3] is not None:
            st.image(posters[3])
    with col5:
        st.text(names[4])
        if posters[4] is not None:
            st.image(posters[4])
