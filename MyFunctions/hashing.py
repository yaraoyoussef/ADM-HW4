import random
import numpy as np 
''' 
Defining multiple hash functions to experiment 
'''

""" Simple haash function """
def simple_hash(x, a, b, p):
    return (a * x + b) % p

""" Polynomial Hash Function """
def polynomial_hash(x, a, b, p):
    return (x**2 + a * x + b) % p

""" Multiplicative Hash Function """
def multiplicative_hash(x, a, b, p):
    return (a * x) % p

'''
This function will hash each user's watched movie list, creating a representation 
that allows for quick comparisons of user similarities.
the variable 'num_hashes' allows us to experiment with different numbers of hash functions 
'''

def minhash(user_movies, num_hashes, selected_hash):
    signatures = {}
    # Prime number for hash modulus. Large to prevent hash collisions 
    p = 9999991  
    coefficients = [(random.randint(1, 100), random.randint(0, 100)) for _ in range(num_hashes)]
    hash_functions = [lambda x, a=a, b=b, p=p: selected_hash(x, a, b, p) for a, b in coefficients]

    # For each user
    for user, movies in user_movies.items():
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
