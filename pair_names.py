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

class CombinedName:
    first_part = str()
    second_part = str()

    def __init__(self, first_part, second_part):
        self.first_part = first_part
        self.second_part = second_part

    def get_name(self):
        return self.first_part + self.second_part


# --Helper functions and stuff-- #

def index_is_in_range(index, word):
    return index in range(len(word))

def letter_is_consonant(name, index):
    return (name[index] in consonants or 
        (name[index] == 'y' and name[index + 1] in vowels))

def letter_is_vowel(name, index):
    return (name[index] in vowels or 
        (name[index] == 'y' and 
            (not index_is_in_range(index + 1, name) or 
            letter_is_unknown(name, index + 1) or 
            name[index + 1] in (consonants + 'y'))))

def letter_is_unknown(name, index):
    return name[index] not in (consonants + vowels + 'y')

def number_of_vowels(name):
    total = 0

    for vowel in (vowels + 'y'):
        total += name.count(vowel)

    return total

def second_letter_is_silent_e(name, index):
    return ((index + 1 == len(name) - 1 or letter_is_unknown(name, index + 2)) and 
        name[index + 1] == 'e' and 
        name[index] != 'y' and 
        number_of_vowels(name[start_of_word(name, index):(index + 2)]) > 1)

def start_of_word(name, index):
    start_index = index
    while start_index > 0 and not letter_is_unknown(name, start_index):
        start_index -= 1

    return start_index

def can_split(name, index):
    name = name.lower()

    return ((letter_is_consonant(name, index) or letter_is_unknown(name, index)) and 
        letter_is_vowel(name, index + 1) and 
        not second_letter_is_silent_e(name, index) and
        not (index_is_in_range(index + 2, name) and 
            name[index] == 'q' and 
            name[index + 1] == 'u' and 
            letter_is_vowel(name, index + 2)) or
        (name[index] == 'u' and 
            name[index - 1] == 'q' and 
            letter_is_vowel(name, index + 1)))

def is_valid_combination(combination):
    last_letter_of_first_part = combination.first_part[len(combination.first_part) - 1].lower()
    first_letter_of_second_part = combination.second_part[0].lower()

    return last_letter_of_first_part != first_letter_of_second_part

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

def get_name_combinations(first_names, second_names):
    combinations = []
    bad_combinations = []

    for first_name in first_names:
        for second_name in second_names:
            first_combination = CombinedName(first_name.first_part, second_name.second_part)

            if first_combination.get_name() not in combinations and first_combination.first_part != '':
                if is_valid_combination(first_combination):
                    combinations.append(first_combination.get_name())
                elif first_combination.get_name() not in bad_combinations:
                    bad_combinations.append(first_combination.get_name())

            second_combination = CombinedName(second_name.first_part, first_name.second_part)
            if second_combination.get_name() not in combinations and second_combination.first_part != '':
                if is_valid_combination(second_combination):
                    combinations.append(second_combination.get_name())
                elif second_combination.get_name() not in bad_combinations:
                    bad_combinations.append(second_combination.get_name())

    if combinations == []:
        return bad_combinations
    return combinations

def main():
    arguments = sys.argv[1:]

if __name__ == "__main__":
    main()
