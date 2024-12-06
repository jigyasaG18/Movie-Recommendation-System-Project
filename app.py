import pickle
import streamlit as st
import requests
import os

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
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

def download_file_from_google_drive(file_id, destination):
    URL = f"https://drive.google.com/uc?id={file_id}"
    response = requests.get(URL)
    with open(destination, 'wb') as f:
        f.write(response.content)

st.header('Movie Recommender System')

# Load movie list
if not os.path.exists('model/movie_list.pkl'):
    st.error("The movie_list.pkl file was not found. Please ensure it is in the correct directory.")
else:
    movies = pickle.load(open('model/movie_list.pkl', 'rb'))

# Download and load the similarity matrix
similarity_file_id = '1_UlR2lx89WlIdUjAgsdxXZo20QJ7WyqP'  # Google Drive file ID
similarity_file_path = 'similarity.pkl'

if not os.path.exists(similarity_file_path):
    st.write("Downloading similarity.pkl from Google Drive...")
    download_file_from_google_drive(similarity_file_id, similarity_file_path)
else:
    st.write("Found similarity.pkl, loading it...")

similarity = pickle.load(open(similarity_file_path, 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            if recommended_movie_posters[i]: 
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])
            else:
                st.text(recommended_movie_names[i])
                st.text("Poster not available")  

# Google Drive URL construction for other purposes
file_id = '1_UlR2lx89WlIdUjAgsdxXZo20QJ7WyqP'  # Updated file ID
share_url = f'https://drive.google.com/file/d/{file_id}/view?usp=sharing'
st.markdown(f"Access the file via this [Google Drive link]({share_url})")
