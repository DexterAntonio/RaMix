from copy import deepcopy
from functools import partial

import numpy as np

from ramix.spectrum_skeleton import SpectrumSkeleton


class NoiseMaker:
    def __init__(self, wavenumber_std: float, amplitude_std: float, width_std: float, add_baseline: bool, *args,
                 **kwargs) -> None:
        self.wavenumber_noise = partial(np.random.normal, 0.0, wavenumber_std)
        self.amplitude_noise = partial(np.random.lognormal, 1, amplitude_std)
        self.width_noise = partial(np.random.lognormal, 1, width_std)
        self.add_baseline = add_baseline

    def add_noise(self, spectrum_skeleton: SpectrumSkeleton) -> SpectrumSkeleton:
        spectrum_skeleton = deepcopy(spectrum_skeleton)
        for peak_skeleton in spectrum_skeleton.peak_list:
            peak_skeleton.wavenumber = peak_skeleton.wavenumber + self.wavenumber_noise()
            peak_skeleton.amplitude = peak_skeleton.amplitude*self.amplitude_noise()
            peak_skeleton.width = peak_skeleton.width*self.width_noise()
        return spectrum_skeleton

