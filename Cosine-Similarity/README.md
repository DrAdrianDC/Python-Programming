## Cosine Similarity

This Python program calculates the cosine similarity between two vectors. Cosine similarity is a widely used metric to measure the similarity between two objects in various domains such as natural language processing, recommendation systems, and image processing.

The program allows users to input two vectors and computes their cosine similarity, which is a value between -1 and 1. A similarity of 1 indicates identical vectors, while -1 indicates completely opposite vectors. A similarity of 0 indicates the vectors are orthogonal (i.e., they have no correlation and are at a 90-degree angle to each other).

### Overview


**Mathematical Formula**

```bash
Cosine Similarity = (A · B) / (||A|| * ||B||)
```

```bash
A · B = Σ (Ai * Bi) for i = 1 to n
```

||A|| and ||B|| are the Euclidean norms (magnitudes) of the vectors, calculated as:

```bash
||A|| = sqrt(A1^2 + A2^2 + ... + An^2)
||B|| = sqrt(B1^2 + B2^2 + ... + Bn^2)
```

Cosine Similarity is a **simple mathematical concept and easy to implement computationally**, making it highly practical for real-world implementations.


### Requirements

- **Python 3.8.3**
  
To run this code, you'll need the following Python packages:

- `numpy`

You can install the required packages using pip:

```bash
pip install numpy
```

### How to Use 

```bash
python cosine_similarity.py
```
