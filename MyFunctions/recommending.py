import pandas as pd

'''
Prepares the movie rating data for the two most similar users given:
    top_similar_users: List of tuples containing most similar users (sorted) and their similarity scores.
    df: DataFrame containing movie ratings with columns 'userId', 'movieId', and 'rating'.
Returns:
    user1_dict: Dictionary of movieId -> rating for the first similar user.
    user2_dict: Dictionary of movieId -> rating for the second similar user.
'''
def prepare_user_data(top_similar_users, df):
    # Take the two most similar users
    user1 = top_similar_users[0][0]
    user2 = top_similar_users[1][0]

    # Get movie rating info for each user
    user1_list = df[df["userId"] == user1][["movieId", "rating"]]
    user2_list = df[df["userId"] == user2][["movieId", "rating"]]

    # Convert to dictionaries for easy lookup
    user1_dict = dict(zip(user1_list["movieId"], user1_list["rating"]))
    user2_dict = dict(zip(user2_list["movieId"], user2_list["rating"]))

    return user1_dict, user2_dict

'''
Recommends movies based on the ratings of the two most similar users.
If both similar users have rated a movie, recommend this movie based on the average rating.
If there are no commonly rated movies, recommend the top-rated movies of the most similar user.
It returns recommendations: List of tuples containing movie title and the average predicted rating.
'''
def recommend_movies(top_similar_users, df, user_id, top_k = 10):

    # Get the dictionaries containing for each user, the movieID with the given rating 
    user1_dict, user2_dict = prepare_user_data(top_similar_users, df)

    # Get the movies titles
    movie_titles = dict(zip(df["movieId"], df["title"]))

    # Find common movies for both users
    common_movies = set(user1_dict.keys()).intersection(user2_dict.keys())

    # Get the list of movies the user has already seen
    user_movies = set(df[df["userId"] == user_id]["movieId"])
    # Remove the movies the user already rated/watched from the recommendation system
    common_movies -= user_movies

    recommendations = []

    # if users have commonly rated movies
    if common_movies:
        # Take every movie in common movies
        for movie in common_movies:
            # Calculate the average rating
            avg_rating = (user1_dict[movie] + user2_dict[movie]) / 2
            recommendations.append((movie_titles[movie], avg_rating))
        # Sort from highest to lowest
        recommendations.sort(key = lambda x: x[1], reverse=True)

    # else return the top rated movies of the most similar user
    else:
        for movie_id, rating in user1_dict.items():
            recommendations.append((movie_titles[movie_id], rating))
            recommendations.sort(key= lambda x: x[1], reverse=True)
    return recommendations[:top_k]

'''
Generates a final recommendation list of movies with their predicted ratings in the following way:
    First we find the commonly rated movies. 
    IF WE HAVEN'T REACHED TOP_K MOVIES YET:
        Then we proceed with top rated movie from the most similar user.
        Then we proceed with top rated movie from the second most similar user.
        Then we proceed with top rated movies from the most similar user if needed.
This function takes in input the following:
    top_similar_users: List of tuples containing similar users and their similarity scores.
    df: DataFrame containing movie ratings.
    user_id: ID of the user to whom recommendations are being made.
    top_k: Number of top recommendations to return.
And returns:
    recommendations_df: DataFrame containing the top recommended movies with their titles and ratings.
    We decided not to reorder the recommendations based on score at the end in order to prioritize 
    movies recommended by both users over those recommended by only one. 
    This approach gives greater importance to movies that have the endorsement of both users.
'''
def final_recommendation(top_similar_users, df, user_id, top_k=5):

    # Get the dictionaries containing for each user, the movieID with the given rating 
    user1_dict, user2_dict = prepare_user_data(top_similar_users, df)

    # Get the movies titles
    movie_titles = dict(zip(df["movieId"], df["title"]))

    # Find common movies for both users
    common_movies = set(user1_dict.keys()).intersection(user2_dict.keys())

    # Get the list of movies the user has already seen
    user_movies = set(df[df["userId"] == user_id]["movieId"])
    # and remove it from recommendation system
    common_movies -= user_movies

    recommendations = []
    # For each movie in the commonly rated list of movies
    for movie in common_movies:
        # Calculate the average
        avg_rating = (user1_dict[movie] + user2_dict[movie]) / 2
        recommendations.append((movie_titles[movie], avg_rating))
    # Sort the list based on ratings
    recommendations.sort(key = lambda x: x[1], reverse=True)

    # If we found enough recommendations, return them with title
    if len(recommendations) >= top_k:
        recommendations = recommendations[:top_k]
        recommendations_df = pd.DataFrame(recommendations, columns=["title", "avg_rating"])
        return recommendations_df
    # If we havent reached top_k movies yet
    else:
        # Remove common movies already found for both users to avoid adding them again
        for movie in common_movies:
            user1_dict.pop(movie, None)
            user2_dict.pop(movie, None)

        # We take the highest rated movie from the first user
        highest_rated_movie1 = max(user1_dict, key=user1_dict.get)
        recommendations.append((movie_titles[highest_rated_movie1], user1_dict[highest_rated_movie1]))
        # Remove it from the first user's dictionary to avoid adding it again
        user1_dict.pop(highest_rated_movie1, None)

        # If we havent reached 5 movies yet, we take the highest rated movie from the second user
        if len(recommendations) < top_k:
            highest_rated_movie2 = max(user2_dict, key=user2_dict.get)
            recommendations.append((movie_titles[highest_rated_movie2], user2_dict[highest_rated_movie2]))
            # Remove it from the second user's dictionary to avoid adding it again
            user2_dict.pop(highest_rated_movie2, None)

        # If we havent reached 5 movies yet, we take the highest rated movies from the first user until 
        # reaching top_k movies
        while len(recommendations) < top_k:
            highest_rated_movie = max(user1_dict, key=user1_dict.get)
            recommendations.append((movie_titles[highest_rated_movie], user1_dict[highest_rated_movie]))
            # Remove it from the first user's dictionary to avoid adding it again
            user1_dict.pop(highest_rated_movie, None) 
        # Return a dataframe for better visualisation
        return pd.DataFrame(recommendations, columns=["title", "avg_rating"])