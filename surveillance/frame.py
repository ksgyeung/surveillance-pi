from dataclasses import dataclass
import time
from typing import Any
import numpy as np

@dataclass
class Frame:
    frame: np.ndarray
    timestamp: float