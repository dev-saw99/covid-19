import streamlit as st
import requests as rq
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as  plt
import plotly.graph_objs as go
import time


def getData():
    total,statewise =0,0
    URL = 'https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise'
    # print("\n----------------------------------------------\n")
    try:
        dataObj = rq.get(url=URL)
        dataObj = dataObj.json()
        data = dataObj['data']
        total = pd.Series(data['total'])
        statewise = pd.DataFrame(data['statewise'])
        statewise.columns = ['Location','Confirmed','Recovered','Death','Foriegn']
    except:
        print("Error")
    return total,statewise

def getHistory():

    URL = 'https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise/history'
    # print("++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    history = 0
    try:
        historyObj = rq.get(url=URL)
        history  = historyObj.json()
        history = history['data']['history']
        
        data  = []
        for days in history:
            days["total"]['date']  = days['day']
            data.append(days["total"])
        history = pd.DataFrame(data) 

        
    except:
        print("Error")
    return history

def getMap(statewise):
    map_df = gpd.read_file('main/Indian_States.shp')
    map_df['st_nm']=['Andaman and Nicobar Islands', 'Arunachal Pradesh', 'Assam', 'Bihar',
           'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli', 'Daman and Diu',
           'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir',
           'Jharkhand', 'Karnataka', 'Kerala', 'Lakshadweep', 'Madhya Pradesh',
           'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland',
           'Delhi', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim',
           'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand',
           'West Bengal', 'Odisha', 'Andhra Pradesh']
    merged = map_df.set_index('st_nm').join(statewise.set_index('Location'))
    return merged



his = getHistory()
total,statewise = getData()
merged = getMap(statewise)

statewise.sort_values(by='Confirmed',ascending=False,inplace=True)
statewise['Rank'] = list(range(1,38))
statewise.set_index('Rank',inplace=True)

st.markdown(
    "<span style='color:#505050;font-size:58px;font-weight:bold;'>India</span>&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:darkred;font-size:28px;font-weight:bold;'>Covid-19</span><br><span style='color:darkgrey;font-size:80px;font-weight:bold;'>Confirmed : {} </span><br><span style='color:red;font-size:29px;font-weight:bold;'>Death : {} </span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span style='color:green;font-size:30px;font-weight:bold;'>Recovered : {} </span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:orange;font-size:30px;font-weight:bold;'>Active : {} </span><br>".format(
        total.confirmed,
        total.deaths,
        total.recovered,
        total.active,
    ),
    unsafe_allow_html=True
)
@st.cache
def confirmPlot():
    layout = go.Layout(
        width=650,
        height=300,
        margin=dict(
        l=0,
        r=0,
        b=30,
        t=30,
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(2,0,0,0.01)',
    
    )
    fig = go.Figure(layout=layout)
    fig.add_trace(go.Scatter(x=his.date, y=his.confirmed,
                        mode='lines+markers',
                        name='lines',
                        line = dict(color = 'darkgrey',width=4),
                        marker = dict(size=8)))
    
    return fig

@st.cache
def RecoverVsDeathPlot():
    layout = go.Layout(
        width=770,
        height=300,
        margin=dict(
        l=30,
        r=0,
        b=30,
        t=30,
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(2,0,0,0.02)',
    
    )
    fig = go.Figure(layout=layout)

    fig.add_trace(go.Scatter(x=his.date, y=his.deaths,
                        mode='lines+markers',
                        name='Deaths',
                        line = dict(color = 'darkred',width=4),
                        marker = dict(size=8)))
    
    fig.add_trace(go.Scatter(x=his.date, y=his.recovered,
                        mode='lines+markers',
                        name='Recovered',
                        line = dict(color = 'limegreen',width=4),
                        marker = dict(size=8)))
    return fig

@st.cache
def RecoverVsActivePlot():
    layout = go.Layout(
        width=770,
        height=300,
        margin=dict(
        l=30,
        r=0,
        b=30,
        t=30,
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(2,0,0,0.02)',
    
    )
    fig = go.Figure(layout=layout)

    fig.add_trace(go.Scatter(x=his.date, y=his.recovered,
                        mode='lines+markers',
                        name='Recovered',
                        line = dict(color = 'limegreen',width=4),
                        marker = dict(size=8)))
    
    fig.add_trace(go.Scatter(x=his.date, y=his.active,
                        mode='lines+markers',
                        name='Active',
                        line = dict(color = 'orange',width=4),
                        marker = dict(size=8)))
    return fig

def mapPlot():
    fig1,ax=plt.subplots(1,figsize=(25,20))
    ax.axis('off')
    merged.plot(column='Confirmed',cmap='Oranges',ax=ax,linewidth=0.8,edgecolor='0.8')
    return ax.figure

st.markdown("**<BR>Confirmed Cases**",unsafe_allow_html=True)
st.write(confirmPlot())

st.markdown("**<BR>Recovered vs Deaths**",unsafe_allow_html=True)
st.write(RecoverVsDeathPlot())

st.markdown("**<BR>Recovered vs Active**",unsafe_allow_html=True)
st.write(RecoverVsActivePlot())

st.markdown("**<BR>Affected States**",unsafe_allow_html=True)
st.write(mapPlot())

st.markdown("**<BR>Statewise Statistics**",unsafe_allow_html=True)
st.table(
    statewise
)
# st.write(history)