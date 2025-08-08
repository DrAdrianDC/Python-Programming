
# Letter Count and Index Finder


def count_or_find_letter(word, letter, action='count'):
    if action == 'count':
        return word.count(letter)
    elif action == 'index':
        try:
            return word.index(letter)
        except ValueError:
            return f"'{letter}' not found in '{word}'"
    else:
        raise ValueError("Invalid action! Choose 'count' or 'index'.")

# Example usage
word = input("Enter a word: ")
letter = input("Enter the letter to count or find: ")
action = input("Choose the action (count or index): ")

result = count_or_find_letter(word, letter, action)
print(f"The result of {action}ing '{letter}' in '{word}' is: {result}")
