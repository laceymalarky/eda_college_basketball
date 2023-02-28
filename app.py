# %%
import pandas as pd
from matplotlib import pyplot as plt
import streamlit as st

# %%
# Load data from https://barttorvik.com/trank.php#
# http://barttorvik.com/2023_team_results.csv
#data = pd.read_csv('/Users/laceymalarky/Downloads/2023_team_results.csv', index_col=False)

#url = 'http://barttorvik.com/2023_team_results.csv'
#response = requests.get(url).content 
#data_test = pd.read_csv(io.StringIO(response.decode('utf-8')))

data = pd.read_csv('http://barttorvik.com/2023_team_results.csv', index_col = False)
data.head()


# %%
data.shape

# %%
data.info()

# %%
data.columns

# %%
#Filter dataframe for only certain cols
data = data[['rank', 'team', 'conf', 'record', 'adjoe', 'adjde',
       'sos', 'consos', 'Conf Win%', 'Fun Rk, adjt']]

# %%
# Create a scatterplot of offense vs defense
data.plot(x = 'adjoe', y = 'adjde', kind = 'scatter')

# %%
# Test correlation for fun
data['adjoe'].corr(data['adjde'])

# %%
# List of unique conferences
data['conf'].unique()

# %%
#creating header with an option to filter the data and the checkbox:
#dataset includes all teams but this will let users decide whether they want
#to see all teams or just those in the top 10 conferences

st.header("NCAA Men's Backetball Statistics")
st.write("""
##### Filter the data below to see only team in the top 10 conferences
""")
conf_top_10 = st.checkbox('Top 10 Conferences Only')


# %%
conf_top_10

# %%
top10_conf = ['B12', 'SEC', 'B10', 'BE', 'P12', 'ACC', 'MWC', 'Amer', 'WCC', 'A10']

if not conf_top_10:
    data = data.query('conf in @top10_conf')

# %%
#creating options for filter from all teams and different years
team_choice = data['team'].unique()
make_choice_team = st.selectbox('Select team:', team_choice)

# %%
make_choice_team

# %%
#filtering dataset on chosen team and ...
filtered_type=data[(data.team==make_choice_team)]

#showing the final table in streamlit
st.table(filtered_type)

# %%
data

# %%
st.header('Team analysis')
st.write("""
###### Let's analyze what influences price the most. We will check how distibution of price varies depending on 
transmission, engine or body type and state
""")

import plotly.express as px

# Will create histograms with the split by parameter of choice: color, transmission, engine_type, body_type, state

#creating list of options to choose from
list_for_hist=['Conf Win%','consos']

#creating selectbox
choice_for_hist = st.selectbox('Split for price distribution', list_for_hist)

#plotly histogram, where price_usd is split by the choice made in the selectbox
fig1 = px.histogram(data, x=choice_for_hist)

#adding tittle
fig1.update_layout(
title="<b> Split of price by {}</b>".format(choice_for_hist))

#embedding into streamlit
st.plotly_chart(fig1)

# %%
fig1.show()

# %%
st.write("""
###### Now let's check how price is affected by odometer, engine capacity or number of photos in the adds
""")

#Distribution of price depending on odometer_value,engine_capacity,number_of_photos
#with the split by age category

#list_for_scatter=['odometer_value','engine_capacity','number_of_photos']
#choice_for_scatter = st.selectbox('Price dependency on ', list_for_scatter)
fig2 = px.scatter(data, x="adjoe", y='adjde',hover_data=['team'])

fig2.update_layout(
title="<b> Offense vs Defense</b>")
st.plotly_chart(fig2)

# %%
fig2

# %%
#streamlit run streamlit_workshop.py

# %%


# %%
data['Conf Win%'].plot(kind = 'hist')


# %%
data['consos'].plot(kind = 'hist')


# %%


# %%
data.plot(x = 'Conf Win%', y = 'consos', kind = 'scatter')

# %%
data_top10_conf.boxplot(column = 'rank', by = 'conf')


