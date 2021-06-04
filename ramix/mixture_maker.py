import json
import os
from functools import partial
from pathlib import Path
from typing import Union, List, Dict, Tuple, OrderedDict

import numpy as np

from ramix.data_loader import DataLoader
from ramix.noise_maker import NoiseMaker
from ramix.noisy_spectrum_maker import NoisySpectrumMaker
from ramix.peak_funs import lorentzian_wrapper


class MixtureMaker:
    def __init__(self, file_paths: Union[str, List[str]], noise_dict: Dict[str, List[float]], output_dir: str = None) -> None:
        """
        Create a class that generates and saves random mixture spectra in numpy arrays.
        Args:
            file_paths (Union[str, List[str]):  path(s) to the spectrum skeleton json file
            noise_dict (Dict[str, List[float]]): A dictionary defining the different parameters to try
            output_dir (str): output directory to export the numpy arrays to
        """
        data_loader = DataLoader(file_paths)
        self.spectrum_skeletons = data_loader.spectrum_skeletons
        self.permutation_dict = self.make_permutations(noise_dict)
        self.noise_maker_dict: Dict[str, NoiseMaker] = {}
        if output_dir is None:
            self.output_dir = os.getcwd()
        else:
            self.output_dir = output_dir

        for key, perm in self.permutation_dict.items():
            self.noise_maker_dict[key] = NoiseMaker(**perm)

        self.chemical_names = self.get_chemical_names()
        self.chemical_names_map = {}
        for index, name in enumerate(self.chemical_names):
            self.chemical_names_map[name] = index

    def make_y(self, y_dict: OrderedDict[str, float]) -> np.array:
        """
        Creates a numpy array from a dictionary of concentrations
        Args:
            y_dict (OrderedDict): convert a concentration dictionary to a numpy array

        Returns: a numpy array of concentrations

        """
        y = np.zeros(len(self.chemical_names))
        for name, amount in y_dict.items():
            y[self.chemical_names_map[name]] = amount
        return y

    def make_datasets(self, key: str) -> Tuple[np.array, np.array]:
        """
        Generate X and y 2d arrays using generate_mixture_spectrum dataset
        Args:
            key (str): key to select specific noise maker dict

        Returns: Tuple of X and y for the mixture datasets

        """
        nsm = NoisySpectrumMaker(partial(np.random.uniform, 0, 1), lorentzian_wrapper, 200, 2000, 1)
        noise_maker = self.noise_maker_dict[key]
        perm_params = self.permutation_dict[key]
        n = int(perm_params['size'])
        X = np.zeros((n, len(nsm.wavenumbers)))
        y = np.zeros((n, len(self.chemical_names)))
        for i in range(n):
            x, y_dict = nsm.generate_mixture_spectrum(self.spectrum_skeletons, noise_maker)
            X[i, :] = x
            y[i, :] = self.make_y(y_dict)

        return X, y

    def generate_all(self) -> None:
        """
        Generate all of the unique permutations of parameters from the internal noise maker dict and save the
        datasets in their own unique folder.

        Returns: None
        """
        for key in self.permutation_dict.keys():
            print(f'making {key}')
            X, y = self.make_datasets(key)
            output_folder = Path(self.output_dir).joinpath(key)
            output_folder.mkdir(exist_ok=True, parents=True)
            output_X = output_folder.joinpath('X.npy')
            output_y = output_folder.joinpath('y.npy')
            output_species = output_folder.joinpath('species_indices.json')
            np.save(output_X, X)
            np.save(output_y, y)
            with open(output_species, 'w') as f:
                json.dump(self.chemical_names_map, f)
            print(f"completed {key}")

    @staticmethod
    def make_permutations(noise_dict: Dict[str, List[float]]) -> Dict[str, Dict[str, float]]:
        """
        Make (almost) all permutations of the specified noise dict and return a list of all permutations.
        The noise for the wavenumber, amplitude, and width are currently treated together to reduce the
        number of permutations created.
        Args:
            noise_dict (Dict[str, List[float]]): A mixture of different parameters to try

        Returns: A list of all possible permutations

        """
        permutation_dict: Dict[str, Dict[str, float]] = {}
        for size in noise_dict['size']:
            for wavenumber_std, amplitude_std, width_std in zip(noise_dict['wavenumber_noise'],
                                                                noise_dict['amplitude_noise'],
                                                                noise_dict['width_noise']):
                for add_baseline in noise_dict['add_baseline']:
                    key_str = 'size_' + str(size) + '_wn_std_' + str(wavenumber_std) + '_amp_std_' \
                              + str(amplitude_std) +str('_width_std_') + str(width_std) + '_add_baseline_' \
                              + str(add_baseline)
                    permutation_dict[key_str] = {'size': size,
                                                 'wavenumber_std': wavenumber_std,
                                                 'amplitude_std': amplitude_std,
                                                 'width_std': width_std,
                                                 'add_baseline': add_baseline}
        return permutation_dict

    def get_chemical_names(self) -> List[str]:
        """
        Get the names of all of the chemicals involved in the mixture creation
        Returns: List of all of the chemical names
        """
        return [c.name for c in self.spectrum_skeletons]

    def get_component_spectra(self) -> Dict[str, np.array]:
        """
        Get a dictionary of the individual component spectra
        Returns: A dictionary of the component spectra
        """
        nsm = NoisySpectrumMaker(partial(np.random.uniform, 0, 1), lorentzian_wrapper, 200, 2000, 1)
        return nsm.get_component_spectra(self.spectrum_skeletons)

    def get_wavenumbers(self) -> np.array:
        nsm = NoisySpectrumMaker(partial(np.random.uniform, 0, 1), lorentzian_wrapper, 200, 2000, 1)
        return nsm.wavenumbers



