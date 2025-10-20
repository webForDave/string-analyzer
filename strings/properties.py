import string
import hashlib
lowercase_alphabet = list(string.ascii_lowercase)

def check_palindrome(string: str):
    string_backwards = []
    string_as_list = []

    new_string_as_list = []
    new_string_backwards = []

    for i, j in zip(string, string[: : -1]):
        string_as_list.append(i.lower())
        string_backwards.append(j.lower())

    for i, j in zip(string_as_list, string_backwards):
        if i in lowercase_alphabet:new_string_as_list.append(i)
        if j in lowercase_alphabet: new_string_backwards.append(j)

    if "".join(new_string_backwards) == "".join(new_string_as_list):
        return True
    return False

def get_unique_characters(string: str):
    string_as_list = list(string)
    unique_characters = []

    for i in string_as_list:
        if i not in unique_characters and i in lowercase_alphabet:
            unique_characters.append(i)
    return len(unique_characters)

def get_string_hashlib(string: str):
    encoded_string = string.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(encoded_string)
    return sha256_hash.hexdigest()

def get_character_frequency_map(string: str):
    characters = dict()
    string_as_list = []

    for i in string:
        if i.lower() in lowercase_alphabet:
            string_as_list.append(i.lower())

    for i in string_as_list:
        if i in characters:
            characters[i] += 1
        else:
            characters[i] = 1
    return characters

print(get_character_frequency_map("Brave travelers return at twilight, tracing ancient terrain near tranquil rivers, breathing radiant air, hearing eternal rain, treating nature as a tender artist, narrating rare tales anew, creating radiant art that retains ancient traces, trailing after reappearing lanterns, reaching radiant terrain again, returning at twilight repeatedly, treating nature’s eternal rhythm as truth."))

def return_string_properties(string: str):   
    return {
        "length": len(string),
        "is_palindrome": check_palindrome(string),
        "unique_characters": get_unique_characters(string),
        "word_count": len(string.split(" ")),
        "sha256_hash": get_string_hashlib(string),
        "character_frequency_map": get_character_frequency_map(string),
    }