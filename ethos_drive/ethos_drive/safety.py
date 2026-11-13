from .models import Decision

MIN_CONFIDENCE = 0.55

def decide(observations, assessments, sensor_ok=True):
    """Produces text labels for simulation; never sends actuator commands."""
    if not sensor_ok:
        return Decision("SAFE FALLBACK (SIMULATED)", "Sensor input unavailable; request manual review of simulated scenario.", True)
    if any(o.confidence < MIN_CONFIDENCE for o in observations):
        return Decision("SAFE FALLBACK (SIMULATED)", "At least one detection is uncertain; avoid relying on an unsupported classification.", True)
    if not assessments:
        return Decision("NORMAL (SIMULATED)", "No objects detected in the current synthetic scene; absence of detections is not proof of safety.", False)
    worst = max(assessments, key=lambda a: a.risk)
    if worst.risk >= .70:
        action = "EMERGENCY RESPONSE (SIMULATED)"
    elif worst.risk >= .40:
        action = "REDUCE SPEED / CAUTION (SIMULATED)"
    else:
        action = "MONITOR (SIMULATED)"
    return Decision(action, f"Highest illustrative risk: {worst.label} ({worst.risk:.2f}, {worst.severity}).", False)
