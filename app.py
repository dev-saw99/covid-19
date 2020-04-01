import streamlit as st
import requests as rq
import pandas as pd
# import plotly.express as px
import plotly.graph_objs as go
import time

statewise =0
total=0

def getData():
    global total,statewise
    
    URL = 'https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise'
    print("\n----------------------------------------------\n")
    try:
        dataObj = rq.get(url=URL)
        dataObj = dataObj.json()
        data = dataObj['data']
        total = pd.Series(data['total'])
        statewise = pd.DataFrame(data['statewise'])
        statewise.columns = ['Location','Confirmed','Recovered','Death','Foriegn']
    except:
        print("Error")

def getHistory():

    URL = 'https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise/history'
    print("++++++++++++++++++++++++++++++++++++++++++++++++++\n")
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


his = getHistory()

getData()
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

st.markdown("**<BR>Confirmed Cases**",unsafe_allow_html=True)
st.write(confirmPlot())

st.markdown("**<BR>Recovered vs Deaths**",unsafe_allow_html=True)
st.write(RecoverVsDeathPlot())

st.markdown("**<BR>Recovered vs Active**",unsafe_allow_html=True)
st.write(RecoverVsActivePlot())

st.markdown("**<BR>Statewise Statistics**",unsafe_allow_html=True)
st.table(
    statewise
)
# st.write(history)