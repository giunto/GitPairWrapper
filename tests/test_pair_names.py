import unittest, pair_names, sys
from parameterized import parameterized
from mock import patch, mock_open
from pair_names import TwoPartString

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
            {
                'first_name': TwoPartString('Alpha', 'Beta'), 
                'second_name': TwoPartString('Commodore', 'Delta')
            }
        ],
        [
            'ms', 
            'sm', 
            make_fake_file(
                'pair:',
                '  ms: Monty Shallow; montyshallow',
                '  sm: Suzan Magitt; suzanmagitt'
            ), 
            {
                'first_name': TwoPartString('Monty', 'Shallow'), 
                'second_name': TwoPartString('Suzan', 'Magitt')
            }
        ],
        [
            'ak', 
            'mh', 
            make_fake_file(
                'pair:',
                '  ak: Angle Knickerbocker',
                '  mh: Maximina Hardinson'
            ), 
            {
                'first_name': TwoPartString('Angle', 'Knickerbocker'), 
                'second_name': TwoPartString('Maximina', 'Hardinson')
            }
        ],
        [
            'ba',
            'oh',
            make_fake_file(
                'ba: Borghild Amadi; bamadi',
                'oh: Olamide Heidrun; oheidrun'
            ),
            {
                'first_name': TwoPartString('Borghild', 'Amadi'),
                'second_name': TwoPartString('Olamide', 'Heidrun')
            }
        ],

        # Names should be indexed by the initials.
        [
            'ml', 
            'mb', 
            make_fake_file(
                'pair:',
                '  ms: Mariel Sthilaire; msthilarie',
                '  ml: Michel Lola; mlola',
                '  mb: Maximo Baribeau; mbaribeau'
            ), 
            {
                'first_name': TwoPartString('Michel', 'Lola'), 
                'second_name': TwoPartString('Maximo', 'Baribeau')
            }
        ],
                [
            'kb', 
            'lf', 
            make_fake_file(
                'pair:',
                '  kb: Klara Bartos; kbartos',
                '  rh: Royce Hanstine; rhanstine',
                '  lf: Lanny Fiore; lfiore'
            ), 
            {
                'first_name': TwoPartString('Klara', 'Bartos'), 
                'second_name': TwoPartString('Lanny', 'Fiore')
            }
        ],
        [
            'yr', 
            'mn', 
            make_fake_file(
                'pair:',
                '  mn: Mikel Niederhaus; mniederhaus',
                '  yr: Yadira Reddell; yreddell'
            ), 
            {
                'first_name': TwoPartString('Yadira', 'Reddell'),
                'second_name': TwoPartString('Mikel', 'Niederhaus')
            }
        ],
        [
            'sk', 
            'bz', 
            make_fake_file(
                'pair:',
                '  ad: Alane Durig; adurig',
                '  bz: Berry Zuno; bzuno',
                '  sk: Shaquita Kenagy; skenagy'
            ), 
            {
                'first_name': TwoPartString('Shaquita', 'Kenagy'),
                'second_name': TwoPartString('Berry', 'Zuno')
            }
        ],
        [
            'gl', 
            'av', 
            make_fake_file(
                'pair:',
                '  av: Alonzo Vandyk; avandyk',
                '  jc: Josh Caparoula; jcaparoula',
                '  gl: Gustavo Laneve; glaneve'
            ), 
            {
                'first_name': TwoPartString('Gustavo', 'Laneve'), 
                'second_name': TwoPartString('Alonzo', 'Vandyk')
            }
        ],


        # Different lengths of initials should be handled.
        [
            'c', 
            'a', 
            make_fake_file(
                'pair:',
                '  a: Apple Anderson; apple',
                '  c: Carrot Cianciolo; carrot'
            ), 
            {
                'first_name': TwoPartString('Carrot', 'Cianciolo'), 
                'second_name': TwoPartString('Apple', 'Anderson')
            }
        ],
        [
            'abc',
            'xyz',
            make_fake_file(
                'pair:',
                '  xyz: Xavier Zamenhof; xzam',
                '  abc: The Alphabet; abcdefghijklmnopqrstuvwxyz'
            ),
            {
                'first_name': TwoPartString('The', 'Alphabet'),
                'second_name': TwoPartString('Xavier', 'Zamenhof')
            }
        ],

        # If there is no last name, then the last name should be an empty string.
        [
            'tom',
            'na',
            make_fake_file(
                'pair:',
                '  tom: Tom; tom',
                '  na: Nobody; nobody'
            ),
            {
                'first_name': TwoPartString('Tom', ''),
                'second_name': TwoPartString('Nobody', '')
            }
        ],

        # If there are multiple names/letters after the first name, those should be
        # treated as a last name.
        [
            'hm',
            'sb',
            make_fake_file(
                'pair:',
                '  hm: Hank B. McHillington; hankhill',
                '  sb: Sally Van Der Bork; sbork'
            ),
            {
                'first_name': TwoPartString('Hank', 'B. McHillington'),
                'second_name': TwoPartString('Sally', 'Van Der Bork')
            }
        ],

        # Different lengths of whitespace should be handled,
        # but left alone if they are in the last name.
        [
            'fn',
            'bc',
            make_fake_file(
                'pair:',
                '    fn   :   Fiammetta   Nascimbeni   ; fnascimbeni',
                'bc:Benito   Rodolfo   Catalano   '
            ),
            {
                'first_name': TwoPartString('Fiammetta', 'Nascimbeni'),
                'second_name': TwoPartString('Benito', 'Rodolfo   Catalano')
            }
        ]

    ])
    def test_get_names_from_file(self, first_initials, second_initials, file_contents, names):
        with patch('__builtin__.open', mock_open(read_data=file_contents)):
            result = pair_names.get_names_from_file(first_initials, second_initials, 'fake_file.txt')

            first_name = result['first_name']
            second_name = result['second_name']

            expected_first_name = names['first_name']
            expected_second_name = names['second_name']

            self.assertEqual(first_name.first_part, expected_first_name.first_part)
            self.assertEqual(first_name.second_part, expected_first_name.second_part)
            self.assertEqual(second_name.first_part, expected_second_name.first_part)
            self.assertEqual(second_name.second_part, expected_second_name.second_part)

    @parameterized.expand([
        [
            'st', 
            'ib', 
            make_fake_file(
                'pair:',
                '  ib: Ilona Bute; ibute',
                '  ss: Sherry Sokoloski; ssokoloski'
            ), 
            TwoPartString('Ilona', 'Bute')
        ],
    ])
    def test_get_names_from_file_first_name_doesnt_exist(self, first_initials, second_initials, file_contents, expected_second_name):
        with patch('__builtin__.open', mock_open(read_data=file_contents)):
            result = pair_names.get_names_from_file(first_initials, second_initials, 'fake_file.txt')

            first_name = result['first_name']
            second_name = result['second_name']

            self.assertIsNone(first_name)
            self.assertEqual(second_name.first_part, expected_second_name.first_part)
            self.assertEqual(second_name.second_part, expected_second_name.second_part)

    @parameterized.expand([
        [
            'ml', 
            'jn', 
            make_fake_file(
                'pair:',
                '  jm: Jae Miners; jminers',
                '  ml: Malcolm Locks; mlocks'
            ), 
            TwoPartString('Malcolm', 'Locks')
        ],

        # This logic might become obsolete.
        [
            'hn',
            'hn',
            make_fake_file(
                'pair:',
                '  hn: Hoshi Nakahara; hnakahara',
                '  hn: Harlan Nye; hnye'
            ),
            TwoPartString('Harlan', 'Nye')
        ]
    ])
    def test_get_names_from_file_second_name_doesnt_exist(self, first_initials, second_initials, file_contents, expected_first_name):
        with patch('__builtin__.open', mock_open(read_data=file_contents)):
            result = pair_names.get_names_from_file(first_initials, second_initials, 'fake_file.txt')

            first_name = result['first_name']
            second_name = result['second_name']

            self.assertEqual(first_name.first_part, expected_first_name.first_part)
            self.assertEqual(first_name.second_part, expected_first_name.second_part)
            self.assertIsNone(second_name)

    @parameterized.expand([
        [
            'gs',
            'dh',
            make_fake_file(
                'pair:'
                '  em: Elisha McCauley; mccauley',
                '  sm: Saul Mounger; soulmongerer'
            )
        ],
        [
            'qm',
            'gb',
            make_fake_file(
                'pair:'
                '  qm:',
                '  gb:'
            )
        ]
    ])
    def test_get_names_from_file_neither_name_exists(self, first_initials, second_initials, file_contents):
        with patch('__builtin__.open', mock_open(read_data=file_contents)):
            result = pair_names.get_names_from_file(first_initials, second_initials, 'fake_file.txt')

            self.assertIsNone(result['first_name'])
            self.assertIsNone(result['second_name'])

    @parameterized.expand([
        'all_the_pairs.txt',
        'pear_city.html'
    ])
    def test_get_names_from_file_should_use_file_path(self, file_path):
        with patch('__builtin__.open', mock_open(read_data='')) as open_mock:
            pair_names.get_names_from_file('', '', file_path)

            open_mock.assert_called_once_with(file_path)



class TestParseName(unittest.TestCase):

    @parameterized.expand([
        # Basic test cases
        ['brian', [TwoPartString('br', 'ian')]],
        ['BRIAN', [TwoPartString('BR', 'IAN')]],
        ['katie', [
            TwoPartString('k', 'atie'), 
            TwoPartString('kat', 'ie')
        ]],

        # Silent e at the end of words should not be parsed
        ['blake', [TwoPartString('bl', 'ake')]],
        ['BLAKE', [TwoPartString('BL', 'AKE')]],
        ['the', [TwoPartString('th', 'e')]],
        ['ye', [TwoPartString('y', 'e')]],
        ['KANYE', [
            TwoPartString('K', 'ANYE'),
            TwoPartString('KANY', 'E')
        ]],
        ['tree', [TwoPartString('tr', 'ee')]],
        ['ee', [TwoPartString('', 'ee')]],

        # The letter y should be treated as a vowel when it comes before a consonant
        # If it comes before a vowel it is treated as a consonant
        ['kyle', [TwoPartString('k', 'yle')]],
        ['KYLE', [TwoPartString('K', 'YLE')]],
        ['yani', [
            TwoPartString('y', 'ani'), 
            TwoPartString('yan', 'i')
        ]],
        ['YANI', [
            TwoPartString('Y', 'ANI'), 
            TwoPartString('YAN', 'I')
        ]],
        ['quenya', [
            TwoPartString('qu', 'enya'),
            TwoPartString('queny', 'a')
        ]],
        ['FLYYY', [TwoPartString('FL', 'YYY')]],
        ['aya', [
            TwoPartString('', 'aya'), 
            TwoPartString('ay', 'a')
        ]],

        # The letter combination qu should be treated as a consonant if
        # a vowel directly follows.
        # If a consonant follows u then q and u are split.
        ['quigley', [
            TwoPartString('qu', 'igley'),
            TwoPartString('quigl', 'ey')
        ]],
        ['QUIGLEY', [
            TwoPartString('QU','IGLEY'),
            TwoPartString('QUIGL', 'EY')
        ]],
        ['quran', [
            TwoPartString('q', 'uran'),
            TwoPartString('qur', 'an')
        ]],
        ['yaquinta', [
            TwoPartString('y', 'aquinta'),
            TwoPartString('yaqu', 'inta'),
            TwoPartString('yaquint', 'a')
        ]],
        ['quya', [
            TwoPartString('q', 'uya'),
            TwoPartString('quy', 'a')
        ]],
        ['qu', [TwoPartString('q', 'u')]],
        ['qy', [TwoPartString('q', 'y')]],
        ['uq', [TwoPartString('', 'uq')]],

        # Words that start with a vowel should be parsed before the word starts.
        ['ypsilanti', [
            TwoPartString('', 'ypsilanti'), 
            TwoPartString('yps', 'ilanti'), 
            TwoPartString('ypsil', 'anti'), 
            TwoPartString('ypsilant', 'i')
        ]],
        ['AJ', [TwoPartString('', 'AJ')]],
        ['ulo', [
            TwoPartString('', 'ulo'), 
            TwoPartString('ul', 'o')
        ]],

        # If y follows another y, both should be treated as vowels.
        ['yy', [TwoPartString('', 'yy')]],

        # Ignore strings less than 2 characters
        ['', []],
        ['a', []],
        ['b', []],

        # Nonalphabetic characters are treated like consonants
        ['two-words', [
            TwoPartString('tw', 'o-words'),
            TwoPartString('two-w', 'ords')
        ]],

        # The silent e rule still applies if e is followed by an nonalphabetic character.
        ['white space', [
            TwoPartString('wh', 'ite space'),
            TwoPartString('white sp', 'ace')
        ]],
        ['the,exclamation!point', [
            TwoPartString('th', 'e,exclamation!point'),
            TwoPartString('the,', 'exclamation!point'),
            TwoPartString('the,excl', 'amation!point'),
            TwoPartString('the,exclam', 'ation!point'),
            TwoPartString('the,exclamat', 'ion!point'),
            TwoPartString('the,exclamation!p', 'oint')
        ]],
        ['notice the middle word', [
            TwoPartString('n', 'otice the middle word'),
            TwoPartString('not', 'ice the middle word'),
            TwoPartString('notice th', 'e middle word'),
            TwoPartString('notice the m', 'iddle word'),
            TwoPartString('notice the middle w', 'ord')
        ]],
        ['qu eqy tae', [
            TwoPartString('q', 'u eqy tae'),
            TwoPartString('qu ', 'eqy tae'),
            TwoPartString('qu eq', 'y tae'),
            TwoPartString('qu eqy t', 'ae')
        ]],
        [' e ', [TwoPartString(' ', 'e ')]],
        ['the thee me ate greate hate query', [
            TwoPartString('th', 'e thee me ate greate hate query'),
            TwoPartString('the th', 'ee me ate greate hate query'),
            TwoPartString('the thee m', 'e ate greate hate query'),
            TwoPartString('the thee me ', 'ate greate hate query'),
            TwoPartString('the thee me ate gr', 'eate hate query'),
            TwoPartString('the thee me ate greate h', 'ate query'),
            TwoPartString('the thee me ate greate hate qu', 'ery'),
            TwoPartString('the thee me ate greate hate quer', 'y'),
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
        [[TwoPartString('fr', 'y')], [TwoPartString('l', 'eela')], ['freela', 'ly']],
        [[TwoPartString('b', 'ob')], [TwoPartString('r', 'oss')], ['boss', 'rob']],
        [
            [TwoPartString('b', 'enjamin'), TwoPartString('benj', 'amin')],
            [TwoPartString('m', 'atthew'), TwoPartString('matth', 'ew')],
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
            [TwoPartString('qu', 'igley')],
            [TwoPartString('sm', 'ith')],
            ['quith', 'smigley']
        ],

        # Duplicates should not be added.
        [[TwoPartString('st', 'ar')], [TwoPartString('st', 'ar')], ['star']],
        [
            [TwoPartString('s', 'amename'), TwoPartString('sam', 'ename'), TwoPartString('samen', 'ame')],
            [TwoPartString('s', 'amename'), TwoPartString('sam', 'ename'), TwoPartString('samen', 'ame')],
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
            [TwoPartString('', 'eclipse'), TwoPartString('ecl', 'ipse')],
            [TwoPartString('', 'autumn'), TwoPartString('aut', 'umn')],
            ['eclautumn', 'auteclipse', 'eclumn', 'autipse']
        ],
        [
            [TwoPartString('spr', 'ing'), TwoPartString('spring', '')],
            [TwoPartString('w', 'inter'), TwoPartString('winter', '')],
            ['sprinter', 'wing', 'wintering', 'springinter']
        ],
        [
            [TwoPartString('', '')],
            [TwoPartString('', '')],
            []
        ],

        # Parts that connect on the same letter shouldn't be added, unless there
        # are no other combinations.
        [
            [TwoPartString('qu', 'ail')],
            [TwoPartString('v', 'ulture'), TwoPartString('vult', 'ure')],
            ['vail', 'vultail']
        ],
        [
            [TwoPartString('QU', 'AIL')],
            [TwoPartString('V', 'ULTURE'), TwoPartString('VULT', 'URE')],
            ['VAIL', 'VULTAIL']
        ],
        [
            [TwoPartString('ea', 'gle')],
            [TwoPartString('seag', 'ull')],
            ['eaull']
        ],
        [
            [TwoPartString('', 'ural owl')],
            [TwoPartString('qu', 'ail')],
            ['quural owl']
        ],
        [
            [TwoPartString('qu', 'ail')],
            [TwoPartString('', 'ural owl')],
            ['quural owl']
        ],
        [
            [TwoPartString('qu', 'ail')],
            [TwoPartString('', 'ural owl'), TwoPartString('', 'ural owl')],
            ['quural owl']
        ],
        [
            [TwoPartString('', 'ural owl'), TwoPartString('', 'ural owl')],
            [TwoPartString('qu', 'ail')],
            ['quural owl']
        ]

    ])
    def test_get_name_combinations(self, first_name, second_name, combinations):
        result = pair_names.get_name_combinations(first_name, second_name)

        print(result)

        self.assertEqual(len(result), len(combinations))
        for name in result:
            self.assertIn(name, result)

class TestMain(unittest.TestCase):

    @parameterized.expand([
        [
            ['file_name.py', 'wm', 'ks', 'pairs.exe'],

            TwoPartString('Wallis', 'Metz'),
            TwoPartString('Keira', 'Schuchard'),

            [TwoPartString('W', 'allis')],
            [TwoPartString('M', 'etz')],
            [TwoPartString('K', 'eira')],
            [TwoPartString('Sch', 'uchard')],

            ['Weira', 'Kallis'],
            ['Muchard', 'Schetz'],

            'Weira',
            'Muchard'
        ],
        [
            ['file_name.py', 'sw', 'ms', 'pears.sh'],

            TwoPartString('Seong-Ho', 'Van Wegberg'),
            TwoPartString('Min', 'Van Der Stoep'),

            [TwoPartString('S', 'eong-Ho')],
            [TwoPartString('Van W', 'egberg')],
            [TwoPartString('M', 'in')],
            [TwoPartString('Van Der St', 'oep')],

            ['Sin', 'Meong-Ho'],
            ['Van Woep', 'Van Der Stegberg'],

            'Meong-Ho',
            'Van Der Stegberg'
        ],
    ])
    def test_main(
        self, 
        arguments, 
        first_name, 
        second_name, 
        expected_parsed_first_name_first_name,
        expected_parsed_first_name_last_name,
        expected_parsed_second_name_first_name,
        expected_parsed_second_name_last_name,
        expected_first_name_combinations,
        expected_last_name_combinations,
        chosen_first_name, 
        chosen_last_name):

        expected_first_initials = arguments[1]
        expected_second_initials = arguments[2]
        expected_file_path = arguments[3]

        def parse_name_side_effect(name):
            return_values = {
                first_name.first_part: expected_parsed_first_name_first_name,
                first_name.second_part: expected_parsed_first_name_last_name,
                second_name.first_part: expected_parsed_second_name_first_name,
                second_name.second_part: expected_parsed_second_name_last_name
            }
            return return_values[name]


        with patch('sys.argv', arguments):
            with patch('pair_names.get_names_from_file') as get_names_from_file_mock:
                with patch('pair_names.parse_name') as parse_name_mock:
                    with patch('pair_names.get_name_combinations') as get_name_combinations_mock:
                        with patch('random.choice') as choice_mock:
                            get_names_from_file_mock.return_value = {
                                'first_name': first_name,
                                'second_name': second_name
                            }

                            parse_name_mock.side_effect = parse_name_side_effect

                            get_name_combinations_mock.side_effect = [expected_first_name_combinations, expected_last_name_combinations]

                            choice_mock.side_effect = [chosen_first_name, chosen_last_name]

                            result = pair_names.main()

                            get_names_from_file_mock.assert_called_once_with(
                                expected_first_initials, 
                                expected_second_initials, 
                                expected_file_path
                            )

                            parse_name_mock.assert_any_call(first_name.first_part)
                            parse_name_mock.assert_any_call(first_name.second_part)
                            parse_name_mock.assert_any_call(second_name.first_part)
                            parse_name_mock.assert_any_call(second_name.second_part)

                            get_name_combinations_mock.assert_any_call(
                                expected_parsed_first_name_first_name, 
                                expected_parsed_second_name_first_name
                            )
                            get_name_combinations_mock.assert_any_call(
                                expected_parsed_first_name_last_name, 
                                expected_parsed_second_name_last_name
                            )

                            choice_mock.assert_any_call(expected_first_name_combinations)
                            choice_mock.assert_any_call(expected_last_name_combinations)

                            self.assertEqual(result, chosen_first_name + ' ' + chosen_last_name)

    @parameterized.expand([
        [
            ['file_name.py', 'sb', 'na', 'numbers.jpg'],
            TwoPartString('Sari', 'Bengoechea'),
            None,
            'Sari Bengoechea'
        ],
        [
            ['file_name.py', 'cm', 'xx', 'letters.png'],
            TwoPartString('Corwin', 'El-Mofty'),
            None,
            'Corwin El-Mofty'
        ],
        [
            ['file_name.py', 'qw', 'ku', 'doom.wad'],
            None,
            TwoPartString('Kaoru', 'Ulfsson'),
            'Kaoru Ulfsson'
        ],
        [
            ['file_name.py', 'er', 'as', 'misc.xml'],
            None,
            TwoPartString('Asenath', 'De Santiago'),
            'Asenath De Santiago'
        ],
        [
            ['file_name.py', 'gg', 'cx', 'build.gradle'],
            None,
            None,
            ''
        ],
        [
            ['file_name.py', 'za', 'op', 'build.gradle'],
            None,
            None,
            ''
        ],
    ])
    def test_main_missing_name_from_file(self, arguments, first_name, second_name, expected_name):
        with patch('sys.argv', arguments):
            with patch('pair_names.get_names_from_file') as get_names_from_file_mock:
                with patch('pair_names.parse_name') as parse_name_mock:
                    with patch('pair_names.get_name_combinations') as get_name_combinations_mock:
                        with patch('random.choice') as choice_mock:
                            get_names_from_file_mock.return_value = {
                                'first_name': first_name,
                                'second_name': second_name
                            }

                            result = pair_names.main()

                            parse_name_mock.assert_not_called()
                            get_name_combinations_mock.assert_not_called()
                            choice_mock.assert_not_called()

                            self.assertEqual(result, expected_name)

    @parameterized.expand([
        [
            TwoPartString('Ignace', ''),
            TwoPartString('Vulfgang', 'Kumar'),

            [TwoPartString('Ign', 'ace')],
            [TwoPartString('Vulfg', 'ang')],

            ['Ignang', 'Vulfgace']
        ]
    ])
    def test_main_last_name_doesnt_exist(
        self, 
        first_name, 
        second_name, 
        expected_parsed_first_name_first_name, 
        expected_parsed_second_name_first_name,
        first_name_combinations):

        arguments = ['file_name.py', 'ab', 'cd' 'efghijklmnopqrstuvwxyz.gif']

        def parse_name_side_effect(name):
            return_values = {
                first_name.first_part: expected_parsed_first_name_first_name,
                second_name.first_part: expected_parsed_second_name_first_name,
            }
            return return_values[name]

        with patch('sys.argv', arguments):
            with patch('pair_names.get_names_from_file') as get_names_from_file_mock:
                with patch('pair_names.parse_name') as parse_name_mock:
                    with patch('pair_names.get_name_combinations') as get_name_combinations_mock:
                        with patch('random.choice') as choice_mock:
                            get_names_from_file_mock.return_value = {
                                'first_name': first_name,
                                'second_name': second_name
                            }

                            parse_name_mock.side_effect = parse_name_side_effect

                            get_name_combinations_mock.return_value = first_name_combinations

                            pair_names.main()

                            self.assertEqual(parse_name_mock.call_count, 2)
                            parse_name_mock.assert_called_with(first_name.first_part)
                            parse_name_mock.assert_called_with(second_name.first_part)







if __name__ == '__main__':
    unittest.main()