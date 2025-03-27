import streamlit as st
import fastf1
import datetime
from helpers import *
import seaborn as sns
from matplotlib import pyplot as plt
import fastf1.plotting
import plotly.express as px
from plotly.io import show

st.set_page_config(
    page_title="F1 App",
    page_icon="👋",
    layout="wide"
)

selected_year = st.selectbox('Race Year',years)
schedule = fastf1.get_event_schedule(selected_year)
selected_race = st.selectbox('Country',schedule['Country'][1:])
selected_session = st.selectbox('Session',session_types)

session = fastf1.get_session(selected_year,selected_race,session_map[selected_session])
session.load()
laps_df = session.laps.pivot(index='Driver', columns='LapNumber',values='LapTime').applymap(convert_to_time_format)


st.markdown(
    """Lap Time Detail"""
)

st.dataframe(laps_df.fillna(''), height=500)

st.markdown(
    """Lap Time Heat Map"""
)

#
#
# HEATMAP
# 
# 

heatmap_df = session.laps.pivot(index='Driver', columns='LapNumber',values='LapTime')
fig = px.imshow(
    heatmap_df,
    text_auto=True,
    aspect='auto',  # Automatically adjust the aspect ratio
    color_continuous_scale=[[0,    'rgb(198, 219, 239)'],  # Blue scale
                            [0.25, 'rgb(107, 174, 214)'],
                            [0.5,  'rgb(33,  113, 181)'],
                            [0.75, 'rgb(8,   81,  156)'],
                            [1,    'rgb(8,   48,  107)']],
    labels={'x': 'Time',
            'y': 'Driver',
            'color': 'Time'}       # Change hover texts
)
fig.update_xaxes(title_text='')      # Remove axis titles
fig.update_yaxes(title_text='')
fig.update_yaxes(tickmode='linear')  # Show all ticks, i.e. driver names
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey',
                 showline=False,
                 tickson='boundaries')              # Show horizontal grid only
fig.update_xaxes(showgrid=False, showline=False)    # And remove vertical grid
fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')     # White background
fig.update_layout(coloraxis_showscale=False)        # Remove legend
fig.update_layout(xaxis=dict(side='top'))           # x-axis on top
fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))  # Remove border margins
st.plotly_chart(fig, key="Heatmap Plot")


#
#
# Violen Chart
# 
# 



st.markdown(
    """Lap Times Visualized"""
)

# Enable Matplotlib patches for plotting timedelta values and load
# FastF1's dark color scheme
fastf1.plotting.setup_mpl(mpl_timedelta_support=True, misc_mpl_mods=False,
                          color_scheme='fastf1')

###############################################################################
# Get all the laps for the point finishers only.
# Filter out slow laps (yellow flag, VSC, pitstops etc.)
# as they distort the graph axis.
point_finishers = session.drivers[:10]
print(point_finishers)
driver_laps = session.laps.pick_drivers(point_finishers).pick_quicklaps()
driver_laps = driver_laps.reset_index()

finishing_order = [session.get_driver(i)["Abbreviation"] for i in point_finishers]
print(finishing_order)

###############################################################################
# First create the violin plots to show the distributions.
# Then use the swarm plot to show the actual laptimes.

# create the figure
fig, ax = plt.subplots(figsize=(10, 5))

# Seaborn doesn't have proper timedelta support,
# so we have to convert timedelta to float (in seconds)
driver_laps["LapTime(s)"] = driver_laps["LapTime"].dt.total_seconds()

sns.violinplot(data=driver_laps,
               x="Driver",
               y="LapTime(s)",
               hue="Driver",
               inner=None,
               density_norm="area",
               order=finishing_order,
               palette=fastf1.plotting.get_driver_color_mapping(session=session)
               )

sns.swarmplot(data=driver_laps,
              x="Driver",
              y="LapTime(s)",
              order=finishing_order,
              hue="Compound",
              palette=fastf1.plotting.get_compound_mapping(session=session),
              hue_order=["WET","INTERMEDIATE","SOFT", "MEDIUM", "HARD"],
              linewidth=0,
              size=4,
              )
# sphinx_gallery_defer_figures

###############################################################################
# Make the plot more aesthetic
ax.set_xlabel("Driver")
ax.set_ylabel("Lap Time (s)")
plt.suptitle(session)
sns.despine(left=True, bottom=True)

plt.tight_layout()
st.pyplot(plt)