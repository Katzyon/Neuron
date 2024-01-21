import numpy as np
import matplotlib.pyplot as plt

def generate_random_vector(prob_vector, k):
    if not np.isclose(sum(prob_vector), 1):
        raise ValueError("Sum of probability vector should be 1.")
    n = len(prob_vector)
    return np.random.choice(range(1, n + 1), size=k, p=prob_vector)

# Generate a random vector
prob_vector = [0.7, 0.2, 0.1]  # Example probability vector for n=3
k = 1000  # Increase k to get a better distribution visualization
random_vector = generate_random_vector(prob_vector, k)

# Plotting the random_vector as a bar plot
values, counts = np.unique(random_vector, return_counts=True)
plt.bar(values, counts, tick_label=[f"Value {i}" for i in values])
plt.xlabel('Values')
plt.ylabel('Counts')
plt.title('Bar Plot of Random Vector')
plt.show()
