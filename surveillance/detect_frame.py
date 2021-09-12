from dataclasses import dataclass
from typing import Any
import time
import numpy as np

@dataclass
class DetectFrame:
    frame: np.ndarray
    time: float
    