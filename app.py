import streamlit as st
import pickle
import pandas as pd
import requests

movies=pickle.load(open('movie.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))
movies_list=movies['title'].values 
st.title("Movie Recommender System")
st.title("Hi, there Let's start")


def fetch_poster(movie_id):
    print(movie_id)
    headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0OTcyZmU2MmU1Nzg4YjAxYmU0NjNiOWZhZWZiMTE5MSIsIm5iZiI6MTczMDY0NjA5Ni4xNTA0MDMsInN1YiI6IjY3Mjc4Y2JmNzYxOTc5ZjAwNWUyYWExOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.cH7vpIzqmhyGrsRKqBMNcKSAjlQOaZMf8LG7Rew6m38"}
    response=requests.get('https://api.themoviedb.org/3/movie/{}'.format(movie_id),headers=headers)
    # response=requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    

    data=response.json()
    poster_path=data['poster_path']
    full_path= "https://image.tmdb.org/t/p/w500" + poster_path
    return full_path


def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_lists=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommend_movies=[]
    recommend_movies_poster=[]
    for i in movies_lists:
        movie_id=movies.iloc[i[0]].movie_id
        print(movie_id)
        
        recommend_movies.append(movies.iloc[i[0]].title)
        #fetch Poster from API
        recommend_movies_poster.append(fetch_poster(movie_id))

    return recommend_movies,recommend_movies_poster


option = st.selectbox(
    "Which type of movies would you like to see related to this?  try these example --> spiderman,Avengers, Dark knight rises",
    movies_list,
)

st.write("You selected:", option)

if st.button("Recommend"):
    recommendation,posters=recommend(option)
    columns = st.columns(5)

    for i in range(len(columns)):
        with columns[i]:
            st.text(recommendation[i])
            st.image(posters[i])


    # with col1:
    #     st.header(recommendation[0])
    #     st.image(posters[0])

    # with col2:
    #     st.header(recommendation[1])
    #     st.image(posters[1])

    # with col3:
    #     st.header(recommendation[2])
    #     st.image(posters[2])
    # with col4:
    #     st.header(recommendation[3])
    #     st.image(posters[3])
    # with col4:
    #     st.header(recommendation[4])
    #     st.image(posters[4])