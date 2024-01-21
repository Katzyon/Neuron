
import random

def create_groups(n = 100, m = 3, k = 20):
    """ create_groups(n = int, m = int, k = int)  -> list, list

    
    The function randomly assigns the n objects to m groups such that each group has k objects.
    Return a list of groups with k elements each and a list of the unassigned objects (if any).
    Args:
        n = number of objects
        m = number of groups
        k = size of each group
    Returns:
        groups = list of groups
        remaining = list of unassigned objects

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
