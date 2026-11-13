from .risk import assess
from .safety import decide
from .explain import explain

def process(observations, sensor_ok=True):
    assessments = [assess(o) for o in observations]
    decision = decide(observations, assessments, sensor_ok=sensor_ok)
    explanation = explain(observations, assessments, decision)
    return assessments, decision, explanation
