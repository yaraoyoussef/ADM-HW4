from collections import defaultdict

''' 
Hashes a band and maps it to a bucket 
- Each band is hashed to a bucket using a simple hash function.
- The hash function maps the ASCII sum of the band's string representation to a bucket.
'''
def band_hashing(band, num_buckets):
    # Convert band to a string
    band_str = "_".join(map(str, band))
    
    # Simple hash function: sum ASCII values of characters in the string
    hash_val = sum(ord(char) for char in band_str)
    
    # Map to a bucket
    return hash_val % num_buckets

'''
Perform Locality-Sensitive Hashing (LSH) on MinHash signatures. LSH groups similar MinHash signatures 
into the same buckets using the "banding" technique to reduce dimensionality and improve efficiency.
'''
def lsh(minhash_signatures, bands, rows_per_band, num_buckets):
    # Assert that each signature must have length equal to bands * rows_per_band
    assert all(len(signature) == bands * rows_per_band for signature in minhash_signatures.values())
    
    # Create the buckets for each band
    buckets = [defaultdict(list) for _ in range(bands)]

    # For each user, hash their bands into buckets
    for user, signature in minhash_signatures.items():
        for band_idx in range(bands):
            start_idx = band_idx * rows_per_band
            end_idx = start_idx + rows_per_band
            band = signature[start_idx:end_idx]

            # Hash the band into a bucket
            bucket_id = band_hashing(band, num_buckets)
            buckets[band_idx][bucket_id].append(user)
            
    return buckets