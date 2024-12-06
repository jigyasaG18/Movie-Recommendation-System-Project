import pickle
import streamlit as st
import requests
import os

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data.get('poster_path')
    if poster_path is not None:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    return None

# Function for movie recommendations
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # Fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Function to download the similarity.pkl file from Google Drive
def download_file_from_google_drive(file_id, destination):
    URL = f"https://drive.google.com/uc?id={file_id}"  # Direct download URL
    response = requests.get(URL)
    
    if response.status_code == 200:
        with open(destination, 'wb') as f:
            f.write(response.content)
    else:
        st.error("Failed to download file from Google Drive. Please check the link or file ID.")

# Streamlit App Layout
st.header('Movie Recommender System')

# Load movies from the pickle file
movies = pickle.load(open('movie_list.pkl', 'rb'))

# Define the Google Drive file ID for the similarity.pkl file
similarity_file_id = '1_UlR2lx89WlIdUjAgsdxXZo20QJ7WyqP'  # Replace with your own file ID
similarity_file_path = 'similarity.pkl'

# Check if the similarity file exists, if not, download it
if not os.path.exists(similarity_file_path):
    st.write("Downloading similarity.pkl file from Google Drive...")
    download_file_from_google_drive(similarity_file_id, similarity_file_path)

# Load the similarity matrix
try:
    similarity = pickle.load(open(similarity_file_path, 'rb'))
except Exception as e:
    st.error(f"Error loading similarity matrix: {e}")
    st.stop()  # Stop the app if the loading fails

# Movie selection dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Show recommendations when the button is clicked
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Display recommended movie posters
    cols = st.columns(5)  # Create 5 columns for displaying movies
    for i in range(5):
        with cols[i]:
            if recommended_movie_posters[i]:  # Check if poster exists
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])
            else:
                st.text(recommended_movie_names[i])
                st.text("Poster not available")  # Handle missing poster gracefully
