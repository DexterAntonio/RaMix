from dataclasses import dataclass
from typing import List, Dict

from ramix.peak_skeleton import PeakSkeleton


@dataclass
class SpectrumSkeleton:
    name: str
    peak_list: List[PeakSkeleton]

    @classmethod
    def make_spectrum_skeleton(cls, species_name: str, peak_dict_list: List[Dict]) -> "SpectrumSkeleton":
        name = species_name
        peak_list: List[PeakSkeleton] = []
        for peak_dict in peak_dict_list:
            peak_list.append(PeakSkeleton(**peak_dict))

        return cls(name, peak_list)








