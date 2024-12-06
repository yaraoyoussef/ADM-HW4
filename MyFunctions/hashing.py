import random
import numpy as np 
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, f1_score

''' 
Defining multiple hash functions to experiment 
'''

''' Simple hash function '''
def simple_hash(x, a, b, p):
    return (a * x + b) % p

''' Polynomial Hash Function '''
def polynomial_hash(x, a, b, p):
    return (x**2 + a * x + b) % p

''' Xor Hash Function '''
def xor_hash(x, a, b, p):
    return x ^ (a + b)

'''
This function will hash each user's watched movie list, creating a representation 
that allows for quick comparisons of user similarities.
It takes in input the dictionary of 'user : [movies]' pairs, the number of hashes applied, and
the hash function to apply, and it returns a dictionary of signatures associated to each user.
We use precomputing for efficiency purposes.
'''
def minhash(user_movies, num_hashes, selected_hash):
    signatures = {}
    # Prime number for hash modulus. Large to prevent hash collisions 
    p = 26749 
    # Get the set of all unique movies
    all_movies = set(movie for movies in user_movies.values() for movie in movies)
    # Precompute all the coefficients (a and b) for the hashes
    coefficients = [(random.randint(1, len(all_movies)), random.randint(0, len(all_movies))) for _ in range(num_hashes)]
    # Precompute the hash functions
    hash_functions = [lambda x, a=a, b=b, p=p: selected_hash(x, a, b, p) for a, b in coefficients]

    # For each user
    for user, movies in user_movies.items():
        # convert to np array for efficiency
        movies = np.array(list(movies))
        # Initialize a signature vector with infinity values
        signature = np.full(num_hashes, float('inf'))
        # For each movie rated by the user
        for i, hash_fn in enumerate(hash_functions):
            # Apply the hash function to all movies
            hash_values = hash_fn(movies)
            # Update the signature with the smallest hash value
            signature[i] = np.min(hash_values)
        # Store the user's signature
        signatures[user] = signature.tolist()
    
    return signatures 

'''
Computes the Jaccard Similarity between two signatures
'''
def jaccard_similarity(sig1, sig2):
    matches = sum(1 for h1, h2 in zip(sig1, sig2) if h1 == h2)
    return matches / float(len(sig1))

''' 
Computes the real jaccard similarity between 2 movie lists of different users
'''
def real_jaccard_similarity(movie_list1, movie_list2):
    movies1 = set(movie_list1)
    movies2 = set(movie_list2)

    # Calculate Jaccard Similarity
    intersection = len(movies1.intersection(movies2))
    union = len(movies1.union(movies2))
    similarity = intersection / union
    return similarity

''' 
This function evaluates how well different hash functions predict user similarity using MinHash signatures.
For a sampled subset of users, compute:
    - Real Jaccard similarity (using movie lists).
    - Predicted similarity (using MinHash signatures).
For each similarity threshold, classify pairs as similar (`1`) or not (`0`).
We calculate:
    - Accuracy: Overall correctness.
    - Precision: Correct similar predictions.
    - F1 Score: Balance between precision and recall.
Returns a DataFrame summarizing each hash function's performance across thresholds.
The purpose of this function is identifing the best hash function and threshold for 
accurate user similarity predictions.
'''
def evaluate_hashes(user_movies, hash_funcs, thresholds, sample_size):
    results = []

    # For each hash function we created and its corrisponding signature we calculated
    for hash_func, signatures in hash_funcs.items():
        print(f"Testing Hash Function: {hash_func}")

        # Sample a subset of users
        user_ids = random.sample(list(signatures.keys()), sample_size)
        num_users = len(user_ids)
        # to store real jaccard similarities and predicted ones
        y_true = []
        y_pred = []
        
        # Calculate the real jaccard similarity and the predicted one for each pair of users
        for i in range(num_users):
            for j in range(i + 1, num_users):
                user1 = user_ids[i]
                user2 = user_ids[j]
                # real similarity
                real_sim = real_jaccard_similarity(user_movies[user1], user_movies[user2])
                # predicted similarity
                similarity = jaccard_similarity(signatures[user1], signatures[user2])
                # storing 
                y_true.append(real_sim)
                y_pred.append(similarity)

        # Iterate over thresholds
        for threshold in thresholds:
            # Predict similar user pairs based on the threshold

            # Giving 1 if similarity is above threshold, 0 otherwise
            y_true_full = [1 if true >= threshold else 0 for true in y_true]
            y_pred_full = [1 if pred >= threshold else 0 for pred in y_pred]
            
            # evaluate using accuracy, precision and f1 score
            accuracy = accuracy_score(y_true_full, y_pred_full)
            precision = precision_score(y_true_full, y_pred_full, zero_division=1)
            f1 = f1_score(y_true_full, y_pred_full, zero_division=1)

            # Store results
            results.append({
                "Hash function": hash_func,
                "Threshold": threshold,
                "Accuracy": accuracy,
                "Precision": precision,
                "F1 Score": f1,
            })
    # return df for visualisation purposes
    return pd.DataFrame(results)
