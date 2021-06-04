from functools import partial
from typing import Callable, List, Dict, Tuple

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve

from ramix.noise_maker import NoiseMaker
from ramix.spectrum_skeleton import SpectrumSkeleton


class NoisySpectrumMaker:
    """
    A class that generates noisy spectra
    """
    def __init__(self, concentration_fun: Callable, peak_fun: Callable,
                 wavenumber_start: float, wavenumber_end: float, step_size: float):
        self.concentration_fun = concentration_fun
        self.peak_fun = peak_fun
        self.wavenumber_start = wavenumber_start
        self.wavenumber_end = wavenumber_end
        self.step_size = step_size
        self.wavenumbers = np.arange(self.wavenumber_start, self.wavenumber_end, self.step_size)

    def generate_mixture_spectrum(self, spectrum_skeletons: List[SpectrumSkeleton],
                                  noise_maker: NoiseMaker) -> Tuple[np.array, Dict[str, float]]:
        """
        Generates a noisy mixture spectrum
        Args:
            spectrum_skeletons (List[SpectrumSkeleton): A list of spectrum skeletons
            noise_maker (NoiseMaker): A noise maker object

        Returns:

        """

        concentration_dict: Dict[str, float] = {}
        mixture_spectrum = np.zeros(self.wavenumbers.shape)
        for spectrum_skeleton in spectrum_skeletons:
            noisy_spec_skeleton = noise_maker.add_noise(spectrum_skeleton)
            concentration_dict[spectrum_skeleton.name] = self.concentration_fun()
            mixture_spectrum += \
                self.generate_spectrum(noisy_spec_skeleton, self.peak_fun)*concentration_dict[spectrum_skeleton.name]

        if noise_maker.add_baseline:
            mixture_spectrum += self.random_baseline(len(mixture_spectrum))
        return mixture_spectrum, concentration_dict

    def generate_spectrum(self, spectrum_skeleton: SpectrumSkeleton, peak_fun: Callable) -> np.array:
        return sum(map(partial(peak_fun, self.wavenumbers), spectrum_skeleton.peak_list))

    def get_component_spectra(self, spectrum_skeletons: List[SpectrumSkeleton]) -> Dict[str, np.array]:
        """
        Get the individual component spectra
        Returns: The individual component spectra
        """
        component_spectra: Dict[str, np.array] = {}
        for spectrum_skeleton in spectrum_skeletons:
            component_spectra[spectrum_skeleton.name] = self.generate_spectrum(spectrum_skeleton, self.peak_fun)

        return component_spectra

    @staticmethod
    def random_baseline(x_length: int) -> np.array:
        """Generates a Random baseline

        Args:
            x_length (int): lenght of the baseline to ramix

        Returns:
            np.array: baseline of length x_length
        """

        def baseline_als(y, lam, p, niter=10):
            L = len(y)
            D = sparse.csc_matrix(np.diff(np.eye(L), 2))
            w = np.ones(L)
            for i in range(niter):
                W = sparse.spdiags(w, 0, L, L)
                Z = W + lam * D.dot(D.transpose())
                z = spsolve(Z, w * y)
                w = p * (y > z) + (1 - p) * (y < z)
            return z

        z_total = 0
        z = baseline_als(np.random.rand(x_length), 100, 1, niter=10)
        z_total += np.random.normal(size=z.shape)
        z_total += z / np.max(z) / 25  # np.log(abs(z)+0.01)
        return z_total



