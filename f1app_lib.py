import pandas as pd
import fastf1
import datetime

years = list(range(2018,datetime.datetime.now().year+1))
years.reverse()
session_types = ['Practice 1', 'Practice 2', 'Practice 3', 'Qualifying', 'Sprint','Sprint Qualifying','Race','SS']
session_map = {"Practice 1": "FP1", "Practice 2": "FP2", "Practice 3": "FP3", "Qualifying": "Q", "Race": "R", "Sprint Qualifying": "SQ", "Sprint": "S", "SS": "SS"}

def get_schedule():
    schedule = fastf1.get_event_schedule(2021)
    return schedule

def convert_to_time_format(td):
    if pd.isna(td):  # Handle NaT values
        return "NaT"
    total_seconds = td.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int((total_seconds % 1) * 1000)
    return f"{minutes:02}:{seconds:02}:{milliseconds:03}"