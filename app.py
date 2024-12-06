import pickle
import streamlit as st
import requests
import os

def download_file_from_google_drive(file_id, destination):
    URL = f"https://drive.google.com/uc?id={file_id}"  # Correct the download URL
    response = requests.get(URL)
    
    if response.status_code == 200:
        with open(destination, 'wb') as f:
            f.write(response.content)
    else:
        st.error("Failed to download file. Please check the Google Drive link or your internet connection.")

st.header('Movie Recommender System')

# Load movie list
if not os.path.exists('movie_list.pkl'):
    st.error("The movie_list.pkl file was not found. Please ensure it is in the correct directory.")
else:
    movies = pickle.load(open('movie_list.pkl', 'rb'))

# Download and load the similarity matrix
similarity_file_id = '1_UlR2lx89WlIdUjAgsdxXZo20QJ7WyqP'  # Google Drive file ID
similarity_file_path = 'similarity.pkl'

if not os.path.exists(similarity_file_path):
    st.write("Downloading similarity.pkl from Google Drive...")
    download_file_from_google_drive(similarity_file_id, similarity_file_path)
else:
    st.write("Found similarity.pkl, loading it...")

# Attempt to load the similarity matrix
try:
    similarity = pickle.load(open(similarity_file_path, 'rb'))
except Exception as e:
    st.error(f"Error loading similarity matrix: {e}")

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
share_url = f'https://drive.google.com/file/d/{similarity_file_id}/view?usp=sharing'
st.markdown(f"Access the file via this [Google Drive link]({share_url})")s
