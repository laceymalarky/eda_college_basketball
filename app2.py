# %%
from datetime import date
import pandas as pd
from matplotlib import pyplot as plt
import streamlit as st
import plotly.express as px


# %%
# Create year variable that only pulls current season's file by assuming each season starts in November of the previous year
today = date.today()
if today.month >= 11:
    year = today.year + 1
else:
    year = today.year

# %%
# Load NCAA Basketball statistics from https://barttorvik.com/trank.php#
team_calc_stats = pd.read_csv(
    f'http://barttorvik.com/{year}_team_results.csv', index_col=False)  # Calculated statistics
# Raw performance statistics
team_game_stats = pd.read_csv(
    f'http://barttorvik.com/{year}_fffinal.csv', index_col=False)


# %%
print(team_calc_stats.shape)
print(team_game_stats.shape)

# %%
# Combine team stats dataframes
teams = team_calc_stats.set_index('team').join(
    team_game_stats.set_index('TeamName'))
teams = teams.reset_index()
print(teams.shape)

# %%
# Read Player data (headers retrieved from website)
players_header = ['player_name', 'team', 'conf', 'GP', 'Min_per', 'ORtg', 'usg', 'eFG', 'TS_per', 'ORB_per', 'DRB_per', 'AST_per', 'TO_per',
                  'FTM', 'FTA', 'FT_per', 'twoPM', 'twoPA', 'twoP_per', 'TPM', 'TPA', 'TP_per', 'blk_per', 'stl_per', 'ftr', 'yr', 'ht', 'num',
                  'porpag', 'adjoe', 'pfr', 'year', 'pid', 'type', 'Rec Rank', ' ast/tov', ' rimmade', ' rimmade+rimmiss', ' midmade', ' midmade+midmiss',
                  ' rimmade/(rimmade+rimmiss)', ' midmade/(midmade+midmiss)', ' dunksmade', ' dunksmiss+dunksmade', ' dunksmade/(dunksmade+dunksmiss)',
                  ' pick', ' drtg', 'adrtg', ' dporpag', ' stops', ' bpm', ' obpm', ' dbpm', ' gbpm', 'mp', 'ogbpm', 'dgbpm', 'oreb', 'dreb', 'treb',
                  'ast', 'stl', 'blk', 'pts']

players = pd.read_csv(
    f'http://barttorvik.com/getadvstats.php?year={year}&csv=1', names=players_header, index_col=False)
players.head()

# %%
# Filter dataframe for only certain cols
teams = teams[['rank', 'team', 'conf', 'record', 'adjoe', 'adjde', 'sos', 'consos', 'Conf Win%', 'Fun Rk, adjt',
               'eFG%', 'eFG% Def', 'FTR', 'FTR Def', 'OR%', 'DR%',  'TO%', 'TO% Def.', '3P%', '3pD%', '2p%',  '2p%D', 'ft%', 'ft%D']]

# %%
# Filtering top 10 conferences by rank/number of teams
# top10_conf = ['B12', 'SEC', 'B10', 'BE', 'P12', 'ACC', 'MWC', 'Amer', 'WCC', 'A10']

# top10_conf = teams.groupby('conf')['rank'].sum().div(teams.groupby('conf')['rank'].count()).sort_values(ascending=True)[:10]
# top10_conf = list(top10_conf.index)

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
conf_win_top25 = st.checkbox('Top 25% of Teams by Conference Win Percent')


# %%
# conf_win_top25

# %%
# Filtering top 25% of teams by conference win %
conf_win_Q3 = teams['Conf Win%'].quantile(.75)  # Calculate 3rd quartile
# filter df for teams >= 3rd quartile (top 25)
teams_conf_win_Q3 = teams[teams['Conf Win%'] >= conf_win_Q3]['team']
# teams_conf_win_Q3 = list(teams_conf_win_Q3['team']) #List of teams


if conf_win_top25:
    teams = teams[teams['Conf Win%'] >= conf_win_Q3]

# %%
# Select box for Conference
# conf_win_choice = teams_conf_win_q3
# make_choice_conf = st.selectbox('Select team:', conf_win_choice)

# %%
# filtering dataset on chosen team and ...
filtered_teams = teams[teams['team'].isin(teams_conf_win_Q3) == True]

# %%
# showing the final table in streamlit
st.dataframe(filtered_teams)

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
