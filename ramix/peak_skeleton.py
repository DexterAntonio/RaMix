from dataclasses import dataclass


@dataclass
class PeakSkeleton:
    wavenumber: float
    amplitude: float
    width: float
    idenity: str = None
