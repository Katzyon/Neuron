import numpy as np

def generate_random_vector(prob_vector, k):
    """
    Generate a random vector of length k with elements from 1 to n,
    where each element appears with a probability specified in prob_vector.

    :param prob_vector: A probability vector of length n, summing up to 1.
    :param k: The number of repeats (length of the output vector).
    :return: A random vector of length k.
    """
    if not np.isclose(sum(prob_vector), 1):
        raise ValueError("Sum of probability vector should be 1.")

    n = len(prob_vector)
    return np.random.choice(range(1, n + 1), size=k, p=prob_vector)

# Example usage
prob_vector = [0.7, 0.2, 0.1]  # Example probability vector for n=3
k = 1000  # Number of repeats
random_vector = generate_random_vector(prob_vector, k)

# plot the histogram
import matplotlib.pyplot as plt
plt.hist(random_vector, bins=range(1, len(prob_vector) + 2))
plt.show()

