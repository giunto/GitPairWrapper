import unittest, pair_names
from parameterized import parameterized
from pair_names import SplitName

def parse_and_print(name):
    result = pair_names.parse_name(name)

    for x in result:
        print(x.first_part, x.second_part)

    return result

class TestParseName(unittest.TestCase):

    @parameterized.expand([
        # Basic test cases
        ['brian', [SplitName('br', 'ian')]],
        ['BRIAN', [SplitName('BR', 'IAN')]],
        ['katie', [
            SplitName('k', 'atie'), 
            SplitName('kat', 'ie')
        ]],
        ['ulo', [
            SplitName('', 'ulo'), 
            SplitName('ul', 'o')
        ]],

        # Silent e at the end of words should not be parsed
        ['blake', [SplitName('bl', 'ake')]],
        ['BLAKE', [SplitName('BL', 'AKE')]],
        ['the', [SplitName('th', 'e')]],
        ['ye', [SplitName('y', 'e')]],
        ['KANYE', [
            SplitName('K', 'ANYE'),
            SplitName('KANY', 'E')
        ]],
        ['tree', [SplitName('tr', 'ee')]],
        ['ee', [SplitName('', 'ee')]],

        # The letter y should be treated as a vowel when it comes before a consonant
        # If it comes before a vowel it is treated as a consonant
        ['kyle', [SplitName('k', 'yle')]],
        ['KYLE', [SplitName('K', 'YLE')]],
        ['yani', [
            SplitName('y', 'ani'), 
            SplitName('yan', 'i')
        ]],
        ['YANI', [
            SplitName('Y', 'ANI'), 
            SplitName('YAN', 'I')
        ]],
        ['quenya', [
            SplitName('qu', 'enya'),
            SplitName('queny', 'a')
        ]],
        ['FLYYY', [SplitName('FL', 'YYY')]],

        # The letter combination qu should be treated as a consonant if
        # a vowel directly follows.
        # If a consonant follows u then q and u are split.
        ['quigley', [
            SplitName('qu', 'igley'),
            SplitName('quigl', 'ey')
        ]],
        ['QUIGLEY', [
            SplitName('QU','IGLEY'),
            SplitName('QUIGL', 'EY')
        ]],
        ['quran', [
            SplitName('q', 'uran'),
            SplitName('qur', 'an')
        ]],
        ['yaquinta', [
            SplitName('y', 'aquinta'),
            SplitName('yaqu', 'inta'),
            SplitName('yaquint', 'a')
        ]],
        ['quya', [
            SplitName('q', 'uya'),
            SplitName('quy', 'a')
        ]],
        ['qu', [SplitName('q', 'u')]],
        ['qy', [SplitName('q', 'y')]],
        ['uq', [SplitName('', 'uq')]],

        # Words that start with a vowel should be parsed before the word starts.
        ['ypsilanti', [
            SplitName('', 'ypsilanti'), 
            SplitName('yps', 'ilanti'), 
            SplitName('ypsil', 'anti'), 
            SplitName('ypsilant', 'i')
        ]],

        # If y follows another y, both should be treated as vowels.
        ['yy', [SplitName('', 'yy')]],

        # Ignore strings less than 2 characters
        ['', []],
        ['a', []],
        ['b', []],

        # Nonalphabetic characters are treated like consonants
        ['two-words', [
            SplitName('tw', 'o-words'),
            SplitName('two-w', 'ords')
        ]],

        # The silent e rule still applies if e is followed by an nonalphabetic character.
        ['white space', [
            SplitName('wh', 'ite space'),
            SplitName('white sp', 'ace')
        ]],
        ['the,exclamation!point', [
            SplitName('th', 'e,exclamation!point'),
            SplitName('the,', 'exclamation!point'),
            SplitName('the,excl', 'amation!point'),
            SplitName('the,exclam', 'ation!point'),
            SplitName('the,exclamat', 'ion!point'),
            SplitName('the,exclamation!p', 'oint')
        ]],
        ['notice the middle word', [
            SplitName('n', 'otice the middle word'),
            SplitName('not', 'ice the middle word'),
            SplitName('notice th', 'e middle word'),
            SplitName('notice the m', 'iddle word'),
            SplitName('notice the middle w', 'ord')
        ]],
        ['qu eqy tae', [
            SplitName('q', 'u eqy tae'),
            SplitName('qu ', 'eqy tae'),
            SplitName('qu eq', 'y tae'),
            SplitName('qu eqy t', 'ae')
        ]],
        [' e ', [SplitName(' ', 'e ')]],
        ['the thee me ate greate hate query', [
            SplitName('th', 'e thee me ate greate hate query'),
            SplitName('the th', 'ee me ate greate hate query'),
            SplitName('the thee m', 'e ate greate hate query'),
            SplitName('the thee me ', 'ate greate hate query'),
            SplitName('the thee me ate gr', 'eate hate query'),
            SplitName('the thee me ate greate h', 'ate query'),
            SplitName('the thee me ate greate hate qu', 'ery'),
            SplitName('the thee me ate greate hate quer', 'y'),
        ]]
    ])
    def test_parse_name(self, name, split_names):
        result = pair_names.parse_name(name)

        for x in result:
            print(x.first_part, x.second_part)

        self.assertEqual(len(result), len(split_names))
        for i in range(len(split_names)):
            self.assertEqual(result[i].first_part, split_names[i].first_part)
            self.assertEqual(result[i].second_part, split_names[i].second_part)

if __name__ == '__main__':
    unittest.main()