import random
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

    # For each user
    for user in user_movies:
         # Initialize a signature vector with infinity values
        signature = [float('inf')] * num_hashes
         # For each movie rated by the user
        for movie in user_movies[user]:
            # For each hash function
            for i in range(num_hashes):
                a = random.randint(1, 100)
                b = random.randint(1, 100)
                # Hash the movie ID using
                hash_value = selected_hash(movie, a, b, p)
                 # Update the signature with the smallest hash value
                signature[i] = min(signature[i], hash_value)
        # Store the MinHash signature for the current user in the dictionary
        signatures[user] = signature
    
    return signatures