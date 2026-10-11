
import streamlit as st

st.set_page_config(
    page_title="AeroLink Nepal",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ AeroLink Nepal")
st.subheader("Airport Communication & Surveillance Network Simulator")

st.info("Version 0.1 | Educational Simulation")

st.write("Welcome to AeroLink Nepal!")

st.header("Engineering Modules")

modules = [
    "Digital Communication",
    "Network Monitor",
    "Wireless Link Analyzer",
    "Aircraft Surveillance Simulator",
    "Reliability and Failover"
]

selected_module = st.selectbox(
    "Choose a module:",
    modules
)

st.success(f"Selected Module: {selected_module}")

st.write("This module is currently under development.")
