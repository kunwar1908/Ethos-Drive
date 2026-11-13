
import os
import tempfile
import streamlit as st
import pandas as pd
import plotly.express as px
from ethos_drive.synthetic import SCENARIOS, get_scenario
from ethos_drive.pipeline import process
from ethos_drive.logger import EventLogger

st.set_page_config(page_title="ETHOS DRIVE", page_icon="🚘", layout="wide")
st.title("ETHOS DRIVE")
st.caption("Explainable Ethical Traffic-Scenario Simulator · Educational prototype · No real vehicle control")
logger = EventLogger()
mode = st.sidebar.radio("Input mode", ["Synthetic", "Video"])


def display_result(observations, assessments, decision, explanation):
    a, b, c = st.columns(3)
    a.metric("Observations", len(observations))
    b.metric("Peak heuristic risk", f"{max((x.risk for x in assessments), default=0):.2f}")
    c.metric("Fallback", "YES" if decision.fallback else "NO")
    st.subheader(decision.action)
    st.write(decision.explanation)
    if assessments:
        df = pd.DataFrame([{"Object": x.label, "Risk": x.risk, "Severity": x.severity, "Confidence": x.confidence} for x in assessments])
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.plotly_chart(px.bar(df, x="Object", y="Risk", color="Severity", range_y=[0, 1]), use_container_width=True)
    with st.expander("Explainability / reasoning", expanded=True):
        st.text(explanation)

if mode == "Synthetic":
    scenario = st.selectbox("Select scenario", list(SCENARIOS))
    st.write("The distances and relative speeds in synthetic scenarios are invented demonstration inputs.")
    if st.button("Run synthetic scenario", type="primary"):
        observations = get_scenario(scenario)
        sensor_ok = scenario != "Sensor unavailable"
        assessments, decision, explanation = process(observations, sensor_ok)
        logger.record("synthetic", scenario, observations, assessments, decision)
        display_result(observations, assessments, decision, explanation)
else:
    st.info("Video detections supply object classes and confidence only. Distance and relative speed are unknown; scores are NOT collision predictions.")
    upload = st.file_uploader("Upload video", type=["mp4", "mov", "avi", "mkv"])
    max_frames = st.slider("Maximum sampled frames", 1, 60, 12)
    stride = st.slider("Sample every Nth frame", 1, 60, 15)
    if upload and st.button("Analyze video", type="primary"):
        if upload.size > 100 * 1024 * 1024:
            st.error("Maximum upload size for this demo is 100 MB.")
        else:
            suffix = os.path.splitext(upload.name)[1].lower()
            path = None
            try:
                with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp:
                    temp.write(upload.getbuffer())
                    path = temp.name
                from ethos_drive.video import analyze_video
                frames = analyze_video(path, max_frames=max_frames, stride=stride)
                if not frames:
                    st.warning("No readable frames found.")
                for number, observations, rgb in frames:
                    assessments, decision, explanation = process(observations)
                    logger.record("video", f"{upload.name}:frame-{number}", observations, assessments, decision)
                    with st.expander(f"Frame {number} — {decision.action}", expanded=(number == frames[0][0])):
                        st.image(rgb, channels="RGB", use_container_width=True)
                        display_result(observations, assessments, decision, explanation)
            except Exception as exc:
                st.error(f"Video analysis failed: {exc}")
            finally:
                if path and os.path.exists(path):
                    os.unlink(path)

st.divider()
st.subheader("Black-box event log")
rows = logger.recent(100)
if rows:
    st.dataframe(pd.DataFrame(rows).drop(columns=["details"]), use_container_width=True, hide_index=True)
    st.download_button("Export events as CSV", pd.DataFrame(rows).to_csv(index=False).encode(), "ethos_drive_events.csv", "text/csv")
else:
    st.caption("Run a scenario to populate the event log.")
