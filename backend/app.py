from flask import Flask, request, jsonify
from flask_cors import CORS 
import pandas as pd
import numpy as np
import pickle
import requests
import time
from functools import lru_cache
TMDB_API_KEY = '0c9875e91d7175df2c867f39b9750c37'

app = Flask(__name__)
CORS(app)  
# Load the processed dataset
df = pd.read_csv('Processed_data.csv')
similarity = np.loadtxt('similarity_matrix.csv', delimiter=',')
# Helper: case-insensitive search for movie index


def get_movie_index(title):
    title = title.lower()
    matches = df[df['title'].str.lower() == title]
    return matches.index[0] if not matches.empty else None

# Endpoint: List all titles/ids for autocomplete


import time
import random

@lru_cache(maxsize=1000)  # Cache results to avoid repeated API calls

def get_poster_url(tmdb_id, max_attempts=3):
    """Fetch poster URL with retry logic"""
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}&language=en-US"
    
    for attempt in range(max_attempts):
        try:
            # Add random delay to avoid rate limits
            time.sleep(0.8 + random.uniform(0, 0.7))
            
            resp = requests.get(url, timeout=8)
            if resp.status_code == 200:
                data = resp.json()
                poster_path = data.get("poster_path")
                if poster_path:
                    return f"https://image.tmdb.org/t/p/w500{poster_path}"
                else:
                    return None  # No poster available
            elif resp.status_code == 404:
                return None  # Movie not found
            else:
                print(f"TMDB API error {resp.status_code} for ID {tmdb_id}, attempt {attempt + 1}")
                
        except Exception as e:
            print(f"Exception for ID {tmdb_id}, attempt {attempt + 1}: {e}")
            if attempt < max_attempts - 1:  # Don't sleep on last attempt
                time.sleep(2 + random.uniform(0, 2))  # Extra wait after error
    
    print(f"Failed to get poster for ID {tmdb_id} after {max_attempts} attempts")
    return None


@app.route('/movies', methods=['GET'])
def movies():
    movies_list = [{'title': row['title'], 'id': row['id']}
                   for _, row in df.iterrows()]
    return jsonify(movies_list)

# Endpoint: Get recommendations for a given movie (title)


@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    title = data.get('title', '')
    idx = get_movie_index(title)
    if idx is None:
        return jsonify({'error': 'Movie not found'}), 404

    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    top_movies = []
    for i in scores[1:11]:
        movie_row = df.iloc[i[0]]
        top_movies.append({
            'title': str(movie_row['title']),
            'id': int(movie_row['id']),
            'poster_url': get_poster_url(int(movie_row['id']))
        })
    return jsonify(top_movies)



if __name__ == '__main__':
    app.run(debug=True)
