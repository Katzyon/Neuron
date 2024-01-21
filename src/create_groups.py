import random

def create_groups(n = 100, m = 3, k = 20):
    """ create_groups(n = int, m = int, k = int) -> list, list
    Create m groups of size k from n range numbers.
    Return a list of groups and a list of remaining numbers.
    Inputs: 
        n: The range of numbers, from 1 to n.
        m: The number of groups.
        k: The size of each group.
    Outputs:
        groups: A list of m groups of size k.
        remaining_numbers: A list of remaining numbers not assined to any group :-(.
    """

    # Create a list from 1 to n
    number_list = list(range(1, n + 1))

    # Initialize the list for groups and the list for remaining numbers
    groups = []
    remaining_numbers = number_list.copy()

    # Create m groups each of size k
    for _ in range(m):
        if len(remaining_numbers) < k:
            raise ValueError("Not enough remaining numbers to form a group")
        
        group = random.sample(remaining_numbers, k)
        groups.append(group)

        # Remove the selected numbers from the remaining numbers
        remaining_numbers = [num for num in remaining_numbers if num not in group]

    return groups, remaining_numbers

# Example usage
n, m, k = map(int, input("Enter n, m, k separated by SPACES: ").split())
groups, remaining = create_groups(n, m, k)

print("Groups:", groups)
print("Remaining numbers:", remaining)
