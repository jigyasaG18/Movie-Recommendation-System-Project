import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data.get('poster_path')
    if poster_path is not None:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    return None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Update: using a loop for displaying posters
    cols = st.columns(5)  # Create 5 columns for displaying movies
    for i in range(5):
        with cols[i]:
            if recommended_movie_posters[i]:  # Check if poster exists
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])
            else:
                st.text(recommended_movie_names[i])
                st.text("Poster not available")  # Handle missing poster gracefully

# Hardcoded Google Drive link
google_drive_link = "https://drive.google.com/file/d/1_UlR2lx89WlIdUjAgsdxXZo20QJ7WyqP/view?usp=sharing"
st.markdown(f"Access the file via this [Google Drive link]({google_drive_link})")
