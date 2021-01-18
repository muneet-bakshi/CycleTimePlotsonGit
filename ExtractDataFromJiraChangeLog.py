
#!/usr/bin/python3.6
import re

# library modules
from jira import JIRA
from jira.client import GreenHopper
from datetime import datetime as dt
import csv

# plot imports
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio



user = 'muneet.bakshi@ideas.com'
apikey = 'vzlLwxrxAGVeVIH4FM1iC304'
server = 'https://ideasinc.atlassian.net'

options = {
 'server': server
}

jira = JIRA(options, basic_auth=(user,apikey) )

###########################################
# create dataframe
###########################################
df = pd.DataFrame(columns=["HrefURL", "Key", "Team", "IssueType", "To_Defined", "To_Submitted", "To_InProgress", 
"To_CodeReview", "To_InTesting", "To_ReadyForTesting", "To_Fixed", "To_Accepted", "To_Done",  "Cycle_Time", "Sprint_Name"])
print(df.dtypes)

###########################################
# get the sprints from the G3 Scrum Board
###########################################
sprints = jira.sprints(52)
print(sprints)

for sprint in sprints :
    if ((sprint.name.find('[G3 Global]') != -1) and (sprint.name.find('Spillover') == -1) and (sprint.name.find('6.2 Iteration 3') == -1) and (sprint.name.find('6.2 Iteration 4') == -1)): 
        print("Contains given substring ") 
        print(sprint.name, sprint.id)
        #######################################
        # grab all the issues in the sprint
        #######################################
        block_size = 100
        block_num = 0
        while True:
            
            start_idx = block_num * block_size
            jql = 'Sprint in (' + str(sprint.id) + ') and issuetype in (Defect, Story)'
            #jql = 'Sprint = 252 and issuetype in (Defect, Story)'
            
            if block_num == 0:
                issues = jira.search_issues(jql, start_idx, block_size, expand='changelog')
            else:
                more_issue = jira.search_issues(jql, start_idx, block_size, expand='changelog')
                if len(more_issue)>0:
                    for x in more_issue:
                        issues.append(x)
                else:
                    break
            if len(issues) == 0:
                # Retrieve issues until there are no more to come
                break
            block_num += 1

        print(len(issues))

        ##############################################################################################################################################         
        # loop through the issues and grab the status transition timestamps
        ##############################################################################################################################################

        # for issue in issues:
        #     print('hi %s: %s' % (issue.key, issue.fields.summary))
            
        for issue in issues:
                if str(issue.fields.status) == "Done":
                    # print(f"Changes from issue: {issue.key} {issue.fields.summary}")
                    # print(f"Number of Changelog entries found: {issue.changelog.total}") # number of changelog entries (careful, each entry can have multiple field changes)

                    currentTimestamp = dt.now()
                    dtDoneStoredObject = dt.fromtimestamp(100000)
                    dtInProgressStoredObject = currentTimestamp
                    To_Defined_TimeStampDtObj = currentTimestamp
                    To_Submitted_TimeStampDtObj = currentTimestamp
                    To_CodeReview_TimeStampDtObj = currentTimestamp
                    To_InTesting_TimeStampDtObj = currentTimestamp
                    To_ReadyForTesting_TimeStampDtObj = currentTimestamp
                    To_Fixed_TimeStampDtObj = currentTimestamp
                    To_Accepted_TimeStampDtObj = currentTimestamp

                    for history in issue.changelog.histories:
                        for item in history.items:
                            if item.field == "status" and item.toString == "Done":
                                date_str=str(history.created)
                                date_obj = dt.strptime(date_str[0:19], "%Y-%m-%dT%H:%M:%S")
                                if date_obj > dtDoneStoredObject :
                                    dtDoneStoredObject = dt.fromtimestamp(date_obj.timestamp())
                                    
                            if item.field == "status" and item.toString == "In Progress":
                                date_str=str(history.created)
                                date_obj = dt.strptime(date_str[0:19], "%Y-%m-%dT%H:%M:%S")
                                if date_obj < dtInProgressStoredObject :
                                    dtInProgressStoredObject = dt.fromtimestamp(date_obj.timestamp())
                                    
                            if item.field == "status" and item.toString == "Defined":
                                date_str=str(history.created)
                                date_obj = dt.strptime(date_str[0:19], "%Y-%m-%dT%H:%M:%S")
                                if date_obj < To_Defined_TimeStampDtObj :
                                    To_Defined_TimeStampDtObj = dt.fromtimestamp(date_obj.timestamp())
                            
                            if item.field == "status" and item.toString == "Submitted":
                                date_str=str(history.created)
                                date_obj = dt.strptime(date_str[0:19], "%Y-%m-%dT%H:%M:%S")
                                if date_obj < To_Submitted_TimeStampDtObj :
                                    To_Submitted_TimeStampDtObj = dt.fromtimestamp(date_obj.timestamp())

                            if item.field == "status" and item.toString == "Code Review":
                                date_str=str(history.created)
                                date_obj = dt.strptime(date_str[0:19], "%Y-%m-%dT%H:%M:%S")
                                if date_obj < To_CodeReview_TimeStampDtObj :
                                    To_CodeReview_TimeStampDtObj = dt.fromtimestamp(date_obj.timestamp())
                            
                            if item.field == "status" and item.toString == "In Testing":
                                date_str=str(history.created)
                                date_obj = dt.strptime(date_str[0:19], "%Y-%m-%dT%H:%M:%S")
                                if date_obj < To_InTesting_TimeStampDtObj :
                                    To_InTesting_TimeStampDtObj = dt.fromtimestamp(date_obj.timestamp())
                            
                            if item.field == "status" and item.toString == "Ready For Testing":
                                date_str=str(history.created)
                                date_obj = dt.strptime(date_str[0:19], "%Y-%m-%dT%H:%M:%S")
                                if date_obj < To_ReadyForTesting_TimeStampDtObj :
                                    To_ReadyForTesting_TimeStampDtObj = dt.fromtimestamp(date_obj.timestamp())
                            
                            if item.field == "status" and item.toString == "Fixed":
                                date_str=str(history.created)
                                date_obj = dt.strptime(date_str[0:19], "%Y-%m-%dT%H:%M:%S")
                                if date_obj < To_Fixed_TimeStampDtObj :
                                    To_Fixed_TimeStampDtObj = dt.fromtimestamp(date_obj.timestamp())
                            
                            if item.field == "status" and item.toString == "Accepted":
                                date_str=str(history.created)
                                date_obj = dt.strptime(date_str[0:19], "%Y-%m-%dT%H:%M:%S")
                                if date_obj < To_Accepted_TimeStampDtObj :
                                    To_Accepted_TimeStampDtObj = dt.fromtimestamp(date_obj.timestamp())
                    
                    
                    #difference = dtDoneStoredObject - dtInProgressStoredObject
                    jiraURL = "https://ideasinc.atlassian.net/browse/" + issue.key
                    hrefURL = "<a href=\'" + jiraURL + "'\>"+ issue.key +"</a>"                            
                    team, value = issue.key.split("-",1)        

                    print(sprint.name)

                    # Write the row to the dataframe
                    #df.loc[len(df)] = [hrefURL] + [issue.key] + [team] + [issue.fields.issuetype.name] + [dt.strftime(To_Defined_TimeStampDtObj, '%m/%d/%Y %H:%M:%S')] + [dt.strftime(To_Submitted_TimeStampDtObj, '%m/%d/%Y %H:%M:%S')] + [dt.strftime(dtInProgressStoredObject, '%m/%d/%Y %H:%M:%S')] + [dt.strftime(To_CodeReview_TimeStampDtObj, '%m/%d/%Y %H:%M:%S')] + [dt.strftime(To_InTesting_TimeStampDtObj, '%m/%d/%Y %H:%M:%S')] + [dt.strftime(To_ReadyForTesting_TimeStampDtObj, '%m/%d/%Y %H:%M:%S')] + [dt.strftime(To_Fixed_TimeStampDtObj, '%m/%d/%Y %H:%M:%S')] + [dt.strftime(To_Accepted_TimeStampDtObj, '%m/%d/%Y %H:%M:%S')] + [dt.strftime(dtDoneStoredObject, '%m/%d/%Y %H:%M:%S')] + [1 if difference.days == 0 else difference.days] + [sprint.name]
                    df.loc[len(df)] = [hrefURL] + [issue.key] + [team] + [issue.fields.issuetype.name] + [dt.strftime(To_Defined_TimeStampDtObj, '%m/%d/%Y %H:%M:%S')] + [dt.strftime(To_Submitted_TimeStampDtObj, '%m/%d/%Y %H:%M:%S')] + [dt.strftime(dtInProgressStoredObject, '%m/%d/%Y %H:%M:%S')] + [dt.strftime(To_CodeReview_TimeStampDtObj, '%m/%d/%Y %H:%M:%S')] + [dt.strftime(To_InTesting_TimeStampDtObj, '%m/%d/%Y %H:%M:%S')] + [dt.strftime(To_ReadyForTesting_TimeStampDtObj, '%m/%d/%Y %H:%M:%S')] + [dt.strftime(To_Fixed_TimeStampDtObj, '%m/%d/%Y %H:%M:%S')] + [dt.strftime(To_Accepted_TimeStampDtObj, '%m/%d/%Y %H:%M:%S')] + [dt.strftime(dtDoneStoredObject, '%m/%d/%Y %H:%M:%S')] + ["0"] + [sprint.name.replace('[G3 Global]', '')]
                    print(df)

else: 
    print ("Doesn't contains given substring")  


##############################################################################################################################################         
# loop through the dataframe and remove cells that contain today's date. This indicates that the issue never transitioned throgh this state
##############################################################################################################################################
for ind in df.index: 
    date1 = df['To_Defined'].str[:10][ind]
    date2 = str(dt.now().date().strftime('%m/%d/%Y'))
    if date1 == date2 :
        df['To_Defined'][ind] = ""

for ind in df.index: 
    date1 = df['To_Submitted'].str[:10][ind]
    date2 = str(dt.now().date().strftime('%m/%d/%Y'))
    if date1 == date2 :
        df['To_Submitted'][ind] = ""

for ind in df.index: 
    date1 = df['To_InProgress'].str[:10][ind]
    date2 = str(dt.now().date().strftime('%m/%d/%Y'))
    if date1 == date2 :
        df['To_InProgress'][ind] = ""

for ind in df.index: 
    date1 = df['To_CodeReview'].str[:10][ind]
    date2 = str(dt.now().date().strftime('%m/%d/%Y'))
    if date1 == date2 :
        df['To_CodeReview'][ind] = ""

for ind in df.index: 
    date1 = df['To_InTesting'].str[:10][ind]
    date2 = str(dt.now().date().strftime('%m/%d/%Y'))
    if date1 == date2 :
        df['To_InTesting'][ind] = ""

for ind in df.index: 
    date1 = df['To_ReadyForTesting'].str[:10][ind]
    date2 = str(dt.now().date().strftime('%m/%d/%Y'))
    if date1 == date2 :
        df['To_ReadyForTesting'][ind] = ""

for ind in df.index: 
    date1 = df['To_Fixed'].str[:10][ind]
    date2 = str(dt.now().date().strftime('%m/%d/%Y'))
    if date1 == date2 :
        df['To_Fixed'][ind] = ""

for ind in df.index: 
    date1 = df['To_Accepted'].str[:10][ind]
    date2 = str(dt.now().date().strftime('%m/%d/%Y'))
    if date1 == date2 :
        df['To_Accepted'][ind] = ""

for ind in df.index: 
    date1 = df['To_Done'].str[:10][ind]
    date2 = str(dt.now().date().strftime('%m/%d/%Y'))
    if date1 == date2 :
        df['To_Done'][ind] = ""

###############################################################
# loop through the data frame for all negative cycle times and 
# recalculate the cycle time based on the earliest time stamp
# if there is only To_Done default cycle time to 1 day
################################################################
# set df data types
df["To_Defined"] =  pd.to_datetime(df["To_Defined"], format="%m/%d/%Y %H:%M:%S", errors='coerce')
df["To_Submitted"] =  pd.to_datetime(df["To_Submitted"], format="%m/%d/%Y %H:%M:%S", errors='coerce')
df["To_InProgress"] =  pd.to_datetime(df["To_InProgress"], format="%m/%d/%Y %H:%M:%S", errors='coerce')
df["To_CodeReview"] =  pd.to_datetime(df["To_CodeReview"], format="%m/%d/%Y %H:%M:%S", errors='coerce')
df["To_InTesting"] =  pd.to_datetime(df["To_InTesting"], format="%m/%d/%Y %H:%M:%S", errors='coerce')
df["To_ReadyForTesting"] =  pd.to_datetime(df["To_ReadyForTesting"], format="%m/%d/%Y %H:%M:%S", errors='coerce')
df["To_Fixed"] =  pd.to_datetime(df["To_Fixed"], format="%m/%d/%Y %H:%M:%S", errors='coerce')
df["To_Accepted"] =  pd.to_datetime(df["To_Accepted"], format="%m/%d/%Y %H:%M:%S", errors='coerce')
df["To_Done"] =  pd.to_datetime(df["To_Done"], format="%m/%d/%Y %H:%M:%S", errors='coerce')

df['minDate'] = df[['To_Defined', 'To_Submitted', 'To_InProgress', 'To_CodeReview', 'To_InTesting', 'To_ReadyForTesting', 'To_Fixed', 'To_Accepted']].min(axis=1)

df["minDate"] =  pd.to_datetime(df["minDate"], format="%m/%d/%Y %H:%M:%S")

df['Cycle_Time'] = (df['To_Done'] - df['minDate']).dt.days

for ind in df.index:
    if (pd.isnull(df.loc[ind, 'Cycle_Time']) or df['Cycle_Time'][ind] == 0 or df['Cycle_Time'][ind] == "" ):
        df['Cycle_Time'][ind] = 1
        

############################################################
#  SAVE DATA FRAME TO A CSV FILE
############################################################
df.to_csv("JiraSprintChangeLog.csv", index=False)

############################################################
# START PLOTTING 
############################################################
# SCATTER PLOT with Story & Defect Separated
############################################################
# populate data frame with defect data
dfStory = df.loc[df['IssueType'] == "Story"] 
dfDefect = df.loc[df['IssueType'] == "Defect"] 

dfStory.sort_values(by=['To_Done'])
storyCount = len(dfStory.index)
print("Story Count: " + str(storyCount))

# populate data frame with defect data
dfDefect.sort_values(by=['To_Done'])
defectCount = len(dfDefect.index)
print("Defect Count: " + str(defectCount))

totalRowCount = storyCount + defectCount

print("Total Count: " + str(defectCount + storyCount))

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=dfStory["To_Done"],
    y=dfStory["Cycle_Time"],
    mode="markers",
    name="Story" + "(" + str(storyCount) + ")",
    hovertext=dfStory["HrefURL"]
))

fig.add_trace(go.Scatter(
    x=dfDefect["To_Done"],
    y=dfDefect["Cycle_Time"],
    mode="markers",
    name="Defect" + "(" + str(defectCount) + ")",
    hovertext=dfDefect["HrefURL"]
))

fig.update_layout(
    title="<b>IDeaS: Cycle Time Report for " + str(dfStory.iat[0,14]) + "</b><br>",
    xaxis_title="Date Completed (Total Count = " + str(totalRowCount) + ")" ,
    yaxis_title="Cycle Time (Days)",
    legend_title="Issue Type",
    font=dict(
        family="Courier New, monospace",
        size=14,
        color="Black"
    ),
    hoverlabel=dict(bgcolor="white", font_size=12,font_family="Rockwell")
)

fig.show()


############################################################
#  PLOT - MEDIAN BY TEAM using Aggregations
############################################################
data = [dict(
  type = 'bar',
  x = df["Team"],
  y = df["Cycle_Time"],
  mode = 'markers',
  transforms = [dict(
    type = 'aggregate',
    groups = df["Team"],
    aggregations = [dict(
        target = 'y', func = 'median', enabled = True),
    ]
  )]
)]

layout = dict(
  title = '<b>Cycle Time By Team</b><br>Aggregated by Median Days',
  xaxis = dict(title = 'G3 Teams'),
  yaxis = dict(title = 'Median Cycle Time (Days)')
)

fig_dict = dict(data=data, layout=layout)

pio.show(fig_dict, validate=False)

############################################################
#  PLOT - MEDIAN FOR ALL (i.e. Sprint)  using Aggregations
############################################################

data = [dict(
  type = 'bar',
  x = df["Sprint_Name"],
  y = df["Cycle_Time"],
  mode = 'markers',
  transforms = [dict(
    type = 'aggregate',
    groups = df["Sprint_Name"],
    aggregations = [dict(
        target = 'y', func = 'median', enabled = True),
    ]
  )]
)]

layout = dict(
  title = '<b>Cycle Time For G3 (All Teams)</b><br>Aggregated by Median Days',
  xaxis = dict(title = 'G3 Teams (All)'),
  yaxis = dict(title = 'Median Cycle Time (Days)')
)

fig_dict = dict(data=data, layout=layout)

pio.show(fig_dict, validate=False)


