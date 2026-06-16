import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Load environment variables
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(env_path)
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Add some custom CSS for aesthetics
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .poster-img {
        border-radius: 10px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.5);
        transition: 0.3s;
    }
    .poster-img:hover {
        box-shadow: 0 8px 16px 0 rgba(255,255,255,0.2);
        transform: scale(1.02);
    }
    h1 {
        color: #E50914;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        margin-bottom: 2rem;
    }
    .movie-title {
        text-align: center;
        font-weight: bold;
        margin-top: 10px;
        font-size: 1.1rem;
        min-height: 50px;
    }
</style>
""", unsafe_allow_html=True)

import time

def fetch_poster(movie_id):
    """
    Fetches the movie poster URL from TMDB API using the movie ID.
    Implements a retry mechanism (up to 3 times) to handle intermittent connection issues.
    Returns a placeholder image URL if the API key is missing or the request fails.
    """
    if not TMDB_API_KEY or TMDB_API_KEY == 'your_api_key_here':
        return "https://dummyimage.com/500x750/cccccc/000000.jpg&text=No+API+Key"
    
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            if 'poster_path' in data and data['poster_path']:
                return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
            break # if successful but no poster, don't retry
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for movie {movie_id}: {e}")
            time.sleep(1) # wait before retrying
            
    return "https://dummyimage.com/500x750/cccccc/000000.jpg&text=No+Poster"

def recommend(movie):
    """
    Given a movie title, finds the top 5 most similar movies based on the pre-computed 
    cosine similarity matrix. Returns a tuple containing a list of recommended movie 
    titles and a list of their corresponding poster URLs.
    """
    try:
        # Find the index of the selected movie in the dataframe
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = []
        recommended_movies_posters = []
        
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            # fetch poster from API
            recommended_movies_posters.append(fetch_poster(movie_id))
            
        return recommended_movies, recommended_movies_posters
    except Exception as e:
        st.error(f"Error during recommendation: {e}")
        return [], []

st.title('🎬 Movie Recommender System')

try:
    # Load data
    # Navigate up one directory since the app is in frontend/ and pickles might be in root
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dict_path = os.path.join(base_path, 'movie_dict.pkl')
    sim_path = os.path.join(base_path, 'similarity.pkl')
    
    if not os.path.exists(dict_path) or not os.path.exists(sim_path):
        st.warning("Model files not found! Please run `python preprocessing/cleaning.py` first to generate `movie_dict.pkl` and `similarity.pkl`.")
        st.stop()
        
    movies_dict = pickle.load(open(dict_path, 'rb'))
    movies = pd.DataFrame(movies_dict)
    
    similarity = pickle.load(open(sim_path, 'rb'))
    
    selected_movie_name = st.selectbox(
        'Select a movie to get recommendations:',
        movies['title'].values
    )

    if st.button('Recommend 🚀'):
        with st.spinner('Fetching recommendations...'):
            names, posters = recommend(selected_movie_name)
            
            if names:
                cols = st.columns(5)
                for i in range(5):
                    with cols[i]:
                        st.markdown(f'<div class="movie-title">{names[i]}</div>', unsafe_allow_html=True)
                        st.markdown(f'<img src="{posters[i]}" class="poster-img" width="100%">', unsafe_allow_html=True)
                        
except Exception as e:
    st.error(f"Failed to load application data: {e}")
