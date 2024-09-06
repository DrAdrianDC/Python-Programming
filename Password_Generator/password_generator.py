# Password Generator

import random

password_characters = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
    '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', 
    '+', '=', '<', '>', '?', '{', '}', '[', ']', '|', '/', '\\'
]


# Function to generate a random password
def generate_password(length=12):
    password = ""
    for x in range(length):
        password += random.choice(password_characters)
    return password



while True:
    # Prompt user to press Enter to generate a password
    user_input = input("Press Enter to generate your new password (or type 'exit' to quit)... ").strip()
    
    if user_input == "":
        password = generate_password()
        print(f'Your Password is: {password}')
        break
    elif user_input.lower() == "exit":
        print("Exiting the program.")
        break
    else:
        print("Invalid input. Please just press Enter or type 'exit' to quit.")

