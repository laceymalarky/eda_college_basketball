# %%
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px


# %%


url = 'https://www.sports-reference.com/cbb/seasons/men/2023-ratings.html'
html = pd.read_html(url, header=0, skiprows=1)
df = html[0]
# Deletes repeating headers in content
raw = df.drop(df[(df.Rk == 'Rk') | (df.OSRS == 'SRS')].index)
teamstats = raw.drop(
    ['Rk', 'Unnamed: 3', 'Unnamed: 10', 'Unnamed: 12'], axis=1)

# %%
# Set index to school name
teamstats = teamstats.set_index('School')

# %%
# Change data types
teamstats = teamstats.astype({'W': 'int', 'L': 'int', 'Pts': 'float', 'Opp': 'float',
                              'MOV': 'float', 'SOS': 'float', 'OSRS': 'float', 'DSRS': 'float', 'SRS': 'float',
                              'ORtg': 'float', 'DRtg': 'float', 'NRtg': 'float'})
# teamstats['AP Rank'] = round(teamstats['AP Rank'],0)

# %%
teamstats.columns = ['Conference', 'AP_rank', 'Wins', 'Losses', 'Points_per_game', 'Opponent_points_per_game', 'Margin_of_victory', 'Strength_of_schedule', 'Offensive_SRS', 'Defensive_SRS',
                     'SRS', 'Adj_offensive_rating', 'Adj_defensive_rating', 'Adj_net_rating']

# %%


def rank_group(rank):
    if rank is np.NaN:
        return 'Unranked'
    else:
        return 'Top 25'


# Add col to data with rank group
teamstats['AP_rank_desc'] = teamstats['AP_rank'].apply(rank_group)

# %%
# creating header with an option to filter the data and the checkbox:
# dataset includes all teams but this will let users decide whether they want
# to see all teams or just those in the top 10 conferences

st.header("2022-23 Men's College Basketball Ratings")
st.markdown("""
* **Data Source:** https://www.sports-reference.com
""")


# %%
ranked = st.checkbox('Include only top 25')

# %%
if ranked:
    teamstats = teamstats[teamstats.AP_rank_desc == 'Top 25']

# %%

# creating options for filter from all conferences
conference_choice = list(teamstats['Conference'].unique())

conference_choice_all = []
conference_choice_all = conference_choice[:]
conference_choice_all.append('All')

# conference_dropdown = st.multiselect('Conference: ', conference_choice_all)
conference_dropdown = st.selectbox(
    'Conference: ', conference_choice_all, index=len(conference_choice_all)-1)

# filtering dataset on chosen conference
if 'All' in conference_dropdown:
    filtered_conf = teamstats[teamstats.Conference.isin(conference_choice_all)]
else:
    filtered_conf = teamstats[teamstats.Conference == conference_dropdown]

st.header('Display Team Stats for Selected Conference(s)')
st.write('Data Dimensions: ' +
         str(filtered_conf.shape[0]) + ' rows and ' + str(filtered_conf.shape[1]) + ' columns.')
st.dataframe(filtered_conf)


# %%
st.header('Placeholder header')
st.write("""
###### Now let's check how price is affected by odometer, engine capacity or number of photos in the adds
""")

# Distribution of price depending on odometer_value,engine_capacity,number_of_photos
# with the split by age category

# list_for_scatter=['odometer_value','engine_capacity','number_of_photos']
# choice_for_scatter = st.selectbox('Price dependency on ', list_for_scatter)
fig1 = px.scatter(teamstats, x="Offensive_SRS", y='Defensive_SRS', hover_data=[
                  teamstats.index], color='AP_rank_desc')

fig1.update_layout(
    title="<b> Offense vs Defense</b>")
st.plotly_chart(fig1)

# %%
st.header('Placeholder')
st.write("""
###### Placeholder
""")

# creating options for filter from all teams
conf_choice = teamstats['Conference'].unique()
make_choice1 = st.selectbox('Select team 1:', conf_choice)
make_choice2 = st.selectbox('Select team 2:', conf_choice)

# filtering dataset on chosen team and ...
filtered_teamstats = teamstats[(teamstats['Conference'] == make_choice1) | (
    teamstats['Conference'] == make_choice2)]

# Will create histograms with the split by parameter of choice: color, transmission, engine_type, body_type, state

# creating list of options to choose from
list_for_hist = ['Points_per_game', 'Opponent_points_per_game', 'Margin_of_victory', 'Strength_of_schedule', 'Offensive_SRS', 'Defensive_SRS',
                 'SRS', 'Adj_offensive_rating', 'Adj_defensive_rating', 'Adj_net_rating']

# creating selectbox
choice_for_hist = st.selectbox('Performance Metrics', list_for_hist)

# plotly histogram, where price_usd is split by the choice made in the selectbox
fig2 = px.histogram(filtered_teamstats, x=choice_for_hist, color='Conference')

# adding tittle
fig2.update_layout(
    title="<b> Split of stats by {}</b>".format(choice_for_hist))

# embedding into streamlit
st.plotly_chart(fig2)

# %%
st.markdown("""
###### Glossary:
* Simple Rating System (SRS):
    * A rating that takes into account average point differential and strength of schedule, separated into offensive and defensive components. The rating is denominated in points above/below average, where zero is average. 
* Adjusted:
    * A rating adjusted for strength of opposition.
    * Offensive Rating - an estimate of points scored (for teams) or points produced (for players) per 100 possessions.
    * Defensive Rating - an estimate of points allowed per 100 possessions.
    * Net Rating - an estimate of point differential per 100 possessions

**Non-Division I games are excluded from the ratings.**
""")

# %%
# cd git_projects/practicum_sprint4_project
# streamlit run newapp.py
