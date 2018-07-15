import sys

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
    consonants = 'bcdfghjklmnpqrstvwxz'
    letter = name[index]

    return letter.lower() in consonants or y_is_consonant(name, index)

def letter_is_vowel(letter):
    vowels = 'aeiouy'

    return letter.lower() in vowels 

def second_letter_is_silent_e(name, index):
    letter = name[index + 1]

    return index + 1 == len(name) - 1 and letter.lower() == 'e'

def y_is_consonant(name, index):
    letter = name[index]
    next_letter = name[index + 1]

    return letter.lower() == 'y' and letter_is_vowel(next_letter)

def can_split(name, index):
    first_letter = name[index]
    second_letter = name[index + 1]

    return (letter_is_consonant(name, index) and 
        letter_is_vowel(second_letter) and 
        not second_letter_is_silent_e(name, index) and
        not (first_letter.lower() == 'q' and second_letter.lower() == 'u' and letter_is_vowel(name[index + 2]) and not letter_is_consonant(name, index + 2)) or
        (first_letter.lower() == 'u' and name[index - 1].lower() == 'q' and letter_is_vowel(second_letter) and not letter_is_consonant(name, index + 1)))

# --Main functions-- #

def parse_name(name):
    results = []
    name_length = len(name)

    if name_length < 2:
        return results

    if letter_is_vowel(name[0]) and not y_is_consonant(name, 0):
        results.append(SplitName('', name))

    for i in range(name_length):
        if i != (name_length - 1) and can_split(name, i):
            results.append(SplitName(name[0:(i + 1)], name[(i + 1):name_length]))

    return results

def main():
    arguments = sys.argv[1:]

if __name__ == "__main__":
    main()
