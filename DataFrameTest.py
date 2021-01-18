
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

df = pd.read_csv('JiraSprintChangeLog.csv')

# set df data types
df["To_Defined"] =  pd.to_datetime(df["To_Defined"], format="%m/%d/%Y %H:%M:%S")
df["To_Submitted"] =  pd.to_datetime(df["To_Submitted"], format="%m/%d/%Y %H:%M:%S")
df["To_InProgress"] =  pd.to_datetime(df["To_InProgress"], format="%m/%d/%Y %H:%M:%S")
df["To_CodeReview"] =  pd.to_datetime(df["To_CodeReview"], format="%m/%d/%Y %H:%M:%S")
df["To_InTesting"] =  pd.to_datetime(df["To_InTesting"], format="%m/%d/%Y %H:%M:%S")
df["To_ReadyForTesting"] =  pd.to_datetime(df["To_ReadyForTesting"], format="%m/%d/%Y %H:%M:%S")
df["To_Fixed"] =  pd.to_datetime(df["To_Fixed"], format="%m/%d/%Y %H:%M:%S")
df["To_Accepted"] =  pd.to_datetime(df["To_Accepted"], format="%m/%d/%Y %H:%M:%S")
df["To_Done"] =  pd.to_datetime(df["To_Done"], format="%m/%d/%Y %H:%M:%S")

df['minDate'] = df[['To_Defined', 'To_Submitted', 'To_InProgress', 'To_CodeReview', 'To_InTesting', 'To_ReadyForTesting', 'To_Fixed', 'To_Accepted']].min(axis=1)
df["minDate"] =  pd.to_datetime(df["minDate"], format="%m/%d/%Y %H:%M:%S")

df['minDateCycleTime'] = (df['To_Done'] - df['minDate']).dt.days

for ind in df.index:
    if (df['Cycle_Time'][ind]) <=0 and (pd.isnull(df.loc[ind, 'minDate'])) :
        df['Cycle_Time'][ind] = 1
        print(df['Cycle_Time'][ind], pd.isnull(df.loc[ind, 'minDate'])) 
    else :
        df['Cycle_Time'][ind] = df['minDateCycleTime'][ind] 
        print(df['Cycle_Time'][ind])

df.to_csv("JiraSprintChangeLog-OUTPUT.csv", index=False)

# ############################################################
# # START PLOTTING 
# ############################################################
# # SCATTER PLOT
# ############################################################
# # populate data frame with defect data
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

############################################################
#  SAVE DATA FRAME TO A CSV FILE
############################################################
#df.to_csv("JiraSprintChangeLog.csv", index=False)
