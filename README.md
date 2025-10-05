# Movie Recommendation Model

A full-stack, content-based movie recommendation system with poster images, built using Python, Flask, React, and TMDb API. The core logic is based on processing the TMDB 5000 Movies dataset and providing instant recommendations with a modern, interactive UI.

---

##  Features

- **Content-Based Recommendations:** Suggests similar movies using NLP and vectorization of genres, overview, keywords, cast, and crew.
- **TMDb Poster Fetching:** Displays high-quality posters for recommended movies via TMDb API.
- **Modern Web UI:** React SPA with autocomplete movie search, styled results, and error handling.
- **Large Dataset Support:** Efficient processing with large files handled by Git LFS.
- **Exported Similarity Matrix:** Saves similarity data as CSV for scalability.
- **API-Driven:** Flask REST API for frontend-backend separation and easy deployment.

---
##  Sample Images

<img width="1513" height="959" alt="image" src="https://github.com/user-attachments/assets/da7c7c7d-c7c8-46e6-802b-f1bd2f1ca770" />

<img width="1696" height="949" alt="image" src="https://github.com/user-attachments/assets/38b41740-ee8d-40d4-8b63-079485a4e13b" />

<img width="1549" height="948" alt="image" src="https://github.com/user-attachments/assets/0eb6a241-5a9b-40ca-8190-02b8e4539dcd" />

<img width="1912" height="951" alt="image" src="https://github.com/user-attachments/assets/21833e0a-5c5f-4c56-8c57-744731f9a3d6" />


---
## 🗂️ Repository Structure

Movie-recommendation-model/
│
├── Data_preprocess/
│ └── recommendation_model.ipynb # Data cleaning, feature engineering, similarity matrix
│
├── backend/
│ ├── app.py # Flask API: recommends movies, fetches posters
│ ├── fetch_posters.py # Script to fetch/save all poster URLs from TMDb
│ ├── requirements.txt # Python backend dependencies
│
├── frontend/
│ └── src/
│ └── App.jsx # React app, search/recommend UI
│
├── .gitattributes # Configured for Git LFS (large files)
└── ... # Processed data & similarity matrix (CSV)

---

## 🛠️ Tech Stack

- **Python, Pandas, NumPy, scikit-learn**: Data handling, NLP, vectorization
- **Flask**: Lightweight backend API
- **React**: Frontend SPA interface
- **requests**: API interaction with TMDb
- **TMDb API**: Posters, extra movie info
- **Git LFS**: Handles large processed files (CSV, similarity matrix)

---

## 📦 Setup Guide

### 1. Clone repo and install prerequisites

git clone https://github.com/AryaMehta12/Movie-recommendation-model.git
cd Movie-recommendation-model

Ensure Git LFS is installed and initialized
git lfs install
git lfs pull

### 2. Setup Backend

cd backend
pip install -r requirements.txt

Download TMDB 5000 Movies dataset into Data_preprocess/
Run recommendation_model.ipynb (Jupyter) to generate Processed_data.csv and similarity_matrix.csv
(Optional) Fetch and cache poster URLs using fetch_posters.py
python app.py # Runs Flask backend server at http://localhost:5000


### 3. Setup Frontend

cd ../frontend
npm install
npm start # Runs React app at http://localhost:3000

---

## ⚙️ How It Works

- Cleans and merges movie and credit CSVs, extracts genres, keywords, top 5 cast, and main director for each movie.
- Combines these features into a 'tags' column, processes with CountVectorizer for textual features.
- Calculates cosine similarity across all movies, saving the similarity matrix for fast lookup.
- Flask backend provides endpoints:
    - `/movies` – List of available titles/IDs
    - `/recommend` – Get top N recommendations with posters for a given movie
- Poster fetching handled robustly with rate-limiting using TMDb API.
- React frontend allows users to search, select a movie, and view instant posterized recommendations.

---

## 📝 Example Use

- Type a movie’s name in the search box.
- Select a movie from suggestions.
- See 10 most similar movies with posters, titles, and IDs.

---

## 🧩 Key Implementation Notes

- **Serialization & Efficiency:** Similarity matrix and processed data stored as CSV to minimize recomputation and RAM use.
- **Poster Fetching:** Custom scripts to build poster URL cache, minimizes API hits when serving recommendations.
- **Error Handling:** Frontend and backend both return informative messages for missing movies or posters.
- **Extendability:** Code and file structure designed to accommodate collaborative, hybrid, or ML-based future upgrades (item/user collaborative filtering, etc.).

---

## 📃 Credits and Acknowledgments

- Movie metadata: TMDb 5000 Movie Dataset.
- Posters & additional info: [TMDb API](https://www.themoviedb.org/documentation/api).
- Full-stack structure inspired by best practices for ML productization.

---

## 🙋 Contributing

Feel free to fork, file issues, or open pull requests! For major changes or questions, please contact Arya Mehta.

---

## 🏁 License

This project is MIT-licensed and uses the TMDb API under its terms of use.

---
