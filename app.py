import streamlit as st
import pickle
import requests

movie_df = pickle.load(open("movie.pkl", "rb") )

movie_list=movie_df['title'].values

similarity = pickle.load(open("similarity.pkl", "rb") )

api_key = "566ab5474b6adc8043380981f035265d"
#fetch poster
def get_poster(movie_id):
     json_data=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=566ab5474b6adc8043380981f035265d&language=en-US'.format(movie_id))
     json_data = json_data.json()
     # st.text("https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US".format(movie_id))
     # print(json_data)
     return json_data['poster_path']
#fucntion to recommend movies
poster_path=[]
def five_similar_movie(movie):
     movie_index = movie_df[movie_df['title'] == movie].index[0]
     distances = similarity[movie_index]
     movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

     five_movie=[]
     poster_path = []
     poster_base_path="http://image.tmdb.org/t/p/w500"
     for i in movie_list:
          movie_id=movie_df.iloc[i[0]].id
          # print(movie_id)
          five_movie.append(movie_df.iloc[i[0]].title)

          poster_path.append(poster_base_path+get_poster(movie_id))

     return five_movie, poster_path


st.title("Movie Recommender System")

selected_movie = st.selectbox(
     'How would you like to be contacted?',
     movie_list)

if st.button("Recommendations"):
     recommended_movies, movie_poster=five_similar_movie(selected_movie)
     col1, col2, col3, col4, col5 = st.columns(5)
     for index, value in enumerate(st.columns(5)):
          with value:
               st.text(recommended_movies[index])
               st.image(movie_poster[index])
