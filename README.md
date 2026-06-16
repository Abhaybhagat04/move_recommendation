# Movie Recommendation System

This project is a content-based movie recommendation system built in Python. It recommends movies similar to a user's favorite movie by analyzing textual metadata such as genres, keywords, cast, crew, and plot overviews.

## Overview
The system uses the **TMDB 5000 Movie Dataset**. It processes the raw dataset to extract the most meaningful attributes, creates a comprehensive "tag" (a descriptive paragraph) for each movie, and utilizes Natural Language Processing (NLP) techniques to compute similarities between movies.

## How It Works

The entire pipeline is visible in `preprocessing/cleaning.py`:

1. **Data Cleaning & Merging**: Merges the `movies` and `credits` datasets on the movie title.
2. **Feature Extraction**: Extracts the names of genres, keywords, the top 3 actors, and the director from JSON-like strings.
3. **Data Preprocessing**: Removes spaces from names (to prevent distinct concepts like "Science Fiction" and "Science" from overlapping confusingly) and concatenates all text features into a single `tag`.
4. **Stemming**: Reduces words to their base root using NLTK's `PorterStemmer` (e.g., 'actions' and 'action' both become 'action').
5. **Vectorization**: Uses scikit-learn's `CountVectorizer` to convert the text tags into mathematical vectors (Bag of Words technique).
6. **Cosine Similarity**: Calculates the cosine angle between vectors to determine how similar any two movies are to one another.

## Setup and Usage

1. **Install Dependencies**
   Ensure you have the required libraries installed:
   ```bash
   pip install pandas numpy scikit-learn nltk
   ```

2. **Run the Script**
   To see the recommendation script in action (by default it prints top 5 recommendations for 'Batman Begins'), run:
   ```bash
   python preprocessing/cleaning.py
   ```
