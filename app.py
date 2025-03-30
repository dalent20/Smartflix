#imports
import streamlit as st
import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
import os 
from fuzzywuzzy import process





#page layout configuration, and browser tab icon
st.set_page_config(
    page_title= "🎬SmartFlix",
    page_icon= "🎥",
    layout="wide"
)
#TMDB API Key
TMDB_API_KEY = "12a8204a8054371bf7bac3921f771f5f"

# function to search for TMDb for a movie poster
import requests





#make a cleaner title
def clean_title_for_tmdb(title):
    #remove the year if present
    title= title.split("(")[0]
    #reformat "empire strikes back, the" to "the empire strikes back"
    if ", The" in title:
        title= "The" + title.replace(",The", "")
    if ", A" in title:
        title="A " + title.replace(", A", "")
    if ",An" in title:
        title = "An" + title.replace(",An", "")
    
    return title.strip()





def fetch_movie_info(title):
    try:
        cleaned_title= clean_title_for_tmdb(title)

        #search tmdb for movie, edited to search for all titles
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={cleaned_title}"
        response = requests.get(url)
        data = response.json()

        if data["results"]:
            result= data["results"][0]
            poster_path = result.get("poster_path")
            rating= result.get("vote_average", None)
            release_date= result.get("release_date", "")
            release_year= str(release_date)[:4] if release_date else "N/A"

            movie_id= result.get("id")
            #fetch genres from details endpoint
            details_url= f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
            details_response= requests.get(details_url)
            details_data= details_response.json()
            genre_names= [g["name"] for g in details_data.get("genres", [])]
            genres= ", ".join(genre_names) if genre_names else "N/A"



            poster_url = (
                f"https://image.tmdb.org/t/p/w500{poster_path}"
                if poster_path
                else "https://via.placeholder.com/300x450?text=No+Poster"
            )
            print(f"DEBUG: {title} | Poster: {poster_url} | Year: {release_year} | Genres: {genres}")
            return poster_url, rating, release_year, genres
                
        
    except:
        pass

    #if no poster found, return a placeholder
    return "https://via.placeholder.com/300x450?text=No+Poster", None, "N/A", "N/A"





#===load data===
@st.cache_data
def load_data():
    #load ratings
    ratings= pd.read_csv("u.data", sep="\t", names= ["user_id", "movie_id", "rating", "timestamp"])
    movies= pd.read_csv("u.item", sep= "|" , names= ["movie_id", "title"], usecols= [0,1], encoding="latin-1")
    data= pd.merge(ratings.drop("timestamp", axis=1), movies, on="movie_id")

    #create pivot table
    matrix= data.pivot_table(index="title", columns="user_id", values= "rating").fillna(0)

    #compute similarity
    sim_matrix= cosine_similarity(matrix)
    sim_df = pd.DataFrame(sim_matrix, index=matrix.index,columns=matrix.index)

    return sim_df
similarity_df = load_data()



# ====App UI====
st.title("SmartFlix -Ai Movie Recommender")



#for some padding
st.markdown("### What movies do you like?")
st.caption("Enter up to 3 titles (e.g., *Pulp Fiction, Toy Story, Jurassic Park*)")

user_input = st.text_input("Enter 1-3 movies you like(comma-sepreated):", "")



#Sliders
num_recs= st.slider("How many recommendations would you like?", min_value=3, max_value=15,value=5)
high_rating_only = st.checkbox("Only show movies rated 7.0 or higher")



st.markdown("---")




if user_input:
    movie_list = [m.strip() for m in user_input.split(',')]
    #movie matching loop with fuzzywuzzy title mispells
    matched=[]
    all_titles= similarity_df.columns.tolist()

    for m in movie_list:
        best_match, score= process.extractOne(m, all_titles)
        if score > 60: #threshold can be adjusted as needed
            matched.append(best_match)




#no movies found display
    if not matched:
        st.error(" We couldn't find any of those movies. Double check spelling or try something more popular!")
    else:
        combined_scores= similarity_df[matched].mean(axis=1)
        for title in matched:
             combined_scores= combined_scores.drop(title, errors="ignore")
        
        top_recs= combined_scores.sort_values(ascending=False).head(num_recs)

        if top_recs.empty:
             st.warning("No recommendations found based on those titles.")
        else:
             st.subheader("Because you liked " + " , ".join(matched))

        #new display loop
        st.markdown("### Top Recommendations")
        st.markdown("") #tiny spacing

        column_count= 5
        cols= st.columns(column_count)
        
        with st.spinner("fetching recommendations..."):
            for idx, (title, score) in enumerate(top_recs.items()):
                with cols[idx%column_count]: # loop through 5 columns
                     poster_url,avg_rating, release_year, genres = fetch_movie_info(title)
                     #Apply the rating filter
                     if high_rating_only and (avg_rating is None or avg_rating <7.0):
                         continue



                     if "placeholder" in poster_url:
                         #fallback logic if no poster
                         rating_display = f"{avg_rating: .1f}" if avg_rating is not None else "N/A"
                         print(f"DEBUG DISPLAY CHECK (fallback): {title} | avg_rating: {avg_rating} display: {rating_display}")
                         genre_display = genres if genres and genres != "N/A" else "Genre: N/A"
                         year_display = release_year if release_year and release_year != "N/A" else "Year: N/A"

                         st.image(poster_url, use_container_width=True)
                         st.markdown(f"**{title}**")
                         st.caption(f"{genre_display} | {year_display}")
                         st.caption(f"Similarity Score: `{score: .3f}` | Rating: {rating_display}")




                     else:
                         #to check for errors in the rating display 
                         rating_display= f"{avg_rating:.1f}" if avg_rating is not None else "N/A"
                         print(f"{title} TMDb Rating: {avg_rating} Display: {rating_display}")
                         #custom HTML Block for title for score overlay
                         print(f"DEBUG DISPLAY CHECK (poster): {title} | avg_rating: {avg_rating} display: {rating_display}")

                         html= f"""
                         <div style = "position: relative; text-align: center; color: white;">
                            <img src="{poster_url}" style= "width: 100%; border-radius:10px;">
                            <div style="
                                position: absolute;
                                bottom: 0;
                                left: 0;
                                right: 0;
                                padding: 8px;
                                background: linear-gradient(to top, rgba(0,0,0,0.85), rgba(0,0,0,0));
                                border-bottom-left-radius:10px;
                                border-bottom-right-radius:10px;
                                font-weight: 600;
                                font-size: 14px;
                                color: white;
                            ">
                                {title}<br>
                                <span style= "font-size:13px; color: #ccc;">{genres} | {release_year}</span><br>
                                <span style="font-size:13px; color: #ccc;">Similarity: {score: .3f} | Rating: {rating_display}</span>
                            </div>
                        </div>
                         """
                         st.markdown(html, unsafe_allow_html=True)
