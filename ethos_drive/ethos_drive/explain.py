def explain(observations, assessments, decision):
    lines = [f"Decision: {decision.action}", decision.explanation]
    if not observations:
        lines.append("No observations in this scene.")
    for o, a in zip(observations, assessments):
        lines.append(f"{o.label}: risk {a.risk:.2f} ({a.severity}); " + "; ".join(a.reasons))
    lines.append("Fairness note: decisions do not use personal identity or demographic characteristics.")
    lines.append("Limitations: scores are heuristic; video detections do not provide measured depth or velocity.")
    return "\n".join(lines)
