# %%
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# %% [markdown]
# ### Initialization

# %%
# Load data from url
url = 'https://www.sports-reference.com/cbb/seasons/men/2023-ratings.html'
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
# teamstats['AP Rank'] = round(teamstats['AP Rank'],0)

# %%
# Rename columns
teamstats.columns = ['Conference', 'AP_rank', 'Wins', 'Losses', 'Points_per_game', 'Opponent_points_per_game', 'Margin_of_victory', 'Strength_of_schedule', 'Offensive_SRS', 'Defensive_SRS',
                     'SRS', 'Adj_offensive_rating', 'Adj_defensive_rating', 'Adj_net_rating']

# %%
# Classify top 25 and unranked groups


def rank_group(rank):
    if rank is np.NaN:
        return 'Unranked'
    else:
        return 'Top 25'


# Add new col to dataframe
teamstats['Ranking'] = teamstats['AP_rank'].apply(rank_group)

# %%
# creating header with an option to filter the data with a checkbox:
# dataset includes all teams but this will let users decide whether they want
# to see all teams or just those in the AP Poll's top 25

st.header("2022-23 Men's College Basketball Ratings")
st.markdown("""
* **Data Source:** https://www.sports-reference.com
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

# %% [markdown]
# ### Scatterplot

# %%
st.header('Compare Offensive and Defensive Ratings')
st.write("""
###### Analyze offensive and defensive ratings for unranked and top 25 teams
""")

fig1 = px.scatter(teamstats, x="Offensive_SRS", y='Defensive_SRS',
                  hover_data=[teamstats.index], color='Ranking')

fig1.update_layout(
    title="<b> Simple Rating System (SRS) split into offensive and defensive components</b>")
st.plotly_chart(fig1)

# %% [markdown]
# ### Histogram

# %%
st.header('Compare Ratings by Conference')
st.write("""
###### Select multiple conferences to compare
""")

# create multiselect for conferences
comparison = st.multiselect(
    'Conferences to compare: ', conference_choice_all, default='All')

# filtering dataset on chosen conference
if 'All' in comparison:
    filtered_comp = teamstats[teamstats.Conference.isin(conference_choice_all)]
else:
    filtered_comp = teamstats[teamstats.Conference.isin(comparison)]


# creating list of options to choose from
list_for_hist = ['Points_per_game', 'Opponent_points_per_game', 'Margin_of_victory', 'Strength_of_schedule', 'Offensive_SRS', 'Defensive_SRS',
                 'SRS', 'Adj_offensive_rating', 'Adj_defensive_rating', 'Adj_net_rating']

# creating selectbox
choice_for_hist = st.selectbox('Select a Metric', list_for_hist)

# plotly histogram by selected metric  split by the choice of conferences in selectbox, ALL by default
fig2 = px.histogram(filtered_comp, x=choice_for_hist, color='Conference')

# adding tittle
fig2.update_layout(
    title="<b> {} split by Selected Conferences</b>".format(choice_for_hist))

# embedding into streamlit
st.plotly_chart(fig2)

# %% [markdown]
# ### Glossary

# %%
# Add glossary of terms
st.text("""
###### Glossary:
* Simple Rating System (SRS):
    * A rating that takes into account average point differential and strength of schedule, separated into offensive and defensive components. The rating is denominated in points above/below average, where zero is average.
* Adjusted Rating:
    * A rating adjusted for strength of opposition.
    * Offensive Rating - an estimate of points scored (for teams) or points produced (for players) per 100 possessions.
    * Defensive Rating - an estimate of points allowed per 100 possessions.
    * Net Rating - an estimate of point differential per 100 possessions.

*Non-Division I games are excluded from the ratings.*
""")

# %%
# cd git_projects/practicum_sprint4_project
# streamlit run app.py
