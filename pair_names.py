import sys

# --Global variables-- #
consonants = 'bcdfghjklmnpqrstvwxz'
vowels = 'aeiou'

# --Helper classes-- #

class UserName:
    first_name = str()
    last_name = str()

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

class SplitName:
    first_part = str()
    second_part = str()

    def __init__(self, first_part, second_part):
        self.first_part = first_part
        self.second_part = second_part


# --Helper functions and stuff-- #

def letter_is_consonant(name, index):
    letter = name[index].lower()
    next_letter = name[index + 1].lower()

    return letter in consonants or (letter == 'y' and next_letter in vowels)

def letter_is_vowel(name, index):
    letter = name[index].lower()

    return (letter in vowels or 
        (letter == 'y' and ((index + 1) not in range(len(name)) or name[index + 1].lower() in consonants or name[index + 1].lower() == 'y')))

def second_letter_is_silent_e(name, index):
    letter = name[index + 1]

    return index + 1 == len(name) - 1 and letter.lower() == 'e'

def can_split(name, index):
    first_letter = name[index]
    second_letter = name[index + 1]

    return (letter_is_consonant(name, index) and 
        letter_is_vowel(name, index + 1) and 
        not second_letter_is_silent_e(name, index) and
        not ((index + 2) in range(len(name)) and first_letter.lower() == 'q' and second_letter.lower() == 'u' and letter_is_vowel(name, index + 2)) or
        (first_letter.lower() == 'u' and name[index - 1].lower() == 'q' and letter_is_vowel(name, index + 1)))

# --Main functions-- #

def parse_name(name):
    results = []
    name_length = len(name)

    if name_length < 2:
        return results

    if letter_is_vowel(name, 0):
        results.append(SplitName('', name))

    for i in range(name_length):
        if i != (name_length - 1) and can_split(name, i):
            results.append(SplitName(name[:(i + 1)], name[(i + 1):]))

    return results

def main():
    arguments = sys.argv[1:]

if __name__ == "__main__":
    main()
