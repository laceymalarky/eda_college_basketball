# %% [markdown]
# ### Initialization

# %%
# Load packages
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import lxml
from datetime import date

# %% [markdown]
# ### Load data

# %%
# Web scrape html from url to get NCAA ratings for the current season
today = date.today()
year = today.year

url = ('https://www.sports-reference.com/cbb/seasons/men/{}-ratings.html').format(year)
html = pd.read_html(url, header=0, skiprows=1)
df = html[0]
# Deletes repeating headers in content
raw = df.drop(df[(df.Rk == 'Rk') | (df.OSRS == 'SRS')].index)
teamstats = raw.drop(['Rk', 'Unnamed: 3', 'Unnamed: 10',
                     'Unnamed: 12'], axis=1)  # Deletes empty columns

# %% [markdown]
# ### Data Preprocessing

# %%
# Set index to school name
teamstats = teamstats.set_index('School')

# %%
# Change data types
teamstats = teamstats.astype({'W': 'int', 'L': 'int', 'Pts': 'float', 'Opp': 'float',
                              'MOV': 'float', 'SOS': 'float', 'OSRS': 'float', 'DSRS': 'float', 'SRS': 'float',
                              'ORtg': 'float', 'DRtg': 'float', 'NRtg': 'float'})


# %%
# Rename columns
teamstats.columns = ['Conference', 'AP_rank', 'Wins', 'Losses', 'Points_per_game', 'Opponent_points_per_game', 'Margin_of_victory', 'Strength_of_schedule', 'Offensive_SRS', 'Defensive_SRS',
                     'SRS', 'Adj_offensive_rating', 'Adj_defensive_rating', 'Adj_net_rating']

# %%
# Classify top 25 and unranked groups


def rank_group(rank):
    if rank is np.nan:
        return 'Unranked'
    else:
        return 'Top 25'


# Add new col to dataframe
teamstats['Ranking'] = teamstats['AP_rank'].apply(rank_group)

# %% [markdown]
# ### Create Streamlit Elements

# %%
# creating title/header with an option to filter the data with a checkbox:
# dataset includes all teams but this will let users decide whether they want
# to see all teams or just those in the AP Poll's top 25

st.title(f"{year-1}-{year} Men's College Basketball Ratings")
st.markdown("""
This app performs web scraping of NCAA Division I men's basketball team statistics for the current season.
* **Data Source:** https://www.sports-reference.com/cbb/
* **Definitions:**
    * **Simple Rating System (SRS)** takes into account average point differential and strength of schedule, separated into offensive and defensive components. The rating is denominated in points above/below average, where zero is average.
    * **Adjusted Rating** is adjusted for strength of opposition. The offensive rating is an estimate of points scored per 100 possessions; defensive rating is an estimate of points allowed per 100 possessions; net rating is an estimate of point differential per 100 possessions.

    *Non-Division I games are excluded from the ratings.*
""")

ranked = st.checkbox('Filter the page to only include AP Top 25 Teams')

if ranked:
    teamstats = teamstats[teamstats.Ranking == 'Top 25']


# %% [markdown]
# ### Data Table

# %%
# Create data table filterable by conference

# creating options for filter from all conferences
conference_choice = list(teamstats['Conference'].unique())

conference_choice_all = []
conference_choice_all = conference_choice[:]
conference_choice_all.append('All')

# conference_dropdown = st.multiselect('Conference: ', conference_choice_all)
conference_dropdown = st.selectbox(
    'Select a Conference: ', conference_choice_all, index=len(conference_choice_all)-1)

# filtering dataset on chosen conference
if 'All' in conference_dropdown:
    filtered_conf = teamstats[teamstats.Conference.isin(conference_choice_all)]
else:
    filtered_conf = teamstats[teamstats.Conference == conference_dropdown]

st.header('Display Team Statistics')
st.write('Data Dimensions: ' +
         str(filtered_conf.shape[0]) + ' rows and ' + str(filtered_conf.shape[1]) + ' columns.')
st.dataframe(filtered_conf)

# %% [markdown]
# ### Scatterplot

# %%
st.header('Compare Offensive and Defensive Ratings')
st.write("""
###### Analyze the Simple Rating System (SRS) split into offensive and defensive components for unranked and top 25 teams
""")

fig1 = px.scatter(teamstats, x="Offensive_SRS", y='Defensive_SRS',
                  hover_data=[teamstats.index], color='Ranking')

st.plotly_chart(fig1)

# %% [markdown]
# ### Histogram

# %%
st.header('How do Conferences Compare?')
st.markdown("""
1. Select multiple conferences
2. Select a statistic
3. Compare data distributions
""")

# create multiselect for conferences
comparison = st.multiselect('Select Conferences: ',
                            conference_choice_all, default='All')

# filtering dataset on chosen conference
if 'All' in comparison:
    filtered_comp = teamstats[teamstats.Conference.isin(conference_choice_all)]
else:
    filtered_comp = teamstats[teamstats.Conference.isin(comparison)]


# creating list of options to choose from
list_for_hist = ['Points_per_game', 'Opponent_points_per_game', 'Margin_of_victory', 'Strength_of_schedule', 'Offensive_SRS', 'Defensive_SRS',
                 'SRS', 'Adj_offensive_rating', 'Adj_defensive_rating', 'Adj_net_rating']

# creating selectbox
choice_for_hist = st.selectbox('Select a Statistic', list_for_hist)

# plotly histogram by selected metric  split by the choice of conferences in selectbox, ALL by default
fig2 = px.histogram(filtered_comp, x=choice_for_hist, color='Conference')

# adding tittle
fig2.update_layout(
    title="<b> {} split by Selected Conferences</b>".format(choice_for_hist))

# embedding into streamlit
st.plotly_chart(fig2)

# %%
# cd git_projects/practicum_sprint4_project
# streamlit run app.py
