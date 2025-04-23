from enum import Enum

class ExtractionStrategy(Enum):
    ALWAYS = "always"
    BATCH = "batch"
    HEURISTIC = "heuristic"

    @staticmethod
    def from_str(label: str) -> "ExtractionStrategy":
        label = label.lower()
        for strategy in ExtractionStrategy:
            if strategy.value == label:
                return strategy
        raise ValueError(f"Unknown strategy: {label}")
