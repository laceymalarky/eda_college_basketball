# %%
import pandas as pd
from matplotlib import pyplot as plt
import streamlit as st
import plotly.express as px


# %%
# Load team data from https://barttorvik.com/trank.php#
# http://barttorvik.com/2023_team_results.csv

teams = pd.read_csv(
    'http://barttorvik.com/2023_team_results.csv', index_col=False)
teams2 = pd.read_csv('http://barttorvik.com/2023_fffinal.csv', index_col=False)
teams2.head()


# %%
# Read Player data
players_header = ['player_name', 'team', 'conf', 'GP', 'Min_per', 'ORtg', 'usg', 'eFG', 'TS_per', 'ORB_per', 'DRB_per', 'AST_per', 'TO_per',
                  'FTM', 'FTA', 'FT_per', 'twoPM', 'twoPA', 'twoP_per', 'TPM', 'TPA', 'TP_per', 'blk_per', 'stl_per', 'ftr', 'yr', 'ht', 'num',
                  'porpag', 'adjoe', 'pfr', 'year', 'pid', 'type', 'Rec Rank', ' ast/tov', ' rimmade', ' rimmade+rimmiss', ' midmade', ' midmade+midmiss',
                  ' rimmade/(rimmade+rimmiss)', ' midmade/(midmade+midmiss)', ' dunksmade', ' dunksmiss+dunksmade', ' dunksmade/(dunksmade+dunksmiss)',
                  ' pick', ' drtg', 'adrtg', ' dporpag', ' stops', ' bpm', ' obpm', ' dbpm', ' gbpm', 'mp', 'ogbpm', 'dgbpm', 'oreb', 'dreb', 'treb',
                  'ast', 'stl', 'blk', 'pts']

players = pd.read_csv('http://barttorvik.com/getadvstats.php?year=2023&csv=1',
                      names=players_header, index_col=False)
players.head()

# %%
teams.head()

# %%
# Filter dataframe for only certain cols
teams = teams[['rank', 'team', 'conf', 'record', 'adjoe', 'adjde', 'barthag',
               'sos', 'consos', 'Conf Win%', 'Fun Rk, adjt']]

# %%
# List of unique conferences
teams['conf'].unique()

# %%
# creating header with an option to filter the data and the checkbox:
# dataset includes all teams but this will let users decide whether they want
# to see all teams or just those in the top 10 conferences

st.header("2023 NCAA Men's Basketball Statistics")
st.write("""
##### T-Rank based on offensive and defensive efficiency from https://barttorvik.com/trank.php#
""")
st.write("""
##### Filter the data below to see only team in the top 10 conferences
""")
conf_top_10 = st.checkbox('Top 10 Conferences Only')


# %%
conf_top_10

# %%
top10_conf = ['B12', 'SEC', 'B10', 'BE',
              'P12', 'ACC', 'MWC', 'Amer', 'WCC', 'A10']

if not conf_top_10:
    teams = teams.query('conf in @top10_conf')


# %%
# Select box for Conference
conf_choice = teams['conf'].unique()
make_choice_conf = st.selectbox('Select team:', conf_choice)

# %%
# filtering dataset on chosen team and ...
filtered_conf = teams[(teams.conf == make_choice_conf)]

# %%
# showing the final table in streamlit
st.table(filtered_conf)

# %%
# Add rank grouping


def rank_group(rank):
    if rank <= 25:
        return 'Top 25'
    elif rank <= 100:
        return '26 - 100'
    elif rank <= 200:
        return '101 - 200'
    else:
        return '201 +'


# %%
# Add col to data with rank group
teams['rank_desc'] = teams['rank'].apply(rank_group)

# %%
st.header('Team analyis by rank')
st.write("""
###### Now let's check how price is affected by odometer, engine capacity or number of photos in the adds
""")

# Distribution of price depending on odometer_value,engine_capacity,number_of_photos
# with the split by age category

# list_for_scatter=['odometer_value','engine_capacity','number_of_photos']
# choice_for_scatter = st.selectbox('Price dependency on ', list_for_scatter)
fig1 = px.scatter(teams, x="adjoe", y='adjde',
                  hover_data=['team'], color='rank_desc')

fig1.update_layout(
    title="<b> Offense vs Defense</b>")
st.plotly_chart(fig1)

# %%
# data_top10_conf.boxplot(column = 'rank', by = 'conf')

# %%
st.header('Player analysis')
st.write("""
###### Let's analyze what influences price the most. We will check how distibution of price varies depending on 
transmission, engine or body type and state
""")

# creating options for filter from all teams
team_choice = teams['team'].unique()
make_choice_team1 = st.selectbox('Select team 1:', team_choice)
make_choice_team2 = st.selectbox('Select team 2:', team_choice)

# filtering dataset on chosen team and ...
filtered_team = players[(players['team'] == make_choice_team1) | (
    players['team'] == make_choice_team2)]

# Will create histograms with the split by parameter of choice: color, transmission, engine_type, body_type, state

# creating list of options to choose from
list_for_hist = [' bpm', ' obpm', ' dbpm', ' gbpm', 'mp', 'ogbpm',
                 'dgbpm', 'oreb', 'dreb', 'treb', 'ast', 'stl', 'blk', 'pts']

# creating selectbox
choice_for_hist = st.selectbox('Player Metrics', list_for_hist)

# plotly histogram, where price_usd is split by the choice made in the selectbox
fig3 = px.histogram(filtered_team, x=choice_for_hist, color='team')

# adding tittle
fig3.update_layout(
    title="<b> Split of price by {}</b>".format(choice_for_hist))

# embedding into streamlit
st.plotly_chart(fig3)

# %%
# cd git_projects/practicum_sprint4_project
# streamlit run app.py
