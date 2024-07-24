import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=aac35e6a8d252f451d59a5652e86f348&language=en-US'.format(movie_id))
    data= response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']



def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id= movies.iloc[i[0]].movie_id
        #fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies, recommended_movies_posters



movie_dict= pickle.load(open('movie_dict.pkl', 'rb'))
movies= pd.DataFrame(movie_dict)
st.title('Movie Recommendation System')

similarity= pickle.load(open('similarity.pkl', 'rb'))


selected_movie= st.selectbox('Select movie', movies['title'].values)

if st.button('Recommend similar movies'):
    names, posters= recommend(selected_movie)
    col1, col2, col3, col4, col5= st.columns(5)
    with col1:
        st.image(posters[0])
        st.subheader(names[0])
    with col2:
        st.image(posters[1])
        st.subheader(names[1])
    with col3:
        st.image(posters[2])
        st.subheader(names[2])
    with col4:
        st.image(posters[3])
        st.subheader(names[3])
    with col5:
        st.image(posters[4])
        st.subheader(names[4])

