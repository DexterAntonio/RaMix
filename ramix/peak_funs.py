import numpy as np

from ramix.peak_skeleton import PeakSkeleton


def lorentzian(x_data: np.ndarray, p0: float, a: float, w: float) -> np.ndarray:
    """Generates a single lorenzian peak at a given location

    Args:
        x_data (np.ndarray): an array of x_data to add the spectra too 
        p0 (float): peak location 
        a (float): amplitude of the peak 
        w (float): width of the peak

    Returns:
        np.ndarray: spectra with single peak  
    """    
    assert p0<max(x_data) , ("peak value greater than max x value")
    u = (x_data - p0)/(w/2)
    L = a/(1 + u**2) 
    return L

def gaussian(x_data: np.ndarray, p0: float, a: float, w: float) -> np.ndarray:
    """Generates a single gaussian peak at a given location

    Args:
        x_data (np.ndarray): an array of x_data to add the spectra too 
        p0 (float): peak location 
        a (float): amplitude of the peak 
        w (float): width of the peak

    Returns:
        np.ndarray: spectra with single peak  
    """    
    assert p0<max(x_data) , ("peak value greater than max x value")
    u = (x_data - p0)/(w/2)
    L = np.exp(-np.log(2)*u**2)
    return L

def lorentzian_wrapper(x_data: np.ndarray, peak_skeleton: PeakSkeleton):
    return lorentzian(x_data, peak_skeleton.wavenumber, peak_skeleton.amplitude, peak_skeleton.width)