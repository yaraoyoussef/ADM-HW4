import MyFunctions.clustering as clustering
import MyFunctions.hashing as hashing

''' 
Find users in the same bucket as the specified user given:
    user_id: The ID of the user whose neighbors are to be found.
    buckets: List of buckets from LSH, where each bucket maps band indices to user IDs.
The function returns a set of user IDs that are in the same bucket(s) as the given user, 
excluding the user itself.
'''
def find_users(user_id, buckets):
    similar_users = set()
    # Iterate through all bands' buckets
    for _, band_buckets in enumerate(buckets):
        # Iterate through buckets in each band
        for bucket_id, users in band_buckets.items():
            # Check if the current user is in the bucket
            if user_id in users:
                # Add all users in the bucket to the set
                similar_users.update(users)
    # Remove the original user from the set
    similar_users.discard(user_id)
    return similar_users

''' 
Rank similar users based on Jaccard similarity given:
    user_id: The ID of the current user.
    similar_users: A set of user IDs that are potential matches.
    minhash_signatures: Dictionary mapping user IDs to their MinHash signatures.
and returns a list of the top 2 users with the highest Jaccard similarity.
'''
def rank_similar_users(user_id, similar_users, minhash_signatures):
    # Retrieve current user's signature
    user_sig = minhash_signatures[user_id]
    similarities = []

    # Calculate Jaccard similarity between the current user and each similar user
    for user in similar_users:
        similarity = hashing.jaccard_similarity(user_sig, minhash_signatures[user])
        # Append user ID and similarity score as a tuple
        similarities.append((user, similarity))
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Return top 2 most similar users 
    return similarities[:2]

''' 
Handle cases where no similar users are found.
Args:
    user_id: The ID of the user whose neighbors are to be found.
    buckets: List of buckets from LSH, where each bucket maps band indices to user IDs.
    minhash_signatures: Dictionary mapping user IDs to their MinHash signatures.
    lsh_parameters: Dictionary containing LSH parameters (e.g., bands, rows_per_band, num_buckets).
    adjust_params_callback: Callback function to modify LSH parameters dynamically.
Returns:
    A list of the top similar users after adjusting LSH parameters.
'''
def similars_not_found(user_id, buckets, minhash_signatures, lsh_parameters, adjust_params_callback):
    # Find similar users for the given user ID using find_users function
    similar_users = find_users(user_id, buckets)

    # While no similar users are found
    while not similar_users:
        print("No similar users found. Adjusting LSH parameters...")
        # Adjust LSH parameters using the callback function
        lsh_parameters = adjust_params_callback(lsh_parameters, len(minhash_signatures[user_id]))
        # Recompute LSH buckets with updated parameters
        buckets = clustering.lsh(minhash_signatures, **lsh_parameters)
        # Search for similar users again
        similar_users = find_users(user_id, buckets)

    # Rank the similar users based on Jaccard similarity
    top_users = rank_similar_users(user_id, similar_users, minhash_signatures)
    return top_users

''' 
Function to dynamically adjust LSH parameters for better clustering
'''
def adjust_params(params, length):
    # Compute all valid divisors of the signature length
    divisors = [d for d in range(1, length + 1) if length % d == 0]

    # Retrieve the current number of bands
    current_bands = params["bands"]
    try:
        # Find the index of the current number of bands and move to the next valid divisor
        new_band_idx = divisors.index(current_bands) +1
        # Update the number of bands
        params["bands"] = divisors[new_band_idx]
    except IndexError:
        # If the current band index is at the end of the list, reset to the first divisor
        params["bands"] = divisors[0]
    # Recalculate rows per band based on the new number of bands
    params["rows_per_band"] = length // params["bands"]
    # Double the number of buckets to allow for finer-grained clustering
    params["num_buckets"] *= 2
    return params
