import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load the ratings data
column_names = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_csv('u.data', sep='\t', names=column_names)

# Show the first 5 rows
print(ratings.head())

movie_columns= ['movie_id', 'title']
movies = pd.read_csv(
    'u.item',
    sep='|',
    names=movie_columns,
    usecols=[0, 1],
    encoding='latin-1'
)

print(movies.head())

data = pd.merge(ratings, movies, on='movie_id')

print(data.head())


#drop timestamp
data = data.drop('timestamp', axis =1)

#create pivot table with movies as rows and users as columns
movie_user_matrix = data.pivot_table(index= 'title', columns= 'user_id', values= 'rating')

#replace Nan with 0 so we can use matric for similarity
movie_user_matrix = movie_user_matrix.fillna(0)

#show the first 5 rows of the matrix
print(movie_user_matrix.head())

#compute cosine similarity between all movies
similarity_matrix = cosine_similarity(movie_user_matrix)
#convert similarity matrix back into a dataframe with movie titles as index & columns
similarity_df = pd.DataFrame(similarity_matrix, index=movie_user_matrix.index, columns=movie_user_matrix.index)

#show top 5 rows of the similarity matrix
print(similarity_df.head())

# old recommend_movies()
def recommend_movies(movie_title, num_recommendations=5):
    #try to match the input to an actual title(case-insensitive, partial match)
    matches = [title for title in similarity_df.columns if movie_title.lower() in title.lower()]
    if not matches:
        print("movie not found. Please Try again.")
        return
    #use the first matching title
    matched_title = matches[0]
    similarity_scores = similarity_df[matched_title]
    similar_movies = similarity_scores.sort_values(ascending=False)[1:num_recommendations+1]

    print(f"\Becuse you liked '{matched_title}', you might also like:\n")
    for title, score in similar_movies.items():
        print(f"{title} {score: .3f})")

#new recommend_movies()
def recommend_movies_from_list(movies_list, num_recommendations= 5):
    matched_titles = []
    #try to match each input title
    for user_input in movie_list:
        matches=[title for title in similarity_df.columns if user_input.lower() in title.lower()]
        if matches:
            matched_titles.append(matches[0])
        else:
            print(f"Movie not found: {user_input}")
        
    if not matched_titles:
        print("No valid movies found. Please try again.")
        return
    
    #Average the similarity scores for all the matched movies
    combined_scores = similarity_df[matched_titles].mean(axis=1)
    #Remove the input movies from the recommendations
    for title in matched_titles:
        combined_scores = combined_scores.drop(title, errors= 'ignore')

    #Get top N recommendations
    top_recommendations = combined_scores.sort_values(ascending=False). head(num_recommendations)

    print(f"\nBecause you liked: {','.join(matched_titles)}\nYou might also like:\n")
    for title, score in top_recommendations.items():
        print(f"{title} (Score: {score: .3f})")

#Ask the user for multiple movies, comma-seperated
user_input = input("\nEnter 1-3 movies you like (e.g. 'Toy Story, Pulp Fiction'):")
movie_list =[movie.strip() for movie in user_input.split(',')]
recommend_movies_from_list(movie_list)