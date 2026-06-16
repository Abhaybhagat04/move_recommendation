import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# 1. Load the datasets
movie = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")

# 2. Merge both datasets on the 'title' column
movie = movie.merge(credits, on="title")

# 3. Select only the features we need for our recommendation system
movie = movie[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# 4. Remove any rows that have missing values (nulls)
movie.dropna(inplace=True)

# Helper function to extract names from JSON-like strings
def convert(obj):
    """
    Parses a stringified list of dictionaries (like genres or keywords) 
    and extracts the 'name' attribute from each dictionary.
    """
    l = []
    # ast.literal_eval safely parses a string into a Python list/dict
    for i in ast.literal_eval(obj):
        l.append(i["name"])
    return l    

# Apply the helper function to extract genre and keyword names
movie['genres'] = movie['genres'].apply(convert)
movie['keywords'] = movie['keywords'].apply(convert)

# Helper function to extract only the top 3 actors from the cast list
def convert3(obj):
    """
    Parses the cast list and extracts the names of the top 3 actors/actresses.
    """
    l = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            l.append(i["name"])
            counter += 1
        else:
            break    
    return l

movie['cast'] = movie['cast'].apply(convert3)

# Helper function to extract the Director's name from the crew list
def fetch_director(obj):
    """
    Iterates through the crew list and returns the name of the individual
    whose job is marked as 'Director'.
    """
    l = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            l.append(i['name'])
            break
    return l

movie['crew'] = movie['crew'].apply(fetch_director)

# Split the overview text into a list of individual words
movie['overview'] = movie['overview'].apply(lambda x: x.split())

# Remove spaces inside names/genres (so 'Science Fiction' becomes 'ScienceFiction')
# This ensures that our vectorizer treats it as a single unique entity
movie['genres'] = movie['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movie['keywords'] = movie['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movie['cast'] = movie['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movie['crew'] = movie['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

# 5. Create a new 'tag' column by combining overview, genres, keywords, cast, and crew
movie['tag'] = movie['overview'] + movie['genres'] + movie['keywords'] + movie['crew']

# Create a new dataframe containing only the essential columns
new_df = movie[['movie_id', 'title', 'tag']]

# Join the list of tags back into a single string for each movie
new_df['tag'] = new_df['tag'].apply(lambda x: " ".join(x))

# Convert all tags to lowercase to ensure consistency
new_df['tag'] = new_df['tag'].apply(lambda x: x.lower())

# Initialize the Stemmer (this reduces words to their root form, e.g., 'running' -> 'run')
ps = PorterStemmer()

def stem(text):
    """
    Applies the PorterStemmer algorithm to reduce each word in the text 
    to its root form (e.g., 'running' becomes 'run').
    """
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)    

# Apply stemming to the tags
new_df['tag'] = new_df['tag'].apply(stem)

# 6. Vectorize the tags using Bag of Words strategy
cv = CountVectorizer(max_features=5000, stop_words='english')
vactor = cv.fit_transform(new_df['tag']).toarray()

# 7. Calculate Cosine Similarity between all movie vectors
similarity = cosine_similarity(vactor)

# 8. Recommendation Function
def recommend(movie):
    # Convert input to lowercase to make the search case-insensitive
    movie = movie.lower()
    matches = new_df[new_df['title'].str.lower() == movie]
    
    # If the movie isn't in our dataset, exit gracefully
    if matches.empty:
        print(f"Movie '{movie}' not found in the dataset.")
        return
        
    # Get the index of the requested movie
    movie_index = matches.index[0]
    
    # Get the distances (similarity scores) for this specific movie
    distances = similarity[movie_index]
    
    # Sort the movies based on similarity score (highest first), excluding itself (index 0)
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    # Print the top 5 recommendations
    for i in movie_list:
        print(new_df.iloc[i[0]].title)

# Example Usage
# recommend('batman Begins')

# 9. Export Models for Frontend
# Save the dataframe as a dictionary so it can be loaded easily in Streamlit
pickle.dump(new_df.to_dict(), open('movie_dict.pkl', 'wb'))
# Save the similarity matrix
pickle.dump(similarity, open('similarity.pkl', 'wb'))