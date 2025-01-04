## Cosine Similarity

This Python program calculates the cosine similarity between two vectors. Cosine similarity is a widely used metric to measure the similarity between two objects in various domains such as natural language processing, recommendation systems, and image processing.

The program allows users to input two vectors and computes their cosine similarity, which is a value between -1 and 1. A similarity of 1 indicates identical vectors, while -1 indicates completely opposite vectors. A similarity of 0 indicates the vectors are orthogonal (i.e., they have no correlation and are at a 90-degree angle to each other).

### Overview


**Mathematical Formula**


![cosine-similarity](https://github.com/user-attachments/assets/8579fde6-b703-4c0d-aa45-7fd8b737b160 =500x500)

<img src="https://github.com/user-attachments/assets/8579fde6-b703-4c0d-aa45-7fd8b737b160" width="500" height="500">


||A|| and ||B|| are the Euclidean norms (magnitudes) of the vectors, calculated as:


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
