from unittest import TestCase
from src.data_generation.data_loader import DataLoader


class TestDataLoader(TestCase):
    def test_init(self):
        with self.subTest('test single file init'):
            dl = DataLoader('data/mix_data.json')
            names = [s.name for s in dl.spectrum_skeletons]
            self.assertCountEqual(['ethanol', 'glucose', 'water', 'gylcerol', 'lactic acid'],
                                  names)
            ss_ethanol = [s for s in dl.spectrum_skeletons if s.name == 'ethanol'][0]
            wavenumbers = [peak.wavenumber for peak in ss_ethanol.peak_list]
            self.assertCountEqual([1600, 1400, 1200, 1000, 900, 800, 400],
                                  wavenumbers)

        with self.subTest('test multi file init'):
            dl = DataLoader(['data/mix_data.json', 'data/mix_data_2.json'])
            names = [s.name for s in dl.spectrum_skeletons]
            self.assertCountEqual(['ethanol', 'glucose', 'water', 'gylcerol', 'lactic acid', 'fruit',
                                   'watermelon', 'apple', 'fish', 'cat'], names)
            ss_fruit = [s for s in dl.spectrum_skeletons if s.name == 'fruit'][0]
            wavenumbers = [peak.wavenumber for peak in ss_fruit.peak_list]
            self.assertCountEqual([1600, 1400, 1200, 1000, 900, 800, 400],
                                  wavenumbers)

    def test_read_json(self):
       with self.subTest('load single file'):
           spectrum_skeletons = DataLoader.read_json('data/mix_data.json')
           names = [s.name for s in spectrum_skeletons]
           self.assertCountEqual(['ethanol', 'glucose', 'water', 'gylcerol', 'lactic acid'],
                                 names)
           ss_ethanol = [s for s in spectrum_skeletons if s.name == 'ethanol'][0]
           wavenumbers = [peak.wavenumber for peak in ss_ethanol.peak_list]
           self.assertCountEqual([1600, 1400, 1200, 1000, 900, 800, 400],
                                 wavenumbers)

