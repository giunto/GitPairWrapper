import sys, re, random

# --Global variables-- #
consonants = 'bcdfghjklmnpqrstvwxz'
vowels = 'aeiou'

# --Helper classes-- #

class TwoPartString:
    first_part = str()
    second_part = str()

    def __init__(self, first_part, second_part):
        self.first_part = first_part
        self.second_part = second_part

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and 
        self.first_part == other.first_part and 
        self.second_part == other.second_part)

    def get_full_string(self, seperator=''):
        return self.first_part + seperator + self.second_part

class CombinationHandler:
    valid_combinations = []
    invalid_combinations = []

    def __init__(self):
        self.valid_combinations = []
        self.invalid_combinations = []

    def filter_and_add(self, combination):
        if (combination.get_full_string() not in self.valid_combinations and 
            combination.first_part != '' and 
            combination.second_part != ''):

            if is_valid_combination(combination):
                self.valid_combinations.append(combination.get_full_string())
            elif combination.get_full_string() not in self.invalid_combinations:
                self.invalid_combinations.append(combination.get_full_string())

    def get_combinations(self):
        if self.valid_combinations == []:
            return self.invalid_combinations
        return self.valid_combinations

# --Helper functions and stuff-- #

def create_user_name_from_matches(match):
    names = match.group(2).split(' ', 1)
    first_name = names[0]
    last_name = names[1].strip() if len(names) > 1 else ''
    return TwoPartString(first_name, last_name)

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

def get_names_from_file(first_initials, second_initials, file_path):
    pair_file = open(file_path)

    pattern = re.compile(r'\s*(\w+)\s*:\s*([^;^\n]+)')

    first_name = None
    second_name = None
    
    for line in pair_file.readlines():
        matches = pattern.match(line)
        if matches != None:
            initials = matches.group(1)
            name = create_user_name_from_matches(matches)
            if initials == first_initials:
                first_name = name
            if initials == second_initials and first_initials != second_initials:
                second_name = name

    return {'first_name': first_name, 'second_name': second_name}

def parse_name(name):
    results = []
    name_length = len(name)

    if name_length < 2:
        return results

    if letter_is_vowel(name.lower(), 0):
        results.append(TwoPartString('', name))

    for i in range(name_length):
        if i != (name_length - 1) and can_split(name, i):
            results.append(TwoPartString(name[:(i + 1)], name[(i + 1):]))

    return results

def get_name_combinations(first_names, second_names):
    combinations = CombinationHandler()

    for first_name in first_names:
        for second_name in second_names:
            combinations.filter_and_add(TwoPartString(first_name.first_part, second_name.second_part))
            combinations.filter_and_add(TwoPartString(second_name.first_part, first_name.second_part))

    return combinations.get_combinations()

def main():
    names = get_names_from_file(sys.argv[1], sys.argv[2], sys.argv[3])

    if names['first_name'] == None and names['second_name'] == None:
        return ''
    if names['second_name'] == None:
        return names['first_name'].get_full_string(' ')
    if names['first_name'] == None:
        return names['second_name'].get_full_string(' ')

    if names['first_name'].second_part == '':
        parse_name(TwoPartString('Vulfgang', 'Kumar'))
        parse_name(TwoPartString('Ignace', ''))

        get_name_combinations(TwoPartString('Vulfg', 'ang'), TwoPartString('Ign', 'ace'))

    first_name_combinations = get_name_combinations(
            parse_name(names['first_name'].first_part),
            parse_name(names['second_name'].first_part)
        )
    last_name_combinations = get_name_combinations(
        parse_name(names['first_name'].second_part),
        parse_name(names['second_name'].second_part)
    )

    return (random.choice(first_name_combinations) + 
    ' ' + random.choice(last_name_combinations))

if __name__ == "__main__":
    print(main())
