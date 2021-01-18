
#!/usr/bin/python3.6

# library modules
from jira import JIRA
from datetime import datetime as dt
import csv

# plot imports
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px

from itertools import chain


df = pd.read_csv('JiraSprintChangeLog.csv')
df.sort_values(by=['To_Done'])
df['To_Done'] = pd.to_datetime(df['To_Done']);
df.sort_values(by=['To_Done'])

dfResult = df.groupby(['Team','Sprint_Name'], as_index=False)['Cycle_Time'].median()
print(dfResult)

dfResult.columns = ['Team','Sprint','Median_CT']

# plot cycle time by team by sprint
fig = px.bar(dfResult, x="Team", y="Median_CT", color="Sprint")
fig.show()

dfResult.to_csv("mattBS.csv", index=False)
# plot cycle time by sprint
fig = px.scatter(df, x="To_Done", y="Cycle_Time", color="Sprint Name", hover_data=['Key'])
fig.show()

# plot cycle time by sprint
fig = px.bar(df, x="Team", y=df["Cycle_Time"], color="Sprint Name", hover_data=['Team'])
fig.show()


############################################################
# START PLOTTING 
############################################################
# SCATTER PLOT
############################################################
# populate data frame with defect data
# dfStory = df.loc[df['IssueType'] == "Story"] 
# dfDefect = df.loc[df['IssueType'] == "Defect"] 

# dfStory.sort_values(by=['To_Done'])
# storyCount = len(dfStory.index)
# print("Story Count: " + str(storyCount))

# # populate data frame with defect data
# dfDefect.sort_values(by=['To_Done'])
# defectCount = len(dfDefect.index)
# print("Defect Count: " + str(defectCount))

# totalRowCount = storyCount + defectCount

# print("Total Count: " + str(defectCount + storyCount))

# fig = go.Figure()

# fig.add_trace(go.Scatter(
#     x=dfStory["To_Done"],
#     y=dfStory["Cycle_Time"],
#     mode="markers",
#     name="Story" + "(" + str(storyCount) + ")",
#     hovertext=dfStory["HrefURL"]
# ))

# fig.add_trace(go.Scatter(
#     x=dfDefect["To_Done"],
#     y=dfDefect["Cycle_Time"],
#     mode="markers",
#     name="Defect" + "(" + str(defectCount) + ")",
#     hovertext=dfDefect["HrefURL"]
# ))

# fig.update_layout(
#     title="<b>IDeaS: Cycle Time Report for " + str(dfStory.iat[0,14]) + "</b><br>",
#     xaxis_title="Date Completed (Total Count = " + str(totalRowCount) + ")" ,
#     yaxis_title="Cycle Time (Days)",
#     legend_title="Issue Type",
#     font=dict(
#         family="Courier New, monospace",
#         size=14,
#         color="Black"
#     ),
#     hoverlabel=dict(bgcolor="white", font_size=12,font_family="Rockwell")
# )

# fig.show()

# ############################################################
# #  PLOT - MEDIAN BY TEAM using Aggregations
# ############################################################
# data = [dict(
#   type = 'bar',
#   x = df["Team"],
#   y = df["Cycle_Time"],
#   mode = 'markers',
#   transforms = [dict(
#     type = 'aggregate',
#     groups = df["Team"],
#     aggregations = [dict(
#         target = 'y', func = 'median', enabled = True),
#     ]
#   )]
# )]

# layout = dict(
#   title = '<b>Cycle Time By Team</b><br>Aggregated by Median Days',
#   xaxis = dict(title = 'G3 Teams'),
#   yaxis = dict(title = 'Median Cycle Time (Days)')
# )

# fig_dict = dict(data=data, layout=layout)

# pio.show(fig_dict, validate=False)

# ############################################################
# #  PLOT - MEDIAN FOR ALL (i.e. Sprint)  using Aggregations
# ############################################################

# data = [dict(
#   type = 'bar',
#   x = df["Sprint Name"],
#   y = df["Cycle_Time"],
#   mode = 'markers',
#   transforms = [dict(
#     type = 'aggregate',
#     groups = df["Sprint Name"],
#     aggregations = [dict(
#         target = 'y', func = 'median', enabled = True),
#     ]
#   )]
# )]

# layout = dict(
#   title = '<b>Cycle Time For G3 (All Teams)</b><br>Aggregated by Median Days',
#   xaxis = dict(title = 'G3 Teams (All)'),
#   yaxis = dict(title = 'Median Cycle Time (Days)')
# )

# fig_dict = dict(data=data, layout=layout)

# pio.show(fig_dict, validate=False)

# ############################################################
# #  SAVE DATA FRAME TO A CSV FILE
# ############################################################
# #df.to_csv("JiraSprintChangeLog.csv", index=False)
