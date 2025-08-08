# Cosine similarity

# Import libraries
import numpy as np
from numpy.linalg import norm

# Cosine similarity function
def cosine_similarity(vector_1, vector_2):
    '''
    Calculates the cosine similarity between two vectors

    Parameters:
    - vector_1: First vector (numpy array or list)
    - vector_2: Second vector (numpy array or list)
    
    Returns:
    - cosine_similarity: A value between -1 and 1 representing the similarity.
    '''

    # Ensure the inputs are numpy arrays
    vector_1 = np.array(vector_1, dtype=float)
    vector_2 = np.array(vector_2, dtype=float)

    norms_product = norm(vector_1) * norm(vector_2)
   
    # Avoid division by zero
    if norms_product == 0:
        return 0.0
    
    # Compute cosine similarity
    return np.dot(vector_1, vector_2)/(norm(vector_1)* norm(vector_2))


 # User input for vectors
if __name__ == "__main__":
    print("Enter the first vector, with components separated by spaces:")
    vector_1 = list(map(float, input().strip().split()))
    
    print("Enter the second vector, with components separated by spaces:")
    vector_2 = list(map(float, input().strip().split()))


# Compute cosine similarity
    similarity = cosine_similarity(vector_1, vector_2)
    print(f"Cosine Similarity: {similarity:.4f}")
