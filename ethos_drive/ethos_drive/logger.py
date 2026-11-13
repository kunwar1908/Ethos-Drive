import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

class EventLogger:
    def __init__(self, path="data/events.sqlite3"):
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT NOT NULL, mode TEXT NOT NULL, scenario TEXT NOT NULL, action TEXT NOT NULL, fallback INTEGER NOT NULL, details TEXT NOT NULL)")

    def record(self, mode, scenario, observations, assessments, decision):
        payload = {
            "observations": [o.to_dict() for o in observations],
            "assessments": [dict(label=a.label, risk=a.risk, severity=a.severity, reasons=list(a.reasons), confidence=a.confidence) for a in assessments],
            "explanation": decision.explanation,
        }
        with sqlite3.connect(self.path) as db:
            db.execute("INSERT INTO events(created_at,mode,scenario,action,fallback,details) VALUES(?,?,?,?,?,?)", (datetime.now(timezone.utc).isoformat(), mode, scenario, decision.action, int(decision.fallback), json.dumps(payload)))

    def recent(self, limit=100):
        with sqlite3.connect(self.path) as db:
            db.row_factory = sqlite3.Row
            return [dict(r) for r in db.execute("SELECT * FROM events ORDER BY id DESC LIMIT ?", (limit,))]
