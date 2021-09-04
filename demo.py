import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import plotly.express as px
import plotly.graph_objects as go


header = st.container()
dataset = st.container()
interactive = st.container()

st.markdown(
    '''
    <style>
    .main {
    background-color: #F5F5F5;
    }
    </style>
    ''',
    unsafe_allow_html=True
)
background_color = '#F5F5F5'


@st.cache
def get_data(filename):
    data = [(random.randint(0, 100), i+2010) for i in range(10)]
    data = pd.DataFrame(data= data, columns= ['Value', 'Year'])
    return data
with header:
    st.title('Welcome to demo of budget 10 hack!')
    st.text('In this demo stand you can read the data and see the dependencies.')


with dataset:
    st.header('Dataset')
    data = get_data(None)
    st.write(data)

with interactive:
    st.title('Simple graph')
    fig = px.line(x=data['Year'], y=data['Value'])
    fig.update_yaxes(title = 'Value')
    fig.update_xaxes(type = 'category', title = 'Year')
    st.write(fig)


