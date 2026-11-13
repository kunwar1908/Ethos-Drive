# ETHOS DRIVE

**Explainable Ethical Traffic-Scenario Simulator** — an educational, offline Python prototype. It is **not** an autonomous-driving controller and must never be connected to steering, braking, throttle, or other vehicle actuators.

## Requirements
- Python 3.10–3.12 recommended
- Windows, macOS or Linux
- Internet for installing packages; optional YOLO model download on first video run

## Installation

```bash
cd ethos_drive
python -m venv .venv
```

Activate the virtual environment:

- Windows PowerShell: `.venv\\Scripts\\Activate.ps1`
- Windows CMD: `.venv\\Scripts\\activate.bat`
- macOS/Linux: `source .venv/bin/activate`

Install the dashboard dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

For **both synthetic and video modes**, also install:

```bash
pip install -r requirements-video.txt
```

Launch:

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit (typically http://localhost:8501).

## Automated tests

```bash
python -m unittest discover -s tests -v
```

Tests use the standard library and require no model downloads.

## Modules

- `models.py`: typed observation, assessment and decision records
- `synthetic.py`: seven demonstration scenes
- `video.py`: optional YOLO detections on sampled uploaded video frames
- `risk.py`: transparent illustrative heuristic
- `safety.py`: uncertainty/sensor fallback and simulated action labels
- `explain.py`: human-readable explanations and limitations
- `logger.py`: SQLite audit/event history
- `pipeline.py`: orchestration
- `app.py`: Streamlit dashboard and CSV export

## Key limitations

- **Video detection is not distance estimation.** The demo deliberately marks distance and closing speed as unknown; no physical collision-risk prediction is claimed.
- YOLO detections may be wrong or biased; a confidence score is not calibrated probability of safety.
- The risk weights and thresholds are educational examples, not certified safety rules.
- No face recognition, demographic categorization, actuator interfaces, or live road deployment.
- First video run may download `yolov8n.pt` from Ultralytics. For fully offline video analysis, provision an authorized local model and change the model path in `video.py`.
- Do not upload sensitive videos without consent. Uploaded video is handled as a temporary local file; metadata about detections and the filename is saved in SQLite.

## Example demo
1. Select **Synthetic → Pedestrian crossing → Run synthetic scenario**.
2. Inspect risk score, simulated action, explanation and log entry.
3. Select **Synthetic → Ambiguous detection** to show uncertainty fallback.
4. Install video dependencies, select **Video**, upload a short clip and analyze sampled frames.
5. Export the event log as CSV.

## Future research extensions

Compare alternative ethical policy configurations on synthetic cases, evaluate false positives/negatives against labeled data, audit fairness using properly consented aggregate datasets, and document governance against relevant published principles. These are research directions, not claims of compliance.
