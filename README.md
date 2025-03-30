# 🎬 SmartFlix - AI Movie Recommender

SmartFlix is a personalized movie recommendation app powered by collaborative filtering and enhanced with fuzzy title matching and live data from the TMDb API. Users enter up to 3 favorite movies, and SmartFlix returns similar films — complete with posters, genres, release years, and similarity scores.

---

## 🚀 Features

- 🔍 **Fuzzy title matching** for user-friendly input (e.g., "jurasic park" still works!)
- 🤖 **Collaborative filtering** using cosine similarity from the MovieLens 100k dataset
- 🎨 **Clean, modern UI** built with Streamlit and responsive grid layout
- 🎥 **Live poster + rating fetching** from [TMDb](https://www.themoviedb.org/)
- 🎛️ **Controls & filters**: 
  - Number of recommendations (3–15)
  - Optional filter for movies with a TMDb rating ≥ 7.0
- ✅ Handles missing data gracefully

---

## 🛠️ Tech Stack

- Python 3.10+
- Streamlit
- Pandas
- scikit-learn
- fuzzywuzzy
- Requests
- MovieLens 100k Dataset (1997)
- TMDb API

---

## 💡 How to Run the App

1. Clone this repo and install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

3. The app will open in your browser.

✅ Make sure to [get a TMDb API key](https://www.themoviedb.org/settings/api) and paste it inside your `app.py`.

---

## 📸 Screenshots

> *(Optional: Insert a few screenshots of the app layout here)*

---

## 📚 Dataset & License Info

This project uses the [MovieLens 100k dataset](https://grouplens.org/datasets/movielens/) for educational, non-commercial purposes only.  
The full licensing and usage information is provided in the original `README` file included with the dataset, located in this repository.

> The original dataset and its README are included in this repo under the file `README`, provided by GroupLens Research, University of Minnesota.


---

## 🧠 Credits

Built by Dalen Tinsley as a hands-on AI recommendation project.  
Mentored and supported with guidance from OpenAI's ChatGPT.

---