from .models import Observation

SCENARIOS = {
    "Clear road": [],
    "Pedestrian crossing": [Observation("person", .94, 9, 4)],
    "Cyclist nearby": [Observation("bicycle", .87, 14, 3)],
    "Stopped vehicle": [Observation("car", .97, 7, 5)],
    "Ambiguous detection": [Observation("person", .38, 8, 3)],
    "Multiple road users": [Observation("person", .91, 11, 3), Observation("bicycle", .83, 16, 2), Observation("car", .95, 24, 1)],
    "Sensor unavailable": [Observation("unknown", 0, None, None)],
}

def get_scenario(name):
    if name not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {name}")
    return list(SCENARIOS[name])
