import unittest, pair_names
from parameterized import parameterized
from mock import patch, mock_open
from pair_names import SplitName, UserName

def parse_and_print(name):
    result = pair_names.parse_name(name)

    for x in result:
        print(x.first_part, x.second_part)

    return result

def make_fake_file(*args):
    fake_file = ''

    for line in args:
        fake_file += line + '\n'

    return fake_file


class TestGetNamesFromFile(unittest.TestCase):

    @parameterized.expand([

        # Basic test cases
        [
            'ab', 
            'cd', 
            make_fake_file(
                'pair:',
                '  ab: Alpha Beta; alphabeta',
                '  cd: Commodore Delta; commodoredelta'
            ), 
            [
                UserName('Alpha', 'Beta'), 
                UserName('Commodore', 'Delta')
            ]
        ],
        [
            'ms', 
            'sm', 
            make_fake_file(
                'pair:',
                '  ms: Monty Shallow; montyshallow',
                '  sm: Suzan Magitt; suzanmagitt'
            ), 
            [
                UserName('Monty', 'Shallow'), 
                UserName('Suzan', 'Magitt')
            ]
        ],

        # Names should be indexed by the initials.
        [
            'ml', 
            'mb', 
            make_fake_file(
                'pair:',
                '  ms: Mariel Sthilaire; msthilarie'
                '  ml: Michel Lola; mlola',
                '  mb: Maximo Baribeau; mbaribeau'
            ), 
            [
                UserName('Michel', 'Lola'), 
                UserName('Maximo', 'Baribeau')
            ]
        ],

    ])
    def test_get_names_from_file(self, first_initial, second_initial, file_contents, names):
        with patch('__builtin__.open', mock_open(read_data=file_contents)) as open_mock:
            result = pair_names.get_names_from_file(first_initial, second_initial, 'fake_file.txt')

            self.assertEqual(len(result), 2)
            self.assertEqual(result[0].first_name, names[0].first_name)
            self.assertEqual(result[0].last_name, names[0].last_name)
            self.assertEqual(result[1].first_name, names[1].first_name)
            self.assertEqual(result[1].last_name, names[1].last_name)

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
        ['aya', [
            SplitName('', 'aya'), 
            SplitName('ay', 'a')
        ]],

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

class TestGetNameCombinations(unittest.TestCase):

    @parameterized.expand([
        # Basic test cases
        [[SplitName('fr', 'y')], [SplitName('l', 'eela')], ['freela', 'ly']],
        [[SplitName('b', 'ob')], [SplitName('r', 'oss')], ['boss', 'rob']],
        [
            [SplitName('b', 'enjamin'), SplitName('benj', 'amin')],
            [SplitName('m', 'atthew'), SplitName('matth', 'ew')],
            [
                'batthew', 
                'menjamin', 
                'bew', 
                'matthenjamin', 
                'benjatthew', 
                'mamin', 
                'benjew', 
                'matthamin'
            ]
        ],
        [
            [SplitName('qu', 'igley')],
            [SplitName('sm', 'ith')],
            ['quith', 'smigley']
        ],

        # Duplicates should not be added.
        [[SplitName('st', 'ar')], [SplitName('st', 'ar')], ['star']],
        [
            [SplitName('s', 'amename'), SplitName('sam', 'ename'), SplitName('samen', 'ame')],
            [SplitName('s', 'amename'), SplitName('sam', 'ename'), SplitName('samen', 'ame')],
            [
                'samename',
                'sename',
                'samamename',
                'same',
                'samenamename',
                'samame',
                'samenename'
            ]
        ],

        # A word combination shouldn't be added if the first part or second part is an empty string.
        [
            [SplitName('', 'eclipse'), SplitName('ecl', 'ipse')],
            [SplitName('', 'autumn'), SplitName('aut', 'umn')],
            ['eclautumn', 'auteclipse', 'eclumn', 'autipse']
        ],
        [
            [SplitName('spr', 'ing'), SplitName('spring', '')],
            [SplitName('w', 'inter'), SplitName('winter', '')],
            ['sprinter', 'wing', 'wintering', 'springinter']
        ],
        [
            [SplitName('', '')],
            [SplitName('', '')],
            []
        ],

        # Parts that connect on the same letter shouldn't be added, unless there
        # are no other combinations.
        [
            [SplitName('qu', 'ail')],
            [SplitName('v', 'ulture'), SplitName('vult', 'ure')],
            ['vail', 'vultail']
        ],
        [
            [SplitName('QU', 'AIL')],
            [SplitName('V', 'ULTURE'), SplitName('VULT', 'URE')],
            ['VAIL', 'VULTAIL']
        ],
        [
            [SplitName('ea', 'gle')],
            [SplitName('seag', 'ull')],
            ['eaull']
        ],
        [
            [SplitName('', 'ural owl')],
            [SplitName('qu', 'ail')],
            ['quural owl']
        ],
        [
            [SplitName('qu', 'ail')],
            [SplitName('', 'ural owl')],
            ['quural owl']
        ],
        [
            [SplitName('qu', 'ail')],
            [SplitName('', 'ural owl'), SplitName('', 'ural owl')],
            ['quural owl']
        ],
        [
            [SplitName('', 'ural owl'), SplitName('', 'ural owl')],
            [SplitName('qu', 'ail')],
            ['quural owl']
        ]

    ])
    def test_get_name_combinations(self, first_name, second_name, combinations):
        result = pair_names.get_name_combinations(first_name, second_name)

        print(result)

        self.assertEqual(len(result), len(combinations))
        for name in result:
            self.assertIn(name, result)

if __name__ == '__main__':
    unittest.main()