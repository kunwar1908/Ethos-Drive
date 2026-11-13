from dataclasses import dataclass, asdict
from typing import Optional

@dataclass(frozen=True)
class Observation:
    label: str
    confidence: float
    distance_m: Optional[float] = None
    closing_speed_mps: Optional[float] = None
    source: str = "synthetic"
    bbox: Optional[tuple] = None

    def to_dict(self):
        return asdict(self)

@dataclass(frozen=True)
class Assessment:
    label: str
    risk: float
    severity: str
    reasons: tuple
    confidence: float

@dataclass(frozen=True)
class Decision:
    action: str
    explanation: str
    fallback: bool
