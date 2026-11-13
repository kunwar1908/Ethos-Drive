from .models import Assessment

VULNERABLE = {"person", "bicycle", "motorcycle"}

def assess(observation):
    """Illustrative risk heuristic; NOT validated for physical control."""
    c = max(0.0, min(1.0, observation.confidence))
    reasons = []
    if observation.distance_m is None:
        proximity = 0.5
        reasons.append("distance unknown")
    else:
        proximity = max(0.0, min(1.0, (30.0 - observation.distance_m) / 30.0))
        reasons.append(f"estimated distance {observation.distance_m:.1f} m")
    if observation.closing_speed_mps is None:
        closing = 0.5
        reasons.append("relative speed unknown")
    else:
        closing = max(0.0, min(1.0, observation.closing_speed_mps / 10.0))
        reasons.append(f"illustrative closing speed {observation.closing_speed_mps:.1f} m/s")
    vulnerability = 1.0 if observation.label in VULNERABLE else 0.5
    uncertainty = 1.0 - c
    score = 0.40 * proximity + 0.25 * closing + 0.20 * vulnerability + 0.15 * uncertainty
    score = round(min(1.0, max(0.0, score)), 3)
    severity = "HIGH" if score >= .70 else "MEDIUM" if score >= .40 else "LOW"
    reasons.extend([f"class {observation.label}", f"detection confidence {c:.0%}"])
    return Assessment(observation.label, score, severity, tuple(reasons), c)
