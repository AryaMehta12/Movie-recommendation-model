import React, { useState, useEffect } from 'react';
import './App.css'; // We'll create this for styles

const BACKEND_URL = 'http://localhost:5000'; // Flask server

function Poster({ posterUrl, title }) {
  if (!posterUrl) {
    return (
      <div
        style={{
          width: 140,
          height: 210,
          borderRadius: 10,
          background: "linear-gradient(135deg, #212129 60%, #39315f 100%)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "#b3aaff",
          fontWeight: "bold",
          fontSize: "1rem",
          boxShadow: "0 0 28px #7c7fc6aa",
          textAlign: "center",
          border: "2px solid #36347077",
          letterSpacing: "0.02em"
        }}
      >
        No<br/>Poster
      </div>
    );
  }

  return (
    <img
      src={posterUrl}
      alt={title}
      style={{
        borderRadius: 10,
        width: 140,
        height: 210,
        boxShadow: "0 0 28px #7c7fc6aa",
        background: "#181622",
        objectFit: "cover"
      }}
      onError={e => {
        e.target.onerror = null;
        e.target.style.display = "none";
        // Show styled placeholder if error loading poster!
        const parent = e.target.parentNode;
        if (parent) {
          parent.innerHTML = `<div style="width:140px;height:210px;display:flex;align-items:center;justify-content:center;border-radius:10px;background:linear-gradient(135deg,#212129 60%,#39315f 100%);color:#b3aaff;font-weight:bold;font-size:1rem;box-shadow:0 0 28px #7c7fc6aa;text-align:center;border:2px solid #36347077;letter-spacing:0.02em;">No<br/>Poster</div>`;
        }
      }}
    />
  );
}


function App() {
  const [movies, setMovies] = useState([]);
  const [search, setSearch] = useState('');
  const [selectedMovie, setSelectedMovie] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Fetch movies for dropdown/autocomplete
  useEffect(() => {
    fetch(`${BACKEND_URL}/movies`)
      .then(res => res.json())
      .then(data => setMovies(data))
      .catch(err => console.error('Failed to fetch movies:', err));
  }, []);

  // Autocomplete suggestion filter (case-insensitive, top 10)
  useEffect(() => {
    if (!search) setSuggestions([]);
    else {
      setSuggestions(
        movies
          .filter(movie =>
            movie.title.toLowerCase().includes(search.toLowerCase())
          )
          .slice(0, 10)
      );
    }
  }, [search, movies]);

  // Submit search
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedMovie && !search) return;
    
    setLoading(true);
    setError('');
    setRecommendations([]);
    
    try {
      const response = await fetch(`${BACKEND_URL}/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: selectedMovie || search }),
      });
      
      if (!response.ok) {
        throw new Error('Movie not found or server error');
      }
      
      const recs = await response.json();
      setRecommendations(recs);
    } catch (err) {
      setError(`Failed to get recommendations: ${err.message}`);
      console.error('Recommend error:', err);
    }
    setLoading(false);
  };

  // When user clicks a suggestion
  const handleSuggestionClick = (title) => {
    setSelectedMovie(title);
    setSearch(title);
    setSuggestions([]);
  };

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1 className="title">
            <span className="title-gradient">Movie Recommender</span>
          </h1>
          <p className="subtitle">Discover your next favorite movie</p>
        </header>

        <div className="search-section">
          <form onSubmit={handleSubmit} className="search-form">
            <div className="input-container">
              <input
                type="text"
                value={search}
                onChange={e => { setSearch(e.target.value); setSelectedMovie(''); }}
                placeholder="Type a movie title..."
                className="search-input"
                autoComplete="off"
              />
              <button type="submit" className="search-button" disabled={loading}>
                {loading ? 'Searching...' : 'Recommend'}
              </button>
            </div>
            
            {suggestions.length > 0 && (
              <div className="suggestions">
                {suggestions.map(movie => (
                  <div
                    key={movie.id}
                    className="suggestion-item"
                    onClick={() => handleSuggestionClick(movie.title)}
                  >
                    {movie.title}
                  </div>
                ))}
              </div>
            )}
          </form>
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {recommendations.length > 0 && (
          <div className="results-section">
            <h2 className="results-title">Recommended Movies</h2>
            <div className="movies-grid">
              {recommendations.map((movie, index) => (
                <div key={movie.id} className="movie-card">
                  <div className="movie-number">{index + 1}</div>
                  <Poster posterUrl={movie.poster_url} />
                  <div className="movie-title">{movie.title}</div>
                  <div className="movie-id">ID: {movie.id}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
