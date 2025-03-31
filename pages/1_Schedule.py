import streamlit as st
import fastf1
import datetime
from f1app_lib import *

st.set_page_config(
    page_title="F1 App",
    page_icon="👋",
    layout="wide"
)

st.markdown(
    """Enter a year for race schedule"""
    
)

selected_year = st.selectbox('Race Year',years)
schedule = fastf1.get_event_schedule(selected_year)
st.dataframe(schedule)


st.markdown(
    """
"""
)