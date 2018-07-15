import unittest, pair_names
from parameterized import parameterized
from pair_names import SplitName

class TestParseName(unittest.TestCase):

    @parameterized.expand([
        ['brian', [SplitName('br', 'ian')]],
        ['BRIAN', [SplitName('BR', 'IAN')]],
        ['katie', [
            SplitName('k', 'atie'), 
            SplitName('kat', 'ie')
        ]],
        ['blake', [SplitName('bl', 'ake')]],
        ['BLAKE', [SplitName('BL', 'AKE')]],
        ['kyle', [SplitName('k', 'yle')]],
        ['yani', [
            SplitName('y', 'ani'), 
            SplitName('yan', 'i')
        ]],
        ['YANI', [
            SplitName('Y', 'ANI'), 
            SplitName('YAN', 'I')
        ]],
        ['quigley', [
            SplitName('qu', 'igley'),
            SplitName('quigl', 'ey')
        ]],
        ['QUIGLEY', [
            SplitName('QU','IGLEY'),
            SplitName('QUIGL', 'EY')
        ]],
        ['ulo', [
            SplitName('', 'ulo'), 
            SplitName('ul', 'o')
        ]],
        ['ypsilanti', [
            SplitName('', 'ypsilanti'), 
            SplitName('yps', 'ilanti'), 
            SplitName('ypsil', 'anti'), 
            SplitName('ypsilant', 'i')
        ]],
        ['', []],
        ['a', []],
        ['b', []],
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
        ['quenya', [
            SplitName('qu', 'enya'),
            SplitName('queny', 'a')
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