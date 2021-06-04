from unittest import TestCase
from src.data_generation.mixture_maker import MixtureMaker
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt


class TestMixtureMaker(TestCase):
    def test_make_y(self):
        noise_dict = {'size': [1],
                      'wavenumber_noise': [2],
                      'amplitude_noise': [3],
                      'width_noise': [4],
                      'add_baseline': [True]}

        mix_maker = MixtureMaker('data/mix_data.json', noise_dict, 'output')
        chem_dict = {}
        for i, chem_name in enumerate(mix_maker.get_chemical_names()):
            chem_dict[chem_name] = i

        y = mix_maker.make_y(chem_dict)
        y_vals = np.array([i for i in range(len(mix_maker.get_chemical_names()))])
        self.assertCountEqual(y, y_vals)
        for y1, y2 in zip(y, y_vals):
            self.assertEqual(y1, y2)

    def test_make_datasets_plot(self):
        noise_dict = {'size': [1],
                      'wavenumber_noise': [1],
                      'amplitude_noise': [1],
                      'width_noise': [1],
                      'add_baseline': [True]}

        mix_maker = MixtureMaker('data/mix_data_sugars.json', noise_dict, 'output')
        X, y = mix_maker.make_datasets(list(mix_maker.permutation_dict.keys())[0])
        plt.plot(X[0,:])
        plt.show()


    def test_make_datasets(self):
        noise_dict = {'size': [1],
                      'wavenumber_noise': [2],
                      'amplitude_noise': [3],
                      'width_noise': [4],
                      'add_baseline': [True]}

        mix_maker = MixtureMaker('data/mix_data_sugars.json', noise_dict, 'output')
        X, y = mix_maker.make_datasets('size_1_wn_std_2_amp_std_3_width_std_4_add_baseline_True')
        self.assertEqual(X.shape, (1, 1800))
        self.assertEqual(y.shape, (1, 6))

    def test_generate_all(self):
        noise_dict = {'size': [2,3],
                      'wavenumber_noise': [2],
                      'amplitude_noise': [3],
                      'width_noise': [4],
                      'add_baseline': [True]}

        mix_maker = MixtureMaker('data/mix_data.json', noise_dict, 'output')
        mix_maker.generate_all()
        folders = [str(folder).split('/')[-1] for folder in Path(mix_maker.output_dir).glob('*')]
        self.assertCountEqual(mix_maker.permutation_dict.keys(), folders)


    def test_make_permutations(self):
        with self.subTest('test single permutation'):
            noise_dict = {'size': [1],
                          'wavenumber_noise': [2],
                          'amplitude_noise': [3],
                          'width_noise': [4],
                          'add_baseline': [True]}
            permutations = MixtureMaker.make_permutations(noise_dict)
            key = list(permutations.keys())[0]
            value = list(permutations.values())[0]
            self.assertEqual('size_1_wn_std_2_amp_std_3_width_std_4_add_baseline_True',
                             key)
            self.assertDictEqual({'size': 1,
                                  'wavenumber_std': 2,
                                  'amplitude_std': 3,
                                  'width_std': 4,
                                  'add_baseline': True}, value)

        with self.subTest('test multi permutation'):
            noise_dict = {'size': [1, 2],
                          'wavenumber_noise': [2],
                          'amplitude_noise': [3],
                          'width_noise': [4],
                          'add_baseline': [True]}
            permutations = MixtureMaker.make_permutations(noise_dict)
            key1 = list(permutations.keys())[0]
            key2 = list(permutations.keys())[1]
            value1 = list(permutations.values())[0]
            value2 = list(permutations.values())[1]
            self.assertEqual('size_1_wn_std_2_amp_std_3_width_std_4_add_baseline_True', key1)
            self.assertEqual('size_1_wn_std_2_amp_std_3_width_std_4_add_baseline_True', key2)
            self.assertDictEqual({'size': 1,
                                  'wavenumber_std': 2,
                                  'amplitude_std': 3,
                                  'width_std': 4,
                                  'add_baseline': True}, value1)

            self.assertDictEqual({'size': 2,
                                  'wavenumber_std': 2,
                                  'amplitude_std': 3,
                                  'width_std': 4,
                                  'add_baseline': True}, value2)

    def test_get_chemical_names(self):
        chemical_names = ['ethanol', 'glucose', 'water', 'gylcerol', 'lactic acid']
        noise_dict = {'size': [1],
                      'wavenumber_noise': [2],
                      'amplitude_noise': [3],
                      'width_noise': [4],
                      'add_baseline': [True]}

        mix_maker = MixtureMaker('data/mix_data.json', noise_dict, 'output')
        self.assertCountEqual(mix_maker.get_chemical_names(), chemical_names)

