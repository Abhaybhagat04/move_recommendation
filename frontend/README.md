# Movie Recommendation System - Frontend

This is the Streamlit-based web frontend for the Movie Recommendation System.

## Features
- **Interactive UI**: A sleek, dark-themed web interface built using Streamlit.
- **Dynamic Recommendations**: Select a movie from the dropdown, and it immediately calculates and displays the top 5 most similar movies.
- **TMDB API Integration**: Automatically fetches the official high-resolution movie posters for the recommended movies.
- **Resilient**: Includes built-in connection retry mechanisms and fallback placeholder images if posters are unavailable.

## Setup Instructions

### Prerequisites
1. You must have already run the data preprocessing script to generate the models.
   From the root project folder, run:
   ```bash
   python preprocessing/cleaning.py
   ```
   This generates `movie_dict.pkl` and `similarity.pkl` in the root folder.

2. **API Key Setup**:
   You need a free TMDB API key to fetch posters. 
   - Get your API key from [The Movie Database (TMDB)](https://www.themoviedb.org/)
   - Open the `.env` file located in this `frontend` directory.
   - Replace the placeholder with your actual API key:
     ```
     TMDB_API_KEY="your_actual_key_here"
     ```

### Running the App
1. Install the required dependencies from the root directory:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Streamlit app:
   ```bash
   streamlit run frontend/app.py
   ```
3. Open your browser and navigate to `http://localhost:8501`.
