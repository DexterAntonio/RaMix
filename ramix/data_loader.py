import json
from typing import List, Union

from ramix.spectrum_skeleton import SpectrumSkeleton


class DataLoader:
    """
    A class to load in the spectrum skeletons from their json file(s)
    """
    def __init__(self, file_paths: Union[str, List[str]]):
        """
        Create a data loader class

        Args:
            file_paths (Union[str, List[str]]): List of file paths
        """
        if isinstance(file_paths, str):
            file_paths = [file_paths]
        self.file_paths: List[str] = file_paths
        self.spectrum_skeletons: List[SpectrumSkeleton] = []
        for filepath in self.file_paths:
            self.spectrum_skeletons.extend(self.read_json(filepath))

    @staticmethod
    def read_json(filepath: str) -> List[SpectrumSkeleton]:
        """
        Read in the data from a spectrum skeleton json path
        Args:
            filepath (str): Single filepath to a json file

        Returns: a list of spectrum skeletons
        """
        with open(filepath, 'r') as f:
            mixture_data = json.load(f)

        spectrum_skeletons: List[SpectrumSkeleton] = []

        for species_name, peak_dict_list in mixture_data['Species'].items():
            spectrum_skeletons.append(SpectrumSkeleton.make_spectrum_skeleton(species_name, peak_dict_list))

        return spectrum_skeletons



