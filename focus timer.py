import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Focus Tracker")

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Task", "Target_Hours", "Focused_Hours"])
if "timer_start" not in st.session_state:
    st.session_state.timer_start = None
if "current_task" not in st.session_state:
    st.session_state.current_task = ""
if "current_target" not in st.session_state:
    st.session_state.current_target = 0.0

task_name = st.text_input("Task Name")
target_time = st.number_input("Target Hours", min_value=0.0, step=0.5)

col1, col2 = st.columns(2)
with col1:
    if st.button("Start Timer"):
        if task_name:
            st.session_state.current_task = task_name
            st.session_state.current_target = target_time
            st.session_state.timer_start = datetime.now()
            st.success(f"Timer started for task: {task_name}")
        else:
            st.warning("Enter a task name first!")

with col2:
    if st.button("Stop Timer"):
        if st.session_state.timer_start:
            elapsed = datetime.now() - st.session_state.timer_start
            total_seconds = int(elapsed.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            focused_str = f"{hours}h {minutes}m {seconds}s"
            st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([{
                "Task": st.session_state.current_task,
                "Target_Hours": st.session_state.current_target,
                "Focused_Hours": focused_str
            }])], ignore_index=True)
            st.success(f"Timer stopped! Focused time: {focused_str} on {st.session_state.current_task}")
            st.session_state.timer_start = None
            st.session_state.current_task = ""
            st.session_state.current_target = 0.0
        else:
            st.warning("Timer is not running!")

if st.session_state.timer_start:
    elapsed = datetime.now() - st.session_state.timer_start
    total_seconds = int(elapsed.total_seconds())
    if total_seconds > 0: 
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        st.info(f"Timer running: {hours}h {minutes}m {seconds}s")

if st.button("Generate Report"):
    if not st.session_state.data.empty:
        st.subheader("Task Report")
        st.dataframe(st.session_state.data)
    else:
        st.info("No tasks logged yet.")

