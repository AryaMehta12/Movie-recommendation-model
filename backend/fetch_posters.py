import pandas as pd
import requests
import time
import json
from tqdm import tqdm

# Your TMDB API key
TMDB_API_KEY = "0c9875e91d7175df2c867f39b9750c37"  # Replace with your actual key

def fetch_poster_url(tmdb_id):
    # In your fetch_poster_url loop
    time.sleep(1.2)  # Safer: 3.3 requests/sec

    """Fetch poster URL for a single movie ID"""
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}&language=en-US"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            poster_path = data.get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
        elif resp.status_code == 404:
            print(f"Movie ID {tmdb_id} not found on TMDB")
        else:
            print(f"API Error {resp.status_code} for movie ID {tmdb_id}")
        return None
    except Exception as e:
        print(f"Exception for movie ID {tmdb_id}: {e}")
        return None

def main():
    # Load your processed data
    print("Loading movie data...")
    df = pd.read_csv('Processed_data.csv')
    
    # Get unique movie IDs
    unique_ids = df['id'].unique()
    print(f"Found {len(unique_ids)} unique movie IDs")
    
    # Dictionary to store results
    poster_urls = {}
    
    # Fetch poster URLs with progress bar
    print("Fetching poster URLs from TMDB...")
    for tmdb_id in tqdm(unique_ids, desc="Fetching posters"):
        poster_url = fetch_poster_url(tmdb_id)
        poster_urls[int(tmdb_id)] = poster_url
        
        # Rate limiting: TMDB allows 40 requests per 10 seconds
        time.sleep(0.26)  # ~3.8 requests per second to be safe
    
    # Save results to JSON file
    print("Saving poster URLs...")
    with open('poster_urls.json', 'w') as f:
        json.dump(poster_urls, f, indent=2)
    
    # Also save as CSV for easy viewing
    poster_df = pd.DataFrame([
        {'tmdb_id': tmdb_id, 'poster_url': url} 
        for tmdb_id, url in poster_urls.items()
    ])
    poster_df.to_csv('poster_urls.csv', index=False)
    
    # Print summary
    total_movies = len(poster_urls)
    movies_with_posters = sum(1 for url in poster_urls.values() if url is not None)
    movies_without_posters = total_movies - movies_with_posters
    
    print(f"\n=== SUMMARY ===")
    print(f"Total movies: {total_movies}")
    print(f"Movies with posters: {movies_with_posters}")
    print(f"Movies without posters: {movies_without_posters}")
    print(f"Success rate: {(movies_with_posters/total_movies)*100:.1f}%")
    print(f"\nSaved to: poster_urls.json and poster_urls.csv")

if __name__ == "__main__":
    main()
